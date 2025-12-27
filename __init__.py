"""
GeoNodesGuide - Live In-Editor Node Reference & Cheat Sheet for Geometry Nodes

A Blender add-on that shows helpful documentation when you hover over geometry nodes.

VERSION 0.1:
- Text-based documentation with commonly used nodes and real-world examples
- Tooltip stays visible until ESC is pressed
- Toggle button to activate/deactivate
- Fixed position below sidebar panel
"""

bl_info = {
    "name": "Geo Nodes Guide",
    "author": "Addonyte",
    "version": (0, 1, 0),
    "blender": (5, 0, 0),
    "location": "Node Editor > Sidebar > Geo Nodes Guide",
    "description": "Live documentation and examples for Geometry Nodes",
    "category": "Node",
}

import bpy
import blf
from bpy.types import Operator, Panel
import gpu
from gpu_extras.batch import batch_for_shader
import time
import urllib.parse

# Import our modules
from . import database


# ==============================================================================
# GLOBAL STATE - Track if addon is active
# ==============================================================================

class GeoNodesGuideState:
    """Global state for the addon."""
    is_active = False
    operator_instance = None
    current_node_name = ""  # Store current node name for feedback
    current_node_id = ""  # Store current node bl_idname


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def get_active_node_tree():
    """Find the active geometry node tree."""
    for area in bpy.context.screen.areas:
        if area.type == 'NODE_EDITOR':
            for space in area.spaces:
                if space.type == 'NODE_EDITOR':
                    if space.tree_type == 'GeometryNodeTree' and space.node_tree:
                        return space.node_tree
    return None


def get_sidebar_position(context):
    """Get the position below the GeoNodesGuide sidebar panel."""
    # Default position if we can't find the sidebar
    region = context.region
    
    # The sidebar is on the right side of the node editor
    # We'll position the tooltip at a fixed position from the right edge
    # Approximate: sidebar is about 250px wide, panel starts near top
    
    x = region.width - 490  # Position from right edge
    y = region.height - 250  # Position from top (below the panel)
    
    return (x, y)


# ==============================================================================
# FEEDBACK SYSTEM
# ==============================================================================

def get_addon_version():
    """Get addon version as string."""
    return "0.1.0"


def get_prefilled_form_url(node_name, blender_version, addon_version, feedback):
    """Generate pre-filled Google Form URL."""
    base_url = "https://docs.google.com/forms/d/e/1FAIpQLSczlVz-aBZBPH4EwhcUdDjsxl8E8qz0Qs_sADJKf3wf0jxiig/viewform"
    
    # Entry IDs from the Google Form
    params = {
        "usp": "pp_url",
        "entry.137672584": node_name,       # Node Name
        "entry.1146918867": feedback,        # Feedback
        "entry.978863237": blender_version,  # Blender Version
        "entry.1992068176": addon_version    # Addon Version
    }
    
    return base_url + "?" + urllib.parse.urlencode(params)


class GEONODESGUIDE_OT_SubmitFeedback(Operator):
    """Open feedback form in browser with node info pre-filled"""
    bl_idname = "geonodesguide.submit_feedback"
    bl_label = "Submit Feedback"
    bl_options = {'INTERNAL'}
    
    def execute(self, context):
        # Get versions and node info
        blender_version = bpy.app.version_string
        addon_version = get_addon_version()
        node_name = GeoNodesGuideState.current_node_name or "Unknown Node"
        
        # Generate pre-filled form URL (feedback left empty for user to fill in browser)
        url = get_prefilled_form_url(
            node_name,
            blender_version,
            addon_version,
            ""  # User fills this in the browser
        )
        
        # Open in browser
        bpy.ops.wm.url_open(url=url)
        
        self.report({'INFO'}, "Feedback form opened in browser")
        return {'FINISHED'}


# ==============================================================================
# MAIN TOOLTIP OPERATOR
# ==============================================================================

class GEONODESGUIDE_OT_ShowTooltip(Operator):
    """Toggle Geo Nodes Guide hover tooltips"""
    bl_idname = "geonodesguide.show_tooltip"
    bl_label = "Geo Nodes Guide"
    bl_options = {'INTERNAL'}
    
    # State variables
    _timer = None
    _handle = None
    _current_node = None
    _displayed_node = None  # The node whose info is currently shown
    _mouse_pos = (0, 0)
    _tooltip_visible = False
    _close_button_rect = None
    _tooltip_rect = None
    _feedback_button_rect = None
    _back_button_rect = None
    _submit_button_rect = None
    _last_hover_time = 0
    
    def modal(self, context, event):
        """Main event loop."""
        
        # ESC key handling - two-stage: first close tooltip, then deactivate
        if event.type == 'ESC' and event.value == 'PRESS':
            if self._tooltip_visible:
                # First ESC: just close the tooltip
                self.close_tooltip()
                context.area.tag_redraw()
                return {'RUNNING_MODAL'}
            else:
                # Second ESC (no tooltip visible): deactivate addon
                self.cancel(context)
                return {'CANCELLED'}
        
        if context.area.type != 'NODE_EDITOR':
            self.cancel(context)
            return {'CANCELLED'}
        
        self._mouse_pos = (event.mouse_region_x, event.mouse_region_y)
        
        # Handle scroll wheel for tooltip scrolling
        if event.type == 'WHEELUPMOUSE' and self._tooltip_visible:
            if self._tooltip_rect and self.is_point_in_rect(self._mouse_pos, self._tooltip_rect):
                self._scroll_offset = max(0, self._scroll_offset - 30)
                context.area.tag_redraw()
                return {'RUNNING_MODAL'}
        
        if event.type == 'WHEELDOWNMOUSE' and self._tooltip_visible:
            if self._tooltip_rect and self.is_point_in_rect(self._mouse_pos, self._tooltip_rect):
                self._scroll_offset = min(self._max_scroll, self._scroll_offset + 30)
                context.area.tag_redraw()
                return {'RUNNING_MODAL'}
        
        # Handle mouse clicks
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            # Close button click
            if self._tooltip_visible and self._close_button_rect:
                if self.is_point_in_rect(self._mouse_pos, self._close_button_rect):
                    self.close_tooltip()
                    context.area.tag_redraw()
                    return {'RUNNING_MODAL'}
            
            # All other clicks pass through - tooltip stays open
            return {'PASS_THROUGH'}
        
        # Handle mouse movement - only show NEW tooltip if none is visible
        if event.type == 'MOUSEMOVE':
            context.area.tag_redraw()
            
            # If tooltip already visible, don't change it (user must ESC to see new node)
            if self._tooltip_visible:
                # Check if displayed node was deleted by trying to get it fresh
                if self.get_valid_node(context) is None:
                    self.close_tooltip()
                return {'PASS_THROUGH'}
            
            # No tooltip visible - check for node hover
            node = self.get_node_under_mouse(context, event)
            if node:
                # Compare by name to avoid accessing stale node reference
                try:
                    current_name = self._current_node.name if self._current_node else None
                    new_name = node.name
                except:
                    current_name = None
                    new_name = None
                
                if new_name != current_name:
                    self._current_node = node
                    self._last_hover_time = time.time()
                elif time.time() - self._last_hover_time > 0.3:  # Faster response
                    # Show tooltip for this node
                    self.set_displayed_node(node, context)
                    self._tooltip_visible = True
                    context.area.tag_redraw()
            else:
                # Not hovering over any node
                self._current_node = None
                self._last_hover_time = 0
        
        return {'PASS_THROUGH'}
    
    def close_tooltip(self):
        """Close the tooltip but keep addon active."""
        self._tooltip_visible = False
        self._displayed_node = None
        self._displayed_node_name = None
        self._displayed_node_tree = None
        self._current_node = None
        self._last_hover_time = 0
        self._scroll_offset = 0  # Reset scroll when closing
    
    def is_point_in_rect(self, point, rect):
        """Check if point is inside rectangle."""
        x, y = point
        rx, ry, rw, rh = rect
        return rx <= x <= rx + rw and ry - rh <= y <= ry
    
    def get_node_under_mouse(self, context, event):
        """Find node under mouse cursor."""
        space = context.space_data
        if not space.node_tree or space.tree_type != 'GeometryNodeTree':
            return None
        
        mouse_x, mouse_y = event.mouse_region_x, event.mouse_region_y
        view2d = context.region.view2d
        
        for node in space.node_tree.nodes:
            node_left, node_top = node.location[0], node.location[1]
            node_right = node_left + node.width
            node_bottom = node_top - node.dimensions.y
            
            screen_left, screen_top = view2d.view_to_region(node_left, node_top, clip=False)
            screen_right, screen_bottom = view2d.view_to_region(node_right, node_bottom, clip=False)
            
            if screen_left <= mouse_x <= screen_right and screen_bottom <= mouse_y <= screen_top:
                return node
        return None
    
    def invoke(self, context, event):
        """Toggle the tooltip system."""
        # If already active, deactivate
        if GeoNodesGuideState.is_active and GeoNodesGuideState.operator_instance:
            GeoNodesGuideState.operator_instance.cancel(context)
            return {'CANCELLED'}
        
        # Activate
        if context.area.type == 'NODE_EDITOR':
            self._handle = bpy.types.SpaceNodeEditor.draw_handler_add(
                self.draw_tooltip, (context,), 'WINDOW', 'POST_PIXEL')
            self._timer = context.window_manager.event_timer_add(0.05, window=context.window)
            context.window_manager.modal_handler_add(self)
            
            GeoNodesGuideState.is_active = True
            GeoNodesGuideState.operator_instance = self
            
            self.report({'INFO'}, "Geo Nodes Guide activated - hover over nodes for help! Press ESC to close tooltip.")
            return {'RUNNING_MODAL'}
        return {'CANCELLED'}
    
    def cancel(self, context):
        """Clean up when deactivated."""
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None
        if self._handle:
            bpy.types.SpaceNodeEditor.draw_handler_remove(self._handle, 'WINDOW')
            self._handle = None
        
        GeoNodesGuideState.is_active = False
        GeoNodesGuideState.operator_instance = None
        
        self.report({'INFO'}, "Geo Nodes Guide deactivated")
        context.area.tag_redraw()
    
    # ==========================================================================
    # DRAWING FUNCTIONS
    # ==========================================================================
    
    # Scroll state
    _scroll_offset = 0
    _max_scroll = 0
    
    # Store node identification separately (not just reference)
    _displayed_node_name = None
    _displayed_node_tree = None
    
    def get_valid_node(self, context):
        """Get the displayed node if it's still valid, None otherwise.
        
        Instead of storing a node reference (which becomes invalid when deleted),
        we store the node name and tree, then look up the node fresh each time.
        """
        if not self._displayed_node_name or not self._displayed_node_tree:
            return None
        
        try:
            # Check if the tree is still valid
            tree = self._displayed_node_tree
            if tree is None:
                return None
            
            # Look up the node by name in the tree
            if self._displayed_node_name in tree.nodes:
                return tree.nodes[self._displayed_node_name]
            else:
                return None
        except:
            return None
    
    def set_displayed_node(self, node, context):
        """Store node identification for later lookup."""
        if node is None:
            self._displayed_node = None
            self._displayed_node_name = None
            self._displayed_node_tree = None
        else:
            try:
                self._displayed_node = node
                self._displayed_node_name = node.name
                self._displayed_node_tree = node.id_data
            except:
                self._displayed_node = None
                self._displayed_node_name = None
                self._displayed_node_tree = None
    
    def draw_tooltip(self, context):
        """Main tooltip drawing function."""
        if not self._tooltip_visible:
            return
        
        # Get node fresh from tree (safe even if original reference is stale)
        node = self.get_valid_node(context)
        
        if node is None:
            # Node was deleted or invalid
            self._tooltip_visible = False
            self._displayed_node = None
            self._displayed_node_name = None
            self._displayed_node_tree = None
            return
        
        # Now safe to access node properties
        try:
            node_type = node.bl_idname
            node_label = node.label
            node_name = node.name
        except:
            # Fallback in case of any other issue
            self._tooltip_visible = False
            self._displayed_node = None
            self._displayed_node_name = None
            self._displayed_node_tree = None
            return
        
        display_name = node_label or node_name
        
        # Store current node info for feedback
        GeoNodesGuideState.current_node_name = display_name
        GeoNodesGuideState.current_node_id = node_type
        
        # Get node info from database
        info = database.get_node_info(node_type)
        
        if not info:
            # Show bl_idname in tooltip for debugging
            self.draw_basic_tooltip(context, display_name, node_type)
            return
        
        # Calculate position - below the sidebar panel with gap
        region = context.region
        
        # Make box wider - 420px width (extended to the left)
        box_width = 420
        font_id = 0
        
        # First, calculate content height
        header_height = 28  # Compact header with just title
        content_padding = 16  # Gap below header before content starts
        
        # Calculate wrapped description lines
        blf.size(font_id, 12)
        desc_lines = self.wrap_text(info["description"], font_id, box_width - 30)
        
        # Calculate wrapped example lines if present
        blf.size(font_id, 11)
        example_lines = []
        if "example" in info:
            example_lines = self.wrap_text(info["example"], font_id, box_width - 30)
        
        # Calculate total content height
        content_height = 0
        content_height += len(desc_lines) * 16  # description
        content_height += 10 + 18  # Common Uses header + gap
        content_height += len(info.get("common_uses", [])) * 16  # uses
        content_height += 10 + 18  # Pitfalls header + gap
        content_height += len(info.get("pitfalls", [])) * 16  # pitfalls
        if "commonly_used_with" in info:
            content_height += 10 + 18  # Often Combined With header + gap
            content_height += min(4, len(info["commonly_used_with"])) * 16  # items
        if "example" in info:
            content_height += 10 + 18  # Example header + gap
            content_height += len(example_lines) * 16  # example lines
        content_height += 15  # bottom padding
        
        # Calculate box height based on content
        total_height = header_height + content_padding + content_height
        
        # Position - below the sidebar panel (account for feedback button)
        x = region.width - box_width - 25  # Align right edge with sidebar
        y = region.height - 130  # Lower to account for Submit Feedback button
        
        # Set box height to fit content, but cap at available space
        available_height = y - 20
        box_height = min(total_height, available_height)
        
        # Make sure box fits
        if x < 10:
            x = 10
        
        # Store rect for click detection
        self._tooltip_rect = (x, y, box_width, box_height)
        
        # Enable blending
        gpu.state.blend_set('ALPHA')
        
        # Draw background
        self.draw_box(x, y, box_width, box_height, (0.12, 0.12, 0.12, 0.98))
        self.draw_box(x, y, box_width, header_height, (0.08, 0.08, 0.08, 0.98))
        
        # Draw close button
        close_size = 18
        close_x, close_y = x + box_width - close_size - 6, y - 5
        self._close_button_rect = (close_x, close_y, close_size, close_size)
        
        mx, my = self._mouse_pos
        hovering_close = close_x <= mx <= close_x + close_size and close_y - close_size <= my <= close_y
        self.draw_box(close_x, close_y, close_size, close_size, 
                     (0.8, 0.2, 0.2, 0.9) if hovering_close else (0.3, 0.3, 0.3, 0.7))
        
        blf.position(font_id, close_x + 4, close_y - 14, 0)
        blf.size(font_id, 12)
        blf.color(font_id, 1, 1, 1, 1)
        blf.draw(font_id, "✕")
        
        # Draw title - centered vertically in header
        blf.position(font_id, x + 10, y - 18, 0)
        blf.size(font_id, 13)
        blf.color(font_id, 0.3, 0.7, 1, 1)
        title = info["display_name"]
        blf.draw(font_id, title)
        
        # Content area starts here (below header with padding)
        content_top = y - header_height - content_padding
        visible_height = box_height - header_height - 20
        scroll = self._scroll_offset
        
        # Calculate content width (leaving space for scrollbar)
        content_width = box_width - 20
        
        # Bottom boundary for clipping
        content_bottom_boundary = y - box_height + 5
        
        # Track y position for all content
        y_pos = content_top + scroll
        
        # Draw description
        blf.size(font_id, 12)
        blf.color(font_id, 0.85, 0.85, 0.85, 1)
        for line in desc_lines:
            if y_pos > content_bottom_boundary and y_pos <= content_top:
                blf.position(font_id, x + 10, y_pos, 0)
                blf.draw(font_id, line)
            y_pos -= 16
        
        # Draw Common Uses
        y_pos -= 10
        if y_pos > content_bottom_boundary and y_pos <= content_top:
            blf.position(font_id, x + 8, y_pos, 0)
            blf.size(font_id, 13)
            blf.color(font_id, 0.5, 1, 0.5, 1)
            blf.draw(font_id, "✓ Common Uses:")
        y_pos -= 18
        blf.size(font_id, 11)
        blf.color(font_id, 0.75, 0.75, 0.75, 1)
        for use in info["common_uses"]:
            if y_pos > content_bottom_boundary and y_pos <= content_top:
                blf.position(font_id, x + 15, y_pos, 0)
                blf.draw(font_id, "• " + use)
            y_pos -= 16
        
        # Draw Pitfalls
        y_pos -= 10
        if y_pos > content_bottom_boundary and y_pos <= content_top:
            blf.position(font_id, x + 8, y_pos, 0)
            blf.size(font_id, 13)
            blf.color(font_id, 1, 0.6, 0.3, 1)
            blf.draw(font_id, "⚠ Pitfalls:")
        y_pos -= 18
        blf.size(font_id, 11)
        blf.color(font_id, 1, 0.8, 0.6, 1)
        for pit in info["pitfalls"]:
            if y_pos > content_bottom_boundary and y_pos <= content_top:
                blf.position(font_id, x + 15, y_pos, 0)
                blf.draw(font_id, "• " + pit)
            y_pos -= 16
        
        # Draw Often Combined With section
        if "commonly_used_with" in info:
            y_pos -= 10
            if y_pos > content_bottom_boundary and y_pos <= content_top:
                blf.position(font_id, x + 8, y_pos, 0)
                blf.size(font_id, 13)
                blf.color(font_id, 0.4, 0.8, 1, 1)
                blf.draw(font_id, "🔗 Often Combined With:")
            y_pos -= 18
            blf.size(font_id, 11)
            blf.color(font_id, 0.7, 0.85, 1, 1)
            for node_name, reason in info["commonly_used_with"][:4]:
                if y_pos > content_bottom_boundary and y_pos <= content_top:
                    blf.position(font_id, x + 15, y_pos, 0)
                    text = f"• {node_name} - {reason}"
                    blf.draw(font_id, text)
                y_pos -= 16
        
        # Draw Real World Example section
        if "example" in info:
            y_pos -= 10
            if y_pos > content_bottom_boundary and y_pos <= content_top:
                blf.position(font_id, x + 8, y_pos, 0)
                blf.size(font_id, 13)
                blf.color(font_id, 1, 0.8, 0.4, 1)
                blf.draw(font_id, "💡 Real World Example:")
            y_pos -= 18
            blf.size(font_id, 11)
            blf.color(font_id, 0.85, 0.85, 0.75, 1)
            example_lines = self.wrap_text(info["example"], font_id, content_width - 10)
            for line in example_lines:
                if y_pos > content_bottom_boundary and y_pos <= content_top:
                    blf.position(font_id, x + 10, y_pos, 0)
                    blf.draw(font_id, line)
                y_pos -= 16
        
        # Add padding at bottom
        y_pos -= 5
        
        # Calculate max scroll based on actual content
        content_bottom = y_pos - scroll  # Actual bottom position without scroll
        total_content_height = content_top - content_bottom
        self._max_scroll = max(0, total_content_height - visible_height + 5)
        
        # Clamp scroll offset
        self._scroll_offset = max(0, min(self._scroll_offset, self._max_scroll))
        
        # Draw scroll indicator if needed
        if self._max_scroll > 0:
            track_height = visible_height - 10
            scroll_ratio = visible_height / total_content_height
            scroll_bar_height = max(30, track_height * scroll_ratio)
            scroll_progress = self._scroll_offset / self._max_scroll if self._max_scroll > 0 else 0
            scroll_bar_y = y - header_height - 5 - (track_height - scroll_bar_height) * scroll_progress
            
            # Scroll track
            self.draw_box(x + box_width - 10, y - header_height, 6, track_height, (0.2, 0.2, 0.2, 0.5))
            # Scroll thumb
            self.draw_box(x + box_width - 10, scroll_bar_y, 6, scroll_bar_height, (0.5, 0.5, 0.5, 0.9))
    
    def wrap_text(self, text, font_id, max_width):
        """Wrap text to fit within max_width."""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = " ".join(current_line)
            if blf.dimensions(font_id, test_line)[0] > max_width:
                current_line.pop()
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return lines
    
    def draw_basic_tooltip(self, context, node_name, bl_idname=""):
        """Draw a simple tooltip for undocumented nodes."""
        region = context.region
        
        # Match main tooltip sizing
        box_width = 420
        box_height = 100
        
        # Position: same as main tooltip (lower to account for Submit Feedback button)
        x = region.width - box_width - 25  # Align right edge with sidebar
        y = region.height - 130
        
        if x < 10:
            x = 10
        
        font_id = 0
        
        self._tooltip_rect = (x, y, box_width, box_height)
        
        # Draw background
        self.draw_box(x, y, box_width, box_height, (0.12, 0.12, 0.12, 0.98))
        self.draw_box(x, y, box_width, 28, (0.08, 0.08, 0.08, 0.98))
        
        # Draw close button
        close_size = 18
        close_x, close_y = x + box_width - close_size - 6, y - 5
        self._close_button_rect = (close_x, close_y, close_size, close_size)
        
        mx, my = self._mouse_pos
        hovering_close = close_x <= mx <= close_x + close_size and close_y - close_size <= my <= close_y
        self.draw_box(close_x, close_y, close_size, close_size, 
                     (0.8, 0.2, 0.2, 0.9) if hovering_close else (0.3, 0.3, 0.3, 0.7))
        
        blf.position(font_id, close_x + 4, close_y - 14, 0)
        blf.size(font_id, 12)
        blf.color(font_id, 1, 1, 1, 1)
        blf.draw(font_id, "✕")
        
        # Draw title - centered in header
        blf.position(font_id, x + 10, y - 18, 0)
        blf.size(font_id, 13)
        blf.color(font_id, 0.3, 0.7, 1, 1)
        # Truncate if too long
        if len(node_name) > 35:
            node_name = node_name[:33] + "..."
        blf.draw(font_id, node_name)
        
        # Draw message
        blf.position(font_id, x + 10, y - 50, 0)
        blf.size(font_id, 11)
        blf.color(font_id, 0.7, 0.7, 0.7, 1)
        blf.draw(font_id, "Documentation coming soon!")
        
        # Draw bl_idname for debugging
        if bl_idname:
            blf.position(font_id, x + 10, y - 70, 0)
            blf.size(font_id, 9)
            blf.color(font_id, 0.5, 0.7, 0.5, 1)
            blf.draw(font_id, f"Node ID: {bl_idname}")
    
    def draw_box(self, x, y, w, h, color):
        """Draw a colored rectangle."""
        verts = ((x, y), (x + w, y), (x + w, y - h), (x, y - h))
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'TRIS', {"pos": verts}, indices=((0, 1, 2), (2, 3, 0)))
        shader.bind()
        shader.uniform_float("color", color)
        batch.draw(shader)
    
    def draw_wrapped_text(self, font_id, text, x, y, max_w):
        """Draw text with word wrapping."""
        words, lines, line = text.split(), [], []
        for w in words:
            line.append(w)
            if blf.dimensions(font_id, " ".join(line))[0] > max_w:
                line.pop()
                lines.append(" ".join(line))
                line = [w]
        if line:
            lines.append(" ".join(line))
        for i, ln in enumerate(lines[:3]):
            blf.position(font_id, x, y - i * 16, 0)
            blf.draw(font_id, ln)


# ==============================================================================
# UI PANEL
# ==============================================================================

class GEONODESGUIDE_PT_Panel(Panel):
    """Geo Nodes Guide sidebar panel."""
    bl_label = "Geo Nodes Guide"
    bl_idname = "GEONODESGUIDE_PT_panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Geo Nodes Guide"
    
    def draw(self, context):
        layout = self.layout
        
        # Hover Help button
        row = layout.row()
        row.scale_y = 1.8
        
        if GeoNodesGuideState.is_active:
            sub = row.row()
            sub.active = True
            sub.operator("geonodesguide.show_tooltip", text="Hover Help Active", icon='HIDE_OFF', depress=True)
        else:
            row.operator("geonodesguide.show_tooltip", text="Activate Hover Help", icon='HIDE_ON')
        
        # Submit Feedback button (only show when there's a current node)
        if GeoNodesGuideState.current_node_name:
            layout.separator()
            row = layout.row()
            row.scale_y = 1.2
            row.operator("geonodesguide.submit_feedback", text="Submit Feedback", icon='URL')


# ==============================================================================
# REGISTRATION
# ==============================================================================

classes = (
    GEONODESGUIDE_OT_SubmitFeedback,
    GEONODESGUIDE_OT_ShowTooltip,
    GEONODESGUIDE_PT_Panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    print(f"Geo Nodes Guide v0.1 loaded - {len(database.NODE_DATABASE)} nodes documented!")


def unregister():
    # Clean up any active operator
    if GeoNodesGuideState.is_active and GeoNodesGuideState.operator_instance:
        try:
            GeoNodesGuideState.operator_instance.cancel(bpy.context)
        except:
            pass
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
