"""
NodeDoc - Database
All node information, descriptions, common uses, pitfalls, related nodes, and examples.

To add a new node:
1. Find its bl_idname (e.g., 'GeometryNodeMeshCube')
2. Add an entry to NODE_DATABASE with the same structure
"""

NODE_DATABASE = {
    
    # ==========================================================================
    # POINT NODES
    # ==========================================================================
    
    "GeometryNodeDistributePointsOnFaces": {
        "display_name": "Distribute Points on Faces",
        "category": "Point",
        "description": "Scatters points across mesh surfaces - the foundation of any scatter/instancing system.",
        "common_uses": [
            "Grass and vegetation placement",
            "Rock and debris scattering",
            "Even surface coverage"
        ],
        "pitfalls": [
            "Poisson Disk prevents clumping but runs slower",
            "High density values impact viewport performance",
            "Weight Paint input controls local density variation"
        ],
        "commonly_used_with": [
            ("Instance on Points", "place objects at scattered locations"),
            ("Random Value", "vary rotation/scale per point"),
            ("Realize Instances", "convert to real geometry for Booleans"),
            ("Set Material", "assign materials to instances")
        ],
        "example": "For a meadow: connect ground mesh, set Density to 10, choose Poisson Disk for even spacing. Pipe result to Instance on Points with grass blade as input. Use Weight Paint on mesh to control where grass appears denser."
    },
    
    "GeometryNodeDistributePointsInVolume": {
        "display_name": "Distribute Points in Volume",
        "category": "Point",
        "description": "Fills the inside of a closed mesh with points - requires watertight geometry.",
        "common_uses": [
            "Marbles in a jar effect",
            "Volumetric fog/particle clouds",
            "3D object filling"
        ],
        "pitfalls": [
            "Mesh must be completely sealed (no holes)",
            "Non-manifold edges cause unpredictable results",
            "Dense fills consume significant memory"
        ],
        "commonly_used_with": [
            ("Instance on Points", "visualize as spheres or objects"),
            ("Random Value", "size/rotation variation"),
            ("Mesh Boolean", "create complex container shapes"),
            ("Convex Hull", "wrap points in outer shell")
        ],
        "example": "For candy jar: use jar mesh (must be closed), set density, instance small spheres at each point. Grid mode gives uniform spacing, Random mode gives organic distribution."
    },
    
    "GeometryNodePoints": {
        "display_name": "Points",
        "category": "Point",
        "description": "Generates a cloud of points at the origin - the simplest starting primitive.",
        "common_uses": [
            "Custom array layouts",
            "Procedural pattern seeds",
            "Particle system origins"
        ],
        "pitfalls": [
            "All points start at (0,0,0) - must reposition",
            "Invisible until instanced or given radius",
            "High counts affect performance"
        ],
        "commonly_used_with": [
            ("Set Position", "arrange in grids/circles/patterns"),
            ("Instance on Points", "make visible with geometry"),
            ("Index", "number-based positioning math"),
            ("Random Value", "scatter positions")
        ],
        "example": "Create 100 points, use Index with Sine/Cosine math to arrange in a circle, then instance cubes at each position. Points are invisible coordinates until you attach geometry to them."
    },
    
    # ==========================================================================
    # INSTANCE NODES
    # ==========================================================================
    
    "GeometryNodeInstanceOnPoints": {
        "display_name": "Instance on Points",
        "category": "Instances",
        "description": "Stamps copies of geometry at each point location - the core of any scatter system.",
        "common_uses": [
            "Forest and vegetation generation",
            "Crowd replication",
            "Repeating pattern creation"
        ],
        "pitfalls": [
            "Instances are linked copies, not real geometry",
            "Cannot use Booleans without Realize Instances first",
            "Complex source objects multiply viewport load"
        ],
        "commonly_used_with": [
            ("Distribute Points on Faces", "source point locations"),
            ("Random Value", "per-instance scale/rotation variation"),
            ("Collection Info", "randomly pick from multiple objects"),
            ("Realize Instances", "convert to editable mesh")
        ],
        "example": "Scatter points on terrain, plug tree model into Instance input. Each point spawns a tree. Enable Pick Instance + Collection Info to randomly choose between oak, pine, birch variations."
    },
    
    "GeometryNodeRealizeInstances": {
        "display_name": "Realize Instances",
        "category": "Instances",
        "description": "Converts linked instances into actual independent geometry - use only when necessary.",
        "common_uses": [
            "Pre-Boolean operation conversion",
            "Vertex-level mesh editing",
            "Export to non-instance formats"
        ],
        "pitfalls": [
            "Memory usage multiplies dramatically",
            "1000 instances = 1000× the vertex count",
            "Try operations without realizing first"
        ],
        "commonly_used_with": [
            ("Instance on Points", "source of instances"),
            ("Mesh Boolean", "requires real geometry"),
            ("Merge by Distance", "weld seams after realizing"),
            ("Set Position", "deform individual copies")
        ],
        "example": "Only use when required - Booleans, vertex editing, or exports. 100 tree instances stay light; realized, they become 100 full tree meshes. Check if your operation actually needs it first."
    },
    
    "GeometryNodeRotateInstances": {
        "display_name": "Rotate Instances",
        "category": "Instances",
        "description": "Spins instances around their pivot points without converting to real geometry.",
        "common_uses": [
            "Surface normal alignment",
            "Natural-looking scatter variation",
            "Animated spinning objects"
        ],
        "pitfalls": [
            "Input uses radians - multiply degrees by π/180",
            "Rotation order (XYZ) affects final orientation",
            "Local Space option rotates relative to instance"
        ],
        "commonly_used_with": [
            ("Random Value", "randomize per-instance angles"),
            ("Align Euler to Vector", "point instances at targets"),
            ("Normal", "orient perpendicular to surface"),
            ("Scene Time", "animate rotation over time")
        ],
        "example": "Scattered leaves: add Random Value (0 to 6.28 radians = full rotation) to Z axis. For grass pointing outward from curved ground, align to surface Normal using Align Euler to Vector first."
    },
    
    "GeometryNodeScaleInstances": {
        "display_name": "Scale Instances",
        "category": "Instances",
        "description": "Resizes instances from their pivot points - uniform or per-axis stretching.",
        "common_uses": [
            "Natural size variation in scatters",
            "Distance-based shrinking/growing",
            "Animated scale effects"
        ],
        "pitfalls": [
            "Negative values flip/mirror geometry",
            "Non-uniform scale can cause shearing",
            "Center mode scales from instance origin"
        ],
        "commonly_used_with": [
            ("Random Value", "size variation (0.8 to 1.2 typical)"),
            ("Map Range", "convert attributes to scale values"),
            ("Distance", "proximity-based sizing"),
            ("Scene Time", "pulsing/breathing animation")
        ],
        "example": "Realistic forest: Random Value with Min 0.6, Max 1.4 gives 40% size variation. Use Map Range to convert slope angle into scale - steeper areas get smaller trees."
    },
    
    "GeometryNodeTranslateInstances": {
        "display_name": "Translate Instances",
        "category": "Instances",
        "description": "Shifts instances by offset vectors - moves them from their point positions.",
        "common_uses": [
            "Floating objects above surface",
            "Offset stacking/layering",
            "Wave motion animation"
        ],
        "pitfalls": [
            "Local Space moves relative to instance orientation",
            "World Space ignores instance rotation",
            "Offset adds to current position, doesn't replace"
        ],
        "commonly_used_with": [
            ("Normal", "push along surface direction"),
            ("Random Value", "jitter offset"),
            ("Scene Time", "animated bobbing"),
            ("Combine XYZ", "build offset vector")
        ],
        "example": "Hover rocks above terrain: multiply surface Normal by height value (e.g., 0.5), use as Translation. Objects float at consistent height even on slopes. Add Sine(Time) for gentle bobbing."
    },
    
    # ==========================================================================
    # MESH PRIMITIVE NODES
    # ==========================================================================
    
    "GeometryNodeMeshCube": {
        "display_name": "Cube",
        "category": "Mesh Primitives",
        "description": "Generates a 6-faced box mesh - the fundamental building block primitive.",
        "common_uses": [
            "Architecture and structures",
            "Boolean cutting shapes",
            "Placeholder/proxy geometry"
        ],
        "pitfalls": [
            "Only 8 vertices unless subdivided (Vertices X/Y/Z)",
            "Size is total dimension, not half-extent",
            "No edge loops by default - add for beveling"
        ],
        "commonly_used_with": [
            ("Subdivision Surface", "round into sphere-like shape"),
            ("Bevel Mesh", "chamfered edges"),
            ("Mesh Boolean", "carve or combine shapes"),
            ("Transform Geometry", "position and orient")
        ],
        "example": "Size (2,1,3) creates a 2×1×3 meter box. For smooth deformation, increase Vertices X/Y/Z. For beveled edges, add Bevel node or increase vertices near corners first."
    },
    
    "GeometryNodeMeshUVSphere": {
        "display_name": "UV Sphere",
        "category": "Mesh Primitives",
        "description": "Creates a globe-style sphere with latitude/longitude topology - ideal for planet mapping.",
        "common_uses": [
            "Planets and world maps",
            "Balls and round objects",
            "UV-friendly spherical shapes"
        ],
        "pitfalls": [
            "Poles have converging triangles (pinching)",
            "Face sizes vary - small at poles, large at equator",
            "Use Ico Sphere for uniform face distribution"
        ],
        "commonly_used_with": [
            ("Set Shade Smooth", "essential for sphere appearance"),
            ("Noise Texture + Set Position", "planet terrain"),
            ("Subdivision Surface", "extra smoothness"),
            ("UV Map", "texture coordinates included")
        ],
        "example": "Segments=32, Rings=16 for smooth appearance. Higher for close-ups, lower for distant/game assets. The vertical seam makes it perfect for wrapping rectangular textures like Earth maps."
    },
    
    "GeometryNodeMeshIcoSphere": {
        "display_name": "Ico Sphere",
        "category": "Mesh Primitives",
        "description": "Creates an icosahedron-based sphere with evenly distributed faces - no polar pinching.",
        "common_uses": [
            "Geodesic domes",
            "Even point scattering base",
            "Low-poly crystal/gem shapes"
        ],
        "pitfalls": [
            "All triangles - no quad topology",
            "Subdivisions grow exponentially (1=80, 2=320, 3=1280 faces)",
            "Harder to UV unwrap than UV Sphere"
        ],
        "commonly_used_with": [
            ("Dual Mesh", "convert to hexagonal pattern"),
            ("Set Position + Noise", "organic planet terrain"),
            ("Distribute Points on Faces", "even surface coverage"),
            ("Subdivision Surface", "smoother version")
        ],
        "example": "Subdivision 1 = D20 die shape. For planets, Ico Sphere + displacement gives more uniform mountains than UV Sphere. Low subdivision with flat shading = crystal/gem aesthetic."
    },
    
    "GeometryNodeMeshCylinder": {
        "display_name": "Cylinder",
        "category": "Mesh Primitives",
        "description": "Generates a tube shape with optional end caps - pipes, columns, cans.",
        "common_uses": [
            "Pipes and plumbing",
            "Architectural columns",
            "Mechanical shafts"
        ],
        "pitfalls": [
            "Fill Type: N-Gon (clean), Triangle (deformable), None (open ends)",
            "Side Segments needed if you plan to bend it",
            "Vertices controls circular smoothness"
        ],
        "commonly_used_with": [
            ("Set Shade Smooth", "curved surface appearance"),
            ("Mesh Boolean", "cut cylindrical holes"),
            ("Curve to Mesh", "alternative for complex paths"),
            ("Bevel Mesh", "soften cap edges")
        ],
        "example": "Vertices 32 for smooth, 8 for game-ready. Depth = height. Side Segments: increase before bending/deforming. Fill Type None = pipe, N-Gon = solid ends."
    },
    
    "GeometryNodeMeshCone": {
        "display_name": "Cone",
        "category": "Mesh Primitives",
        "description": "Creates a tapered cylinder - point at top, circle at bottom (or truncated frustum).",
        "common_uses": [
            "Spikes and thorns",
            "Roof/tower tops",
            "Simple stylized trees"
        ],
        "pitfalls": [
            "Top Radius 0 = true point (pole vertex)",
            "Top Radius > 0 = flat-topped frustum",
            "Side Segments needed for smooth bending"
        ],
        "commonly_used_with": [
            ("Instance on Points", "spike arrays"),
            ("Rotate Instances", "random spike directions"),
            ("Set Shade Smooth", "smooth cone surface"),
            ("Transform Geometry", "orient point direction")
        ],
        "example": "Ice cream cone: bottom radius 0.3, top radius 0.5, height 1. Spike: top radius 0, many vertices for smooth. Truncated pyramid: top radius > 0, vertices = 4."
    },
    
    "GeometryNodeMeshGrid": {
        "display_name": "Grid",
        "category": "Mesh Primitives",
        "description": "Generates a flat subdivided plane - essential base for terrains and deformable surfaces.",
        "common_uses": [
            "Terrain heightmaps",
            "Water/ocean surfaces",
            "Cloth simulation base"
        ],
        "pitfalls": [
            "Size is total dimensions, not per-cell",
            "X/Y Vertices = subdivisions + 1 (100×100 verts = 99×99 cells)",
            "High resolution severely impacts performance"
        ],
        "commonly_used_with": [
            ("Noise Texture + Set Position", "terrain displacement"),
            ("Subdivision Surface", "smooth undulations"),
            ("Distribute Points on Faces", "scatter on terrain"),
            ("Set Shade Smooth", "smooth terrain shading")
        ],
        "example": "Terrain: Size 100×100m, Vertices 200×200. Displace Z with Noise Texture for hills. Start with low vertex count (50×50), increase only if detail is needed."
    },
    
    "GeometryNodeMeshLine": {
        "display_name": "Mesh Line",
        "category": "Mesh Primitives",
        "description": "Creates a row of connected vertices and edges - mesh version of a straight line.",
        "common_uses": [
            "Edge-based structures",
            "Array starting point",
            "Path before curve conversion"
        ],
        "pitfalls": [
            "No faces - only edges and vertices",
            "Mode: Count (fixed points) vs Resolution (points per unit)",
            "Offset mode defines direction and length"
        ],
        "commonly_used_with": [
            ("Mesh to Curve", "convert for curve operations"),
            ("Instance on Points", "objects along line"),
            ("Set Position", "reshape into custom path"),
            ("Extrude Mesh", "give width/thickness")
        ],
        "example": "Count Mode: exactly N points. Resolution Mode: 1 point per meter regardless of length. Use Start + Offset to define line direction and length."
    },
    
    # ==========================================================================
    # MESH OPERATION NODES
    # ==========================================================================
    
    "GeometryNodeMeshBoolean": {
        "display_name": "Mesh Boolean",
        "category": "Mesh Operations",
        "description": "Combines meshes with CSG operations - Union (add), Difference (subtract), Intersect (overlap only).",
        "common_uses": [
            "Cutting holes in walls",
            "Merging overlapping objects",
            "Complex hard-surface shapes"
        ],
        "pitfalls": [
            "Requires real geometry - Realize Instances first",
            "Both meshes must be closed (watertight)",
            "Slow with high-poly meshes"
        ],
        "commonly_used_with": [
            ("Realize Instances", "convert instances before boolean"),
            ("Cylinder", "circular hole cutter"),
            ("Merge by Distance", "cleanup after boolean"),
            ("Transform Geometry", "position cutter")
        ],
        "example": "Window in wall: Difference mode, wall as Mesh 1, box as Mesh 2 (cutter). Union to merge objects. Intersect keeps only where meshes overlap."
    },
    
    "GeometryNodeSubdivideMesh": {
        "display_name": "Subdivide Mesh",
        "category": "Mesh Operations",
        "description": "Splits faces into smaller faces without smoothing - adds geometry density only.",
        "common_uses": [
            "Pre-displacement detail",
            "Deformation preparation",
            "Increasing vertex resolution"
        ],
        "pitfalls": [
            "Level 1 = 4× faces, Level 2 = 16×, Level 3 = 64×",
            "Does NOT smooth - just splits",
            "Use Subdivision Surface if smoothing needed"
        ],
        "commonly_used_with": [
            ("Set Position", "displace denser mesh"),
            ("Noise Texture", "displacement source"),
            ("Grid", "subdivide flat terrain base"),
            ("Triangulate", "after for consistent topology")
        ],
        "example": "Need more vertices for detailed displacement? Subdivide first, then displace. Different from Subdivision Surface which also smooths geometry."
    },
    
    "GeometryNodeSubdivisionSurface": {
        "display_name": "Subdivision Surface",
        "category": "Mesh Operations",
        "description": "Smoothly subdivides mesh using Catmull-Clark algorithm - rounds corners and edges.",
        "common_uses": [
            "Smoothing low-poly models",
            "Organic/character shapes",
            "Production-quality surfaces"
        ],
        "pitfalls": [
            "Shrinks mesh toward center slightly",
            "Level 2 usually sufficient, 3+ for final render only",
            "Use Edge Crease to preserve sharp edges"
        ],
        "commonly_used_with": [
            ("Set Shade Smooth", "combined for full smoothness"),
            ("Edge Crease", "keep specific edges sharp"),
            ("Bevel Mesh", "add edge loops for sharpness"),
            ("Cube", "smooth into sphere-like shape")
        ],
        "example": "Low-poly cube + Level 2 subdivision = rounded box. Add supporting edge loops near corners to keep them sharper. Crease edges to 1.0 for perfectly sharp."
    },
    
    "GeometryNodeTriangulate": {
        "display_name": "Triangulate",
        "category": "Mesh Operations",
        "description": "Converts all faces to triangles - required for game engines and some operations.",
        "common_uses": [
            "Game engine export prep",
            "3D printing requirements",
            "Pre-Dual Mesh conversion"
        ],
        "pitfalls": [
            "Destroys quad topology permanently",
            "Quad Method affects diagonal placement",
            "Apply as late as possible in pipeline"
        ],
        "commonly_used_with": [
            ("Dual Mesh", "triangulate first for hexagon pattern"),
            ("Export formats", "game-ready output"),
            ("Set Shade Smooth", "improve shading after"),
            ("Decimate", "reduce triangle count after")
        ],
        "example": "Quad Method Beauty for best appearance, Shortest Diagonal for consistency. Game engines triangulate anyway - doing it yourself gives more control over the result."
    },
    
    "GeometryNodeDualMesh": {
        "display_name": "Dual Mesh",
        "category": "Mesh Operations",
        "description": "Swaps vertices and faces topologically - triangles become hexagons, cubes become octahedra.",
        "common_uses": [
            "Hexagonal tile patterns",
            "Voronoi-style cells",
            "Soccer ball from Ico Sphere"
        ],
        "pitfalls": [
            "Input must be manifold (closed, no loose edges)",
            "Works best on triangulated meshes",
            "Open meshes give unpredictable results"
        ],
        "commonly_used_with": [
            ("Triangulate", "prepare for hex pattern"),
            ("Ico Sphere", "geodesic dome patterns"),
            ("Grid + Triangulate", "honeycomb floor"),
            ("Extrude Mesh", "add depth to cells")
        ],
        "example": "Hexagonal tiles: Grid → Triangulate → Dual Mesh. Soccer ball: Ico Sphere (subdivisions 2) → Dual Mesh gives pentagons and hexagons."
    },
    
    "GeometryNodeExtrudeMesh": {
        "display_name": "Extrude Mesh",
        "category": "Mesh Operations",
        "description": "Pushes faces/edges/vertices outward, creating new connecting geometry - core modeling operation.",
        "common_uses": [
            "3D text from flat curves",
            "Building shapes from footprints",
            "City skyline generation"
        ],
        "pitfalls": [
            "Mode: Faces (most common), Edges (ribbon), Vertices (spikes)",
            "Individual mode: each element extrudes separately",
            "Offset Scale: negative values invert direction"
        ],
        "commonly_used_with": [
            ("Scale Elements", "inset before extruding"),
            ("Random Value", "varied extrusion heights"),
            ("Selection", "extrude specific faces only"),
            ("Normal", "extrusion direction")
        ],
        "example": "City blocks: Grid → random Face selection → Extrude with Random heights. Panel details: Scale Elements to 0.9 first (inset), then Extrude inward (negative offset)."
    },
    
    # ==========================================================================
    # GEOMETRY OPERATION NODES
    # ==========================================================================
    
    "GeometryNodeSetPosition": {
        "display_name": "Set Position",
        "category": "Geometry Operations",
        "description": "Moves points/vertices - the primary deformation tool for procedural effects.",
        "common_uses": [
            "Terrain heightmap displacement",
            "Wave/ripple animation",
            "Noise-based deformation"
        ],
        "pitfalls": [
            "Position input = absolute location (replaces)",
            "Offset input = relative movement (adds)",
            "Selection filters which elements move"
        ],
        "commonly_used_with": [
            ("Position", "read current location for math"),
            ("Normal", "push along surface direction"),
            ("Noise Texture", "procedural displacement values"),
            ("Vector Math", "calculate movement vectors")
        ],
        "example": "Terrain: (Normal × Noise × Height) as Offset pushes vertices up/down along surface. Wave: sin(Position.X + Time) × Amplitude as Z offset."
    },
    
    "GeometryNodeJoinGeometry": {
        "display_name": "Join Geometry",
        "category": "Geometry Operations",
        "description": "Combines multiple geometry streams into one output - keeps elements separate (no welding).",
        "common_uses": [
            "Combining procedural parts",
            "Merging parallel branches",
            "Assembling multi-piece models"
        ],
        "pitfalls": [
            "Vertices stay separate - overlaps don't weld",
            "Use Merge by Distance afterward to weld",
            "Attribute name conflicts use first input's value"
        ],
        "commonly_used_with": [
            ("Transform Geometry", "position parts before joining"),
            ("Merge by Distance", "weld overlapping vertices"),
            ("Realize Instances", "convert instances before joining"),
            ("Set Material", "assign materials before joining")
        ],
        "example": "Building a tree: create trunk, create leaves separately, Join Geometry to combine. Parts coexist but don't merge - like items in the same container."
    },
    
    "GeometryNodeTransform": {
        "display_name": "Transform Geometry",
        "category": "Geometry Operations",
        "description": "Applies translation, rotation, and scale to entire geometry uniformly.",
        "common_uses": [
            "Positioning generated primitives",
            "Matching another object's transform",
            "Pre-join positioning"
        ],
        "pitfalls": [
            "Affects ALL input geometry uniformly",
            "Rotation expects radians (multiply degrees by π/180)",
            "Order: Scale first, then Rotate, then Translate"
        ],
        "commonly_used_with": [
            ("Object Info", "copy another object's transform"),
            ("Combine XYZ", "build transform vectors"),
            ("Math (Radians)", "convert degrees to radians"),
            ("Join Geometry", "position before combining")
        ],
        "example": "Position generated cube: Translation (5, 0, 2). Rotate 45° around Z: Rotation (0, 0, 0.785). Different from Set Position which moves points individually."
    },
    
    "GeometryNodeSeparateGeometry": {
        "display_name": "Separate Geometry",
        "category": "Geometry Operations",
        "description": "Splits geometry into two outputs based on selection - selected vs unselected.",
        "common_uses": [
            "Different materials for top/bottom",
            "Process selected parts differently",
            "Split by attribute threshold"
        ],
        "pitfalls": [
            "Domain must match your selection (Point/Face/Edge)",
            "Selection output = True elements",
            "Inverted output = False elements"
        ],
        "commonly_used_with": [
            ("Compare", "create selection from values"),
            ("Position", "split by height/location"),
            ("Normal", "split by face direction"),
            ("Join Geometry", "recombine after processing")
        ],
        "example": "Two-tone object: Position.Z > 0.5 as selection. Top half to Selection output (red material), bottom to Inverted output (blue material), Join Geometry to recombine."
    },
    
    "GeometryNodeDeleteGeometry": {
        "display_name": "Delete Geometry",
        "category": "Geometry Operations",
        "description": "Removes elements matching selection criteria - procedural eraser.",
        "common_uses": [
            "Distance-based culling",
            "Random hole creation",
            "Threshold-based removal"
        ],
        "pitfalls": [
            "Domain must match selection type (Point/Face/Edge)",
            "Selection True = delete, False = keep",
            "Mode affects connected geometry handling"
        ],
        "commonly_used_with": [
            ("Compare", "threshold-based selection"),
            ("Random Value", "random deletion"),
            ("Position + Distance", "proximity culling"),
            ("Face Area", "remove tiny faces")
        ],
        "example": "Cull distant objects: Position distance from origin > 100 → Delete. Random holes: Random Value < 0.1 → Delete faces. Clean tiny faces: Face Area < 0.001 → Delete."
    },
    
    "GeometryNodeMergeByDistance": {
        "display_name": "Merge by Distance",
        "category": "Geometry Operations",
        "description": "Welds vertices within distance threshold - essential cleanup for joined/boolean geometry.",
        "common_uses": [
            "Post-Join Geometry welding",
            "Boolean operation cleanup",
            "Duplicate vertex removal"
        ],
        "pitfalls": [
            "Distance too large = mesh collapse disaster",
            "Start tiny (0.0001), increase if needed",
            "Mode: All vs Selection-limited"
        ],
        "commonly_used_with": [
            ("Join Geometry", "weld seams after combining"),
            ("Realize Instances", "merge instance boundaries"),
            ("Mesh Boolean", "cleanup intersection artifacts"),
            ("Import nodes", "fix duplicate vertices")
        ],
        "example": "After Boolean: try 0.0001m first, slowly increase if gaps remain. After Join: merge where parts should connect. Never start with large values - mesh can collapse into single point."
    },
    
    # ==========================================================================
    # INPUT NODES
    # ==========================================================================
    
    "GeometryNodeInputPosition": {
        "display_name": "Position",
        "category": "Input",
        "description": "Reads XYZ coordinates of each element - the foundation of location-based effects.",
        "common_uses": [
            "Height-based coloring/selection",
            "Distance calculations",
            "Texture coordinate source"
        ],
        "pitfalls": [
            "Returns world-space Vector (X,Y,Z)",
            "Use Separate XYZ for individual axes",
            "Updates if geometry moves"
        ],
        "commonly_used_with": [
            ("Separate XYZ", "extract single axis"),
            ("Set Position", "read then modify"),
            ("Noise Texture", "procedural coordinate input"),
            ("Vector Math (Length)", "distance from origin")
        ],
        "example": "Select high points: Separate XYZ → Z → Compare (> 5). Gradient by height: Z position → Map Range → Color Ramp. Most-used input node."
    },
    
    "GeometryNodeInputNormal": {
        "display_name": "Normal",
        "category": "Input",
        "description": "Reads surface direction at each point - which way the face points outward.",
        "common_uses": [
            "Push geometry along surface",
            "Select upward/downward faces",
            "Instance orientation"
        ],
        "pitfalls": [
            "Normalized vector (length always 1)",
            "Smooth shading interpolates normals",
            "Points need mesh context for normals"
        ],
        "commonly_used_with": [
            ("Set Position", "displace along surface"),
            ("Align Euler to Vector", "orient instances to surface"),
            ("Vector Math (Dot)", "measure facing direction"),
            ("Compare", "select by orientation")
        ],
        "example": "Select flat tops: Normal · (0,0,1) > 0.9 selects near-horizontal faces. Inflate mesh: Normal × 0.1 as Set Position offset pushes everything outward."
    },
    
    "GeometryNodeInputIndex": {
        "display_name": "Index",
        "category": "Input",
        "description": "Returns element number (0,1,2,3...) - unique ID per vertex/face/point for patterns.",
        "common_uses": [
            "Checkerboard selection (modulo 2)",
            "Gradient across elements",
            "Sequential numbering"
        ],
        "pitfalls": [
            "Starts at 0, not 1",
            "Changes if topology changes (use ID for stability)",
            "Different index spaces per domain"
        ],
        "commonly_used_with": [
            ("Math (Modulo)", "every Nth pattern"),
            ("Map Range", "normalize to 0-1"),
            ("Random Value", "as seed for consistent randomness"),
            ("Compare", "select index range")
        ],
        "example": "Checkerboard: Index % 2 = 0 selects even elements. Gradient: Index ÷ Domain Size → 0-1 range. Use as Random Value seed for stable per-element randomness."
    },
    
    # ==========================================================================
    # CURVE NODES
    # ==========================================================================
    
    "GeometryNodeCurvePrimitiveLine": {
        "display_name": "Curve Line",
        "category": "Curve Primitives",
        "description": "Creates a straight 2-point curve - foundation for paths, tubes, and cables.",
        "common_uses": [
            "Pipe/cable starting paths",
            "Direction vectors",
            "Simple connectors"
        ],
        "pitfalls": [
            "Only 2 control points - use Resample for more",
            "Points Mode: explicit start/end positions",
            "Direction Mode: start point + direction + length"
        ],
        "commonly_used_with": [
            ("Curve to Mesh", "create tube geometry"),
            ("Resample Curve", "add intermediate points"),
            ("Set Position", "bend into shape"),
            ("Set Curve Radius", "vary thickness along length")
        ],
        "example": "Cable between two points: Curve Line (Points mode) → Resample (20 points) → apply gravity with Set Position → Curve to Mesh with Circle profile."
    },
    
    "GeometryNodeCurvePrimitiveCircle": {
        "display_name": "Curve Circle",
        "category": "Curve Primitives",
        "description": "Creates a circular curve - essential as tube profile or ring path.",
        "common_uses": [
            "Pipe/tube cross-section profile",
            "Circular motion paths",
            "Ring and hoop shapes"
        ],
        "pitfalls": [
            "Resolution: 8 = octagon, 32+ = smooth circle",
            "Radius Mode vs Points Mode (through 3 points)",
            "Not filled - just outline (use Fill Curve)"
        ],
        "commonly_used_with": [
            ("Curve to Mesh", "as Profile for round tubes"),
            ("Fill Curve", "create solid disc"),
            ("Curve to Points", "evenly spaced circular arrangement"),
            ("Trim Curve", "partial arc from circle")
        ],
        "example": "Round pipe: Curve Line as path, Curve Circle (radius 0.1) as Curve to Mesh profile. Ring of objects: Curve Circle → Curve to Points → Instance on Points."
    },
    
    "GeometryNodeCurveToMesh": {
        "display_name": "Curve to Mesh",
        "category": "Curve Operations",
        "description": "Sweeps a profile shape along a curve path - creates tubes, pipes, ribbons, moldings.",
        "common_uses": [
            "Pipes and cables",
            "Rope and vines",
            "Architectural moldings"
        ],
        "pitfalls": [
            "No Profile = flat ribbon",
            "Circle Profile = round tube",
            "Fill Caps closes tube ends"
        ],
        "commonly_used_with": [
            ("Curve Circle", "round tube profile"),
            ("Set Curve Radius", "varies tube thickness along path"),
            ("Resample Curve", "smoother mesh output"),
            ("Set Curve Tilt", "twists profile along path")
        ],
        "example": "Rope: Curve path + Circle profile (small radius) + Fill Caps. Tapered tentacle: Set Curve Radius from 1→0.1 using Spline Parameter, then Curve to Mesh."
    },
    
    "GeometryNodeFillCurve": {
        "display_name": "Fill Curve",
        "category": "Curve Operations",
        "description": "Creates mesh face(s) from closed curves - like filling outlines with solid color.",
        "common_uses": [
            "2D shapes to mesh",
            "Text/logo solid fills",
            "Floor plans to geometry"
        ],
        "pitfalls": [
            "Curve MUST be closed (cyclic)",
            "Self-intersecting curves fail",
            "Inner curves become holes (like letter O)"
        ],
        "commonly_used_with": [
            ("String to Curves", "solid text"),
            ("Curve Circle", "filled disc"),
            ("Extrude Mesh", "add thickness after"),
            ("Quadrilateral", "filled rectangle")
        ],
        "example": "3D text: String to Curves → Fill Curve → Extrude Mesh (0.1 height). Logo: import SVG curve → Fill Curve → Solidify. Nested curves automatically become holes."
    },
    
    "GeometryNodeResampleCurve": {
        "display_name": "Resample Curve",
        "category": "Curve Operations",
        "description": "Redistributes control points along curve - controls density and spacing.",
        "common_uses": [
            "Even point distribution",
            "Smooth curve conversion",
            "Instance spacing control"
        ],
        "pitfalls": [
            "Count Mode: exact number of points",
            "Length Mode: points every N units",
            "Evaluated Mode: uses curve's native resolution"
        ],
        "commonly_used_with": [
            ("Curve to Points", "evenly spaced instances"),
            ("Set Position", "deform with consistent density"),
            ("Curve to Mesh", "smoother tube output"),
            ("Trim Curve", "before for consistent results")
        ],
        "example": "Fence posts every 2 meters: Resample (Length mode, 2.0) → Curve to Points → Instance posts. Chain links: high Count for smooth drape physics."
    },
    
    # ==========================================================================
    # MATH & UTILITY NODES
    # ==========================================================================
    
    "ShaderNodeMath": {
        "display_name": "Math",
        "category": "Utilities",
        "description": "Performs mathematical operations on values - the universal calculator node.",
        "common_uses": [
            "Arithmetic (add, multiply, power)",
            "Trigonometry (sin, cos for waves)",
            "Logic (greater than, modulo for patterns)"
        ],
        "pitfalls": [
            "Trig functions use radians (π = 180°)",
            "Divide by zero returns 0, not error",
            "Clamp checkbox limits output to 0-1"
        ],
        "commonly_used_with": [
            ("Map Range", "chain for complex remapping"),
            ("Separate XYZ", "math on individual axes"),
            ("Scene Time", "animated calculations"),
            ("Compare", "threshold comparisons")
        ],
        "example": "Wave motion: sin(Position.X × frequency + Time) × amplitude. Checkerboard: floor(X) + floor(Y) then Modulo 2. Exponential falloff: Power(distance, -2)."
    },
    
    "ShaderNodeVectorMath": {
        "display_name": "Vector Math",
        "category": "Utilities",
        "description": "Performs operations on XYZ vectors - essential for 3D position and direction calculations.",
        "common_uses": [
            "Distance and length calculations",
            "Direction normalization",
            "Position offsets and scaling"
        ],
        "pitfalls": [
            "Dot Product returns float (not vector)",
            "Cross Product: order matters (A×B ≠ B×A)",
            "Normalize of zero vector = zero (not error)"
        ],
        "commonly_used_with": [
            ("Position", "position arithmetic"),
            ("Normal", "direction calculations"),
            ("Combine/Separate XYZ", "component access"),
            ("Object Info", "target direction math")
        ],
        "example": "Distance to point: Subtract positions → Length. Direction toward target: Subtract → Normalize. Perpendicular vector: Cross Product with up vector (0,0,1)."
    },
    
    "FunctionNodeRandomValue": {
        "display_name": "Random Value",
        "category": "Utilities",
        "description": "Generates random numbers per element - controlled chaos for natural variation.",
        "common_uses": [
            "Instance scale/rotation variation",
            "Random point selection",
            "Jitter and offset noise"
        ],
        "pitfalls": [
            "Same Seed = identical random sequence",
            "Use ID (not Index) for stable randomness",
            "ID input determines per-element variation"
        ],
        "commonly_used_with": [
            ("Index", "as ID for per-element random"),
            ("Scale/Rotate Instances", "variation values"),
            ("Compare", "random selection threshold"),
            ("Set Position", "position jitter")
        ],
        "example": "Natural forest: Scale Instances with Random (0.7 to 1.3). Random 10% selection: Random Float → Compare (< 0.1). Stable random: use ID node as Seed, not Index."
    },
    
    "ShaderNodeMapRange": {
        "display_name": "Map Range",
        "category": "Utilities",
        "description": "Converts values from one range to another - the universal normalizer and scaler.",
        "common_uses": [
            "Normalize to 0-1 range",
            "Scale noise output",
            "Invert values (flip min/max)"
        ],
        "pitfalls": [
            "From Min/Max = input range to expect",
            "To Min/Max = output range to produce",
            "Clamp prevents overshoot outside range"
        ],
        "commonly_used_with": [
            ("Noise Texture", "rescale 0-1 to useful range"),
            ("Attribute Statistic", "get actual min/max"),
            ("Position", "height-based gradients"),
            ("Random Value", "adjust random range")
        ],
        "example": "Noise to displacement: From 0,1 To -0.5,0.5 centers the noise. Invert: From 0,1 To 1,0 flips values. Height gradient: Position.Z with known min/max → 0-1."
    },
    
    "FunctionNodeCompare": {
        "display_name": "Compare",
        "category": "Utilities",
        "description": "Tests if values meet conditions - outputs true/false for selections and logic.",
        "common_uses": [
            "Height-based selection",
            "Distance threshold filtering",
            "Value range checks"
        ],
        "pitfalls": [
            "Output is Boolean (true/false, or 1/0)",
            "Epsilon adds tolerance for float equality",
            "Mode must match data type"
        ],
        "commonly_used_with": [
            ("Delete Geometry", "conditional removal"),
            ("Separate Geometry", "split by condition"),
            ("Switch", "conditional value selection"),
            ("Boolean Math", "combine multiple conditions")
        ],
        "example": "Select high points: Position.Z → Compare (Greater Than, 5.0). Distance culling: Length(Position) → Compare (Less Than, 10). Combine with Boolean Math AND/OR for complex conditions."
    },
    
    "GeometryNodeSwitch": {
        "display_name": "Switch",
        "category": "Utilities",
        "description": "Chooses between two inputs based on true/false condition - if/else logic.",
        "common_uses": [
            "Toggle between geometries",
            "Conditional value selection",
            "User-controllable options"
        ],
        "pitfalls": [
            "False = first input, True = second input",
            "Both inputs evaluate (performance consideration)",
            "Type dropdown must match your data"
        ],
        "commonly_used_with": [
            ("Compare", "generate the boolean condition"),
            ("Group Input", "user toggle control"),
            ("Random Value (Boolean)", "random switching"),
            ("Boolean Math", "combined conditions")
        ],
        "example": "LOD system: Compare distance < 10 → Switch between high-poly and low-poly. Material variation: Random Boolean → Switch between two materials per face."
    },
    
    "GeometryNodeObjectInfo": {
        "display_name": "Object Info",
        "category": "Input",
        "description": "Pulls data from another scene object - transform, geometry, or both.",
        "common_uses": [
            "Target tracking (look-at)",
            "Copy another object's geometry",
            "Reference external transforms"
        ],
        "pitfalls": [
            "Object picker must reference valid scene object",
            "As Instance: efficient copy, Original: full mesh",
            "Transform Space: relative vs absolute"
        ],
        "commonly_used_with": [
            ("Vector Math", "calculate direction to object"),
            ("Instance on Points", "instance the object"),
            ("Transform Geometry", "apply object's transform"),
            ("Raycast", "use object as target")
        ],
        "example": "Objects follow Empty: Object Info → Location used in Set Position math. Import model: As Instance = False to get actual geometry. Reference transform: use Location/Rotation/Scale outputs."
    },
    
    "GeometryNodeCollectionInfo": {
        "display_name": "Collection Info",
        "category": "Input",
        "description": "Imports geometry from all objects in a collection - essential for varied scatter systems.",
        "common_uses": [
            "Multi-object random scattering",
            "Asset library instancing",
            "Varied vegetation/debris"
        ],
        "pitfalls": [
            "Separate Children: each object becomes pickable instance",
            "Reset Children: ignores object transforms (recommended)",
            "Pick Instance mode requires Instance on Points"
        ],
        "commonly_used_with": [
            ("Instance on Points", "Pick Instance for variety"),
            ("Random Value", "Instance Index for random selection"),
            ("Realize Instances", "convert to real geometry"),
            ("Scale/Rotate Instances", "add variation")
        ],
        "example": "Mixed forest: Collection with oak, pine, birch → Instance on Points with Pick Instance enabled. Random Value (Integer, 0 to object count-1) as Instance Index. Each point randomly gets one tree type."
    },
    
    "GeometryNodeSetMaterial": {
        "display_name": "Set Material",
        "category": "Material",
        "description": "Assigns a material to geometry - required for proper rendering.",
        "common_uses": [
            "Apply material to generated geometry",
            "Multi-material setups",
            "Conditional material by selection"
        ],
        "pitfalls": [
            "Material must exist in .blend file",
            "Selection: which faces receive the material",
            "Later Set Material nodes override earlier ones"
        ],
        "commonly_used_with": [
            ("Random Value", "random material per face"),
            ("Compare/Position", "height-based materials"),
            ("Separate Geometry", "different materials per part"),
            ("Switch", "toggle between materials")
        ],
        "example": "Two-tone: Separate by Z > 0.5, Set Material (red) on top, Set Material (blue) on bottom, Join Geometry. Random faces: Random Boolean as Selection for spotted pattern."
    },
    
    "ShaderNodeTexNoise": {
        "display_name": "Noise Texture",
        "category": "Texture",
        "description": "Generates smooth, organic random patterns - the workhorse of procedural texturing.",
        "common_uses": [
            "Terrain heightmaps",
            "Surface imperfections",
            "Displacement sources"
        ],
        "pitfalls": [
            "Scale: higher = smaller pattern features",
            "Detail: more octaves = more cost",
            "Output is 0-1, often needs Map Range"
        ],
        "commonly_used_with": [
            ("Position", "3D texture coordinates"),
            ("Map Range", "rescale output range"),
            ("Set Position", "displacement"),
            ("Color Ramp", "control contrast/colors")
        ],
        "example": "Terrain: Scale 2 (large hills), Detail 10, Roughness 0.5. Map Range from 0,1 to -1,1 for centered displacement. Animate with W input + Time for flowing effect."
    },
    
    "ShaderNodeMix": {
        "display_name": "Mix",
        "category": "Utilities",
        "description": "Blends between two inputs based on factor - the universal interpolation node.",
        "common_uses": [
            "Color/value transitions",
            "Smooth morphing between states",
            "Weighted combinations"
        ],
        "pitfalls": [
            "Factor 0 = A only, Factor 1 = B only",
            "Factor > 1 or < 0 extrapolates beyond inputs",
            "Clamp Factor prevents overshoot"
        ],
        "commonly_used_with": [
            ("Noise Texture", "organic blend factor"),
            ("Map Range", "create gradient factor"),
            ("Compare", "hard switch (0 or 1)"),
            ("Scene Time", "animated transitions")
        ],
        "example": "Height-based color: Position.Z → Map Range (0-1) as Factor, blend grass green to rock brown. Fade in: Time → Clamp (0-1) as Factor. Can mix floats, vectors, or colors."
    },
    
    "ShaderNodeClamp": {
        "display_name": "Clamp",
        "category": "Utilities",
        "description": "Restricts value to min/max bounds - prevents out-of-range values.",
        "common_uses": [
            "Prevent negative values",
            "Limit to 0-1 range",
            "Sanitize calculated values"
        ],
        "pitfalls": [
            "Min-Max mode: specify both bounds",
            "Range mode: auto-handles reversed min/max",
            "For vectors, clamp each component separately"
        ],
        "commonly_used_with": [
            ("Math", "limit calculation results"),
            ("Noise Texture", "constrain output range"),
            ("Random Value", "ensure valid range"),
            ("Map Range", "has built-in Clamp option")
        ],
        "example": "No negatives: Clamp (min 0, max 999999). Force 0-1: Clamp (0, 1). Note: Math node also has Clamp checkbox for simpler cases."
    },
    
    "FunctionNodeBooleanMath": {
        "display_name": "Boolean Math",
        "category": "Utilities",
        "description": "Logic operations on true/false values - AND, OR, NOT, XOR for combining conditions.",
        "common_uses": [
            "Combine multiple selections",
            "Invert selection (NOT)",
            "Complex conditional logic"
        ],
        "pitfalls": [
            "AND: both must be true",
            "OR: at least one true",
            "XOR: exactly one true (not both)",
            "NOT: inverts single input"
        ],
        "commonly_used_with": [
            ("Compare", "generate boolean inputs"),
            ("Delete Geometry", "combined selection"),
            ("Switch", "combined condition"),
            ("Separate Geometry", "complex filtering")
        ],
        "example": "Select middle band: (Z > 2) AND (Z < 5). Exclude edges: selection AND (NOT edge_selection). Either condition: condition_A OR condition_B."
    },
    
    "ShaderNodeSeparateXYZ": {
        "display_name": "Separate XYZ",
        "category": "Utilities",
        "description": "Splits vector into individual X, Y, Z float components.",
        "common_uses": [
            "Extract height (Z) from position",
            "Single-axis operations",
            "Axis-based selection"
        ],
        "pitfalls": [
            "Output: three separate floats",
            "Use Combine XYZ to reassemble",
            "Works on any vector (position, normal, color)"
        ],
        "commonly_used_with": [
            ("Position", "get individual coordinates"),
            ("Combine XYZ", "reassemble after modification"),
            ("Math", "operate on single axis"),
            ("Compare", "axis-based threshold")
        ],
        "example": "Height-based effect: Position → Separate XYZ → Z component. Flatten to ground: Separate, set Z=0, Combine XYZ → Set Position."
    },
    
    "ShaderNodeCombineXYZ": {
        "display_name": "Combine XYZ",
        "category": "Utilities",
        "description": "Assembles three floats into a single vector - reverse of Separate XYZ.",
        "common_uses": [
            "Build custom position/direction",
            "Reconstruct modified vector",
            "Create offset vectors"
        ],
        "pitfalls": [
            "Unconnected inputs = 0",
            "Order: X, Y, Z (not configurable)",
            "Output is always Vector type"
        ],
        "commonly_used_with": [
            ("Separate XYZ", "modify then recombine"),
            ("Math", "calculate components"),
            ("Set Position", "apply custom position"),
            ("Transform Geometry", "translation vector")
        ],
        "example": "Move only in Z: Combine XYZ (X=0, Y=0, Z=offset) as Set Position Offset. Custom direction: Combine computed X, Y, Z values into vector."
    },
    
    "GeometryNodeInputID": {
        "display_name": "ID",
        "category": "Input",
        "description": "Returns stable unique identifier per element - survives geometry operations unlike Index.",
        "common_uses": [
            "Stable random seed",
            "Track elements through modifications",
            "Consistent per-element values"
        ],
        "pitfalls": [
            "Not sequential (may have gaps)",
            "New geometry gets new IDs",
            "Use Set ID to assign custom IDs"
        ],
        "commonly_used_with": [
            ("Random Value", "stable random using ID as seed"),
            ("Compare", "select specific ID"),
            ("Set ID", "assign custom stable IDs"),
            ("Store Named Attribute", "preserve through operations")
        ],
        "example": "Stable random: use ID (not Index) as Random Value seed - randomness stays consistent even if element order changes. Track particles: ID persists through simulation frames."
    },
    
    "FunctionNodeInputInt": {
        "display_name": "Integer",
        "category": "Input",
        "description": "Whole number input - for counts, indices, seeds, and subdivision levels.",
        "common_uses": [
            "Instance/copy counts",
            "Subdivision levels",
            "Random seed values"
        ],
        "pitfalls": [
            "No decimal values (use Value for floats)",
            "Negative integers allowed",
            "In Group: becomes integer slider in modifier"
        ],
        "commonly_used_with": [
            ("Resample Curve", "point count"),
            ("Subdivide Mesh", "subdivision level"),
            ("Random Value", "seed input"),
            ("Repeat Zone", "iteration count")
        ],
        "example": "Copy count parameter: Integer → Duplicate Elements Amount. Seed control: Integer → Random Value Seed (change to get different random results)."
    },
    
    "FunctionNodeInputVector": {
        "display_name": "Vector",
        "category": "Input",
        "description": "XYZ vector input - for directions, offsets, and 3-component values.",
        "common_uses": [
            "Translation offset",
            "Direction vector",
            "Non-uniform scale"
        ],
        "pitfalls": [
            "All 3 components always present",
            "Not automatically normalized",
            "In Group: becomes XYZ fields in modifier"
        ],
        "commonly_used_with": [
            ("Set Position (Offset)", "translation amount"),
            ("Transform Geometry", "translation/scale"),
            ("Vector Math (Normalize)", "if direction needed"),
            ("Scale Instances", "non-uniform scale")
        ],
        "example": "Offset control: Vector (0, 0, 1) → Set Position Offset = move up. Direction parameter: Vector → Normalize → use as direction. Scale axis: Vector (1, 1, 2) stretches Z."
    },
    
    "FunctionNodeInputBool": {
        "display_name": "Boolean",
        "category": "Input",
        "description": "True/false toggle input - for on/off switches and conditions.",
        "common_uses": [
            "Feature toggle",
            "Mode switch",
            "Conditional behavior"
        ],
        "pitfalls": [
            "Only two states: True or False",
            "In Math: True=1, False=0",
            "In Group: becomes checkbox in modifier"
        ],
        "commonly_used_with": [
            ("Switch", "toggle between options"),
            ("Boolean Math", "combine conditions"),
            ("Delete Geometry", "as selection"),
            ("Compare", "generate from comparison")
        ],
        "example": "Mirror toggle: Boolean → Switch between normal and mirrored geometry. Enable detail: Boolean → Switch between low/high subdivision."
    },
    
    "GeometryNodeSceneTime": {
        "display_name": "Scene Time",
        "category": "Input",
        "description": "Outputs current frame number and seconds - the animation clock for geometry nodes.",
        "common_uses": [
            "Animated procedural effects",
            "Oscillating/pulsing motion",
            "Time-based noise evolution"
        ],
        "pitfalls": [
            "Seconds: continuous float (e.g., 1.5 at frame 36 @24fps)",
            "Frame: integer frame number",
            "Only updates on frame change (not realtime)"
        ],
        "commonly_used_with": [
            ("Math (Sine)", "oscillation: sin(Seconds × speed)"),
            ("Noise Texture W", "evolving noise"),
            ("Set Position", "animated movement"),
            ("Trim Curve", "growing curves over time")
        ],
        "example": "Bobbing motion: sin(Seconds × 2) × 0.5 as Z offset. Growing vine: Seconds / duration as Trim Curve end. Flowing noise: Seconds as Noise W input."
    },
    
    # ==========================================================================
    # ATTRIBUTE NODES
    # ==========================================================================
    
    "GeometryNodeCaptureAttribute": {
        "display_name": "Capture Attribute",
        "category": "Attribute",
        "description": "Snapshots field values before geometry changes - preserves data through transformations.",
        "common_uses": [
            "Store original positions pre-deformation",
            "Preserve Index before topology changes",
            "Cache expensive calculations"
        ],
        "pitfalls": [
            "Geometry MUST flow through this node",
            "Domain must match your use case",
            "Output is anonymous - use output socket, not name"
        ],
        "commonly_used_with": [
            ("Position", "capture before Set Position"),
            ("Index", "preserve numbering"),
            ("Noise Texture", "cache noise values"),
            ("Set Position", "reference original positions")
        ],
        "example": "Displacement with original UV: Capture Position → Set Position (displace) → use Captured Position for texture coordinates. Without capture, displaced Position would give stretched textures."
    },
    
    "GeometryNodeStoreNamedAttribute": {
        "display_name": "Store Named Attribute",
        "category": "Attribute",
        "description": "Saves custom data to geometry by name - bridges geometry nodes to materials.",
        "common_uses": [
            "Pass data to shader/material",
            "Custom vertex colors",
            "Persistent per-element data"
        ],
        "pitfalls": [
            "Name must match when reading",
            "Domain: Point, Face, Edge, etc.",
            "Data Type must match stored value"
        ],
        "commonly_used_with": [
            ("Named Attribute", "read it back"),
            ("Attribute node in shader", "access in material"),
            ("Position", "store position-based data"),
            ("Random Value", "persistent random")
        ],
        "example": "Wetness mask: Store Noise as 'wetness' (Float, Face domain). In material: Attribute node reads 'wetness' → Mix Shader between dry/wet materials. Data travels from geometry nodes to shader."
    },
    
    "GeometryNodeInputNamedAttribute": {
        "display_name": "Named Attribute",
        "category": "Attribute",
        "description": "Reads stored attribute by name - retrieves data from Store Named Attribute or imported geometry.",
        "common_uses": [
            "Read previously stored data",
            "Access vertex colors/UVs by name",
            "Retrieve custom per-element data"
        ],
        "pitfalls": [
            "Attribute must exist (check Spreadsheet)",
            "Data Type must match stored type",
            "Exists output: boolean if attribute found"
        ],
        "commonly_used_with": [
            ("Store Named Attribute", "create the attribute"),
            ("Spreadsheet Editor", "verify attribute exists"),
            ("Compare", "use in selections"),
            ("Material (Attribute node)", "access in shader")
        ],
        "example": "Read stored color: Named Attribute 'my_color' (Color type). Access UVs: Named Attribute 'UVMap' (Vector, Face Corner). Check Exists output to handle missing attributes."
    },
    
    "GeometryNodeAttributeStatistic": {
        "display_name": "Attribute Statistic",
        "category": "Attribute",
        "description": "Calculates min, max, mean, range, std dev across all elements - for normalization and analysis.",
        "common_uses": [
            "Auto-normalize to 0-1 range",
            "Find highest/lowest values",
            "Calculate averages"
        ],
        "pitfalls": [
            "Outputs are single values (not per-element)",
            "Domain: what elements to analyze",
            "Processes entire geometry (performance cost)"
        ],
        "commonly_used_with": [
            ("Map Range", "use Min/Max for normalization"),
            ("Position", "find geometry bounds"),
            ("Face Area", "find largest/smallest faces"),
            ("Value to String", "display statistics")
        ],
        "example": "Auto-normalize height: Attribute Statistic on Position.Z → Map Range (From: Min,Max To: 0,1). Now heights are 0-1 regardless of actual mesh size. Mean output gives center height."
    },
    
    "GeometryNodeAttributeDomainSize": {
        "display_name": "Domain Size",
        "category": "Attribute",
        "description": "Returns element counts per domain - vertices, edges, faces, splines, instances.",
        "common_uses": [
            "Get vertex/face count",
            "Normalize Index to 0-1",
            "Conditional logic by mesh complexity"
        ],
        "pitfalls": [
            "Separate outputs for each domain type",
            "Count changes as geometry is modified",
            "Use Component dropdown to select geometry type"
        ],
        "commonly_used_with": [
            ("Index", "Index ÷ Point Count = 0-1 gradient"),
            ("Compare", "check mesh size"),
            ("Math", "calculate ratios"),
            ("Value to String", "display counts")
        ],
        "example": "Index gradient: Index ÷ (Domain Size Point Count - 1) = 0-1 per vertex. Check face count: Domain Size Face Count > 1000 for LOD switching."
    },
    
    # ==========================================================================
    # ADDITIONAL COMMONLY USED NODES
    # ==========================================================================
    
    "GeometryNodeBoundBox": {
        "display_name": "Bounding Box",
        "category": "Geometry",
        "description": "Creates axis-aligned box containing geometry + outputs min/max corners.",
        "common_uses": [
            "Calculate geometry dimensions",
            "Collision/proxy boxes",
            "Normalize positions to 0-1"
        ],
        "pitfalls": [
            "Always axis-aligned (doesn't rotate with object)",
            "Min/Max: world-space corner positions",
            "Bounding Box output is actual mesh geometry"
        ],
        "commonly_used_with": [
            ("Vector Math (Subtract)", "calculate dimensions"),
            ("Map Range", "normalize position to bounds"),
            ("Transform Geometry", "center using (Min+Max)/2"),
            ("Math", "calculate center, size, diagonal")
        ],
        "example": "Get size: Max - Min = dimensions vector. Center geometry: translate by -(Min + Max)/2. Normalize to 0-1: Map Range Position from Min,Max to 0,1."
    },
    
    "GeometryNodeSampleIndex": {
        "display_name": "Sample Index",
        "category": "Geometry",
        "description": "Retrieves value from geometry at specific index - array-style data lookup.",
        "common_uses": [
            "Get value at specific element",
            "Transfer data between geometries",
            "Access neighbor/connected element data"
        ],
        "pitfalls": [
            "Index out of range: clamped or returns 0",
            "Domain must match data location",
            "Clamp checkbox prevents out-of-range"
        ],
        "commonly_used_with": [
            ("Index", "specify element number"),
            ("Math", "calculate index to sample"),
            ("Position", "commonly sampled value"),
            ("Domain Size", "get valid index range")
        ],
        "example": "Get vertex 0 position: Sample Index (Position, Index=0). Copy first point's color to all: Sample Index (color attribute, Index=0) → Store Named Attribute."
    },
    
    "GeometryNodeRaycast": {
        "display_name": "Raycast",
        "category": "Geometry",
        "description": "Casts rays to find surface intersections - for projection, collision, and snapping.",
        "common_uses": [
            "Project points onto surface",
            "Ground/floor detection",
            "Visibility and occlusion checks"
        ],
        "pitfalls": [
            "Is Hit: false when ray misses",
            "Ray Direction must be normalized for accurate distance",
            "Target must be mesh (not curves/points)"
        ],
        "commonly_used_with": [
            ("Object Info", "target surface geometry"),
            ("Normal", "common ray direction"),
            ("Set Position", "snap to Hit Position"),
            ("Switch", "handle hit vs miss cases")
        ],
        "example": "Drop objects to ground: Raycast downward (0,0,-1) to floor mesh → use Hit Position with Set Position. Check Is Hit before using results to handle misses."
    },
    
    "GeometryNodeProximity": {
        "display_name": "Geometry Proximity",
        "category": "Geometry",
        "description": "Finds closest point on target geometry - for snapping, distance effects, and attraction.",
        "common_uses": [
            "Snap to nearest surface",
            "Distance-based coloring/scaling",
            "Magnetic attraction effects"
        ],
        "pitfalls": [
            "Target Element: Points, Edges, or Faces",
            "Distance is always positive (use Position for direction)",
            "Performance scales with point count"
        ],
        "commonly_used_with": [
            ("Object Info", "target geometry source"),
            ("Map Range", "distance → useful range"),
            ("Set Position", "snap to Position output"),
            ("Color Ramp", "distance-based coloring")
        ],
        "example": "Shrink-wrap effect: Proximity (Target: surface mesh) → Mix Position with original using distance as factor. Objects near surface stick, far ones stay put."
    },
    
    "GeometryNodeSetShadeSmooth": {
        "display_name": "Set Shade Smooth",
        "category": "Mesh",
        "description": "Controls smooth vs flat shading per face - affects visual appearance without changing geometry.",
        "common_uses": [
            "Smooth organic surfaces",
            "Flat shading for hard-surface",
            "Mixed smooth/flat regions"
        ],
        "pitfalls": [
            "Only visual - doesn't change actual geometry",
            "Selection: which faces to affect",
            "Shade Smooth True = smooth, False = flat"
        ],
        "commonly_used_with": [
            ("Subdivision Surface", "usually wants smooth shading"),
            ("Edge Angle", "auto-select sharp edges"),
            ("Compare", "threshold-based smooth/flat"),
            ("Mesh Boolean", "results often need smoothing")
        ],
        "example": "Auto smooth: Edge Angle > 30° as Selection, Set Shade Smooth (False) on sharp edges. Everything else stays smooth, hard edges stay crisp."
    },
    
    "GeometryNodeConvexHull": {
        "display_name": "Convex Hull",
        "category": "Geometry",
        "description": "Creates smallest convex mesh enclosing all points - shrink-wrap around point cloud.",
        "common_uses": [
            "Collision shape generation",
            "Simplified bounding mesh",
            "Point cloud to surface"
        ],
        "pitfalls": [
            "Result is always convex (no concavities)",
            "Interior points don't affect result",
            "For concave, use Volume workflow instead"
        ],
        "commonly_used_with": [
            ("Distribute Points", "scattered points → hull"),
            ("Points to Vertices", "prepare point cloud"),
            ("Mesh Boolean", "combine with for complex shapes"),
            ("Set Shade Smooth", "smooth the result")
        ],
        "example": "Quick collision box: scatter points around complex object → Convex Hull = simplified collision mesh. For concave shapes, use Mesh to Volume → Volume to Mesh instead."
    },
    
    "GeometryNodeFlipFaces": {
        "display_name": "Flip Faces",
        "category": "Mesh",
        "description": "Reverses face normals - fixes inside-out geometry or creates intentional inversion.",
        "common_uses": [
            "Fix inverted normals",
            "Correct Boolean results",
            "Create inside-out effect"
        ],
        "pitfalls": [
            "Flipped faces may be invisible (backface culling)",
            "Selection controls which faces flip",
            "Affects shading, not geometry"
        ],
        "commonly_used_with": [
            ("Mesh Boolean", "results often need flipping"),
            ("Extrude Mesh", "inner faces may invert"),
            ("Normal", "check direction first (· Z)"),
            ("Join Geometry", "unified normal direction")
        ],
        "example": "Fix inside-out: Flip Faces (all). Selective fix: Normal · (0,0,1) < 0 as selection → Flip Faces. Only affects face orientation, not actual geometry."
    },
    
    "GeometryNodeScaleElements": {
        "display_name": "Scale Elements",
        "category": "Mesh",
        "description": "Scales faces/edges from their individual centers - inset effect without extrusion.",
        "common_uses": [
            "Create gaps between faces",
            "Inset preparation before extrude",
            "Per-face size variation"
        ],
        "pitfalls": [
            "Domain: Face or Edge",
            "Scale < 1 shrinks, > 1 expands",
            "Center: Individual (per-element) vs Uniform"
        ],
        "commonly_used_with": [
            ("Extrude Mesh", "Scale → Extrude for window frames"),
            ("Random Value", "varied scale per face"),
            ("Selection", "scale specific faces only"),
            ("Separate Geometry", "before for per-island scale")
        ],
        "example": "Panel inset: Scale Elements (0.9) → Extrude (inward). Tile gaps: Scale Elements (0.95) creates uniform gaps. Honeycomb: Scale Elements on hexagonal grid faces."
    },
    
    # ==========================================================================
    # MORE CURVE NODES
    # ==========================================================================
    
    "GeometryNodeSubdivideCurve": {
        "display_name": "Subdivide Curve",
        "category": "Curve Operations",
        "description": "Adds control points by splitting segments - doubles points per subdivision level.",
        "common_uses": [
            "More points for deformation",
            "Smoother Curve to Mesh output",
            "Preparation for noise displacement"
        ],
        "pitfalls": [
            "Cuts: 1 = double points, 2 = quadruple",
            "Different from Resample (subdivide vs redistribute)",
            "High cuts = exponential point increase"
        ],
        "commonly_used_with": [
            ("Set Position", "displace subdivided points"),
            ("Noise Texture", "add detail after subdivision"),
            ("Curve to Mesh", "smoother tube"),
            ("Set Curve Radius", "more radius control points")
        ],
        "example": "Add curve detail: Subdivide (Cuts 2) → Set Position with Noise. Different from Resample which redistributes existing shape; Subdivide adds points while preserving original positions."
    },
    
    "GeometryNodeTrimCurve": {
        "display_name": "Trim Curve",
        "category": "Curve Operations",
        "description": "Cuts curve to keep only a portion - essential for growth animations.",
        "common_uses": [
            "Animated curve growth",
            "Partial arc/segment",
            "Progress indicators"
        ],
        "pitfalls": [
            "Factor Mode: 0 = start, 1 = end",
            "Length Mode: actual scene units",
            "Start/End: define kept portion"
        ],
        "commonly_used_with": [
            ("Scene Time", "animate trim end"),
            ("Map Range", "control animation curve"),
            ("Curve to Mesh", "after trimming"),
            ("Spline Length", "get total for calculations")
        ],
        "example": "Growing vine: Start=0, End animated from 0→1 over time. Line drawing effect: same approach with Curve to Mesh. Factor 0.25 to 0.75 keeps middle half."
    },
    
    "GeometryNodeCurveToPoints": {
        "display_name": "Curve to Points",
        "category": "Curve Operations",
        "description": "Extracts points from curve with tangent/normal data - for instancing along paths.",
        "common_uses": [
            "Objects along curve path",
            "Fence posts/lights on path",
            "Particle-like effects from curves"
        ],
        "pitfalls": [
            "Count Mode: fixed number of points",
            "Length Mode: points every N units",
            "Evaluated: uses curve's native resolution"
        ],
        "commonly_used_with": [
            ("Instance on Points", "place objects"),
            ("Align Euler to Vector", "use Tangent for alignment"),
            ("Resample Curve", "control spacing first"),
            ("Rotate Instances", "orient along curve")
        ],
        "example": "Street lights: Curve to Points (Length=10m) → Instance on Points. Use Tangent output with Align Euler to Vector to orient lights along road direction."
    },
    
    "GeometryNodeSetCurveRadius": {
        "display_name": "Set Curve Radius",
        "category": "Curve Operations",
        "description": "Controls tube thickness per-point - affects Curve to Mesh profile scaling.",
        "common_uses": [
            "Tapered tubes/tentacles",
            "Variable rope thickness",
            "Organic branch shapes"
        ],
        "pitfalls": [
            "Only visible with Curve to Mesh + Profile",
            "Default radius is 1.0",
            "Needs multiple points for gradual change"
        ],
        "commonly_used_with": [
            ("Spline Parameter", "position-based taper"),
            ("Curve to Mesh", "visualize radius"),
            ("Map Range", "adjust taper curve"),
            ("Noise Texture", "organic irregularity")
        ],
        "example": "Tentacle: Spline Parameter (1→0.1 via Map Range) → Set Curve Radius → Curve to Mesh with Circle profile. Fat at base (1.0), thin at tip (0.1)."
    },
    
    "GeometryNodeCurveSetSplineType": {
        "display_name": "Set Spline Type",
        "category": "Curve Operations",
        "description": "Converts between curve types: Poly (sharp), Bezier (handles), Catmull-Rom (auto-smooth), NURBS.",
        "common_uses": [
            "Sharp corners (→ Poly)",
            "Smooth interpolation (→ Catmull-Rom)",
            "Handle control (→ Bezier)"
        ],
        "pitfalls": [
            "Poly: straight segments, no smoothing",
            "Bezier handle data lost when converting away",
            "NURBS needs many points for smooth result"
        ],
        "commonly_used_with": [
            ("Curve primitives", "change default type"),
            ("Resample Curve", "add points after conversion"),
            ("Fillet Curve", "round Poly corners"),
            ("Curve to Mesh", "different smoothing results")
        ],
        "example": "Sharp zigzag: create curve → Set Spline Type (Poly) = straight segments. Smooth path: → Catmull-Rom = auto-smooth through points without handles."
    },
    
    "GeometryNodeFilletCurve": {
        "display_name": "Fillet Curve",
        "category": "Curve Operations",
        "description": "Rounds sharp corners with smooth arcs - bevels for curves.",
        "common_uses": [
            "Rounded rectangle profiles",
            "Soft path corners",
            "Beveled architectural shapes"
        ],
        "pitfalls": [
            "Only works on Poly/Bezier curves",
            "Radius too large overlaps = artifacts",
            "Count: segments in rounded corner"
        ],
        "commonly_used_with": [
            ("Quadrilateral", "rounded rectangle"),
            ("Set Spline Type (Poly)", "prepare sharp corners"),
            ("Fill Curve", "solid rounded shape"),
            ("Curve to Mesh", "rounded tube profile")
        ],
        "example": "Rounded rectangle: Quadrilateral → Set Spline Type (Poly) → Fillet Curve (radius 0.1, count 4). Limit Radius prevents overlapping on small corners."
    },
    
    "GeometryNodeCurvePrimitiveBezierSegment": {
        "display_name": "Bezier Segment",
        "category": "Curve Primitives",
        "description": "Creates single bezier curve with handle control points - precise curve shaping.",
        "common_uses": [
            "S-curves and swoops",
            "Custom smooth paths",
            "Animation motion paths"
        ],
        "pitfalls": [
            "4 control points: start, handle1, handle2, end",
            "Position mode: absolute handle positions",
            "Offset mode: handles relative to endpoints"
        ],
        "commonly_used_with": [
            ("Curve to Mesh", "3D tube from curve"),
            ("Join Geometry", "connect multiple segments"),
            ("Resample Curve", "even point spacing"),
            ("Transform Geometry", "position curve")
        ],
        "example": "S-curve: Start (0,0,0), Handle Start (1,0,0), Handle End (-1,1,0), End (0,1,0). Adjust handles to control the bulge and flow of the curve."
    },
    
    "GeometryNodeCurvePrimitiveQuadrilateral": {
        "display_name": "Quadrilateral",
        "category": "Curve Primitives",
        "description": "Creates 4-sided curve shape - rectangle, rhombus, parallelogram, trapezoid, or kite.",
        "common_uses": [
            "Rectangular tube profiles",
            "Frame/border shapes",
            "Architectural trim cross-sections"
        ],
        "pitfalls": [
            "Mode: Rectangle, Diamond, Parallelogram, Trapezoid, Kite, Points",
            "Outline only - use Fill Curve for solid",
            "Points mode allows arbitrary 4 corners"
        ],
        "commonly_used_with": [
            ("Fill Curve", "solid rectangle"),
            ("Curve to Mesh", "square tube profile"),
            ("Fillet Curve", "rounded corners"),
            ("Extrude Mesh", "after Fill for 3D")
        ],
        "example": "Square tube: Quadrilateral (Rectangle) as Curve to Mesh profile. Rounded rectangle: add Fillet Curve before Fill. Diamond: use Diamond mode or rotate Rectangle 45°."
    },
    
    "GeometryNodeCurveArc": {
        "display_name": "Arc",
        "category": "Curve Primitives",
        "description": "Creates partial circle segment - by angle/radius or through 3 points.",
        "common_uses": [
            "Architectural arches",
            "Pie chart segments",
            "Rounded corner elements"
        ],
        "pitfalls": [
            "Radius mode: center + radius + sweep angle",
            "Points mode: fits arc through 3 positions",
            "Angles in radians (π = 180°)"
        ],
        "commonly_used_with": [
            ("Fill Curve", "pie slice shape"),
            ("Curve to Mesh", "3D arch"),
            ("Math (Radians)", "convert degrees"),
            ("Join Geometry", "combine with lines for pie")
        ],
        "example": "Quarter circle: Sweep Angle π/2 (90°). Pie slice: Arc + two Curve Lines from center to endpoints + Fill Curve. Semicircle: Sweep Angle π."
    },
    
    "GeometryNodeCurveSpiral": {
        "display_name": "Spiral",
        "category": "Curve Primitives",
        "description": "Creates spiral/helix curve - flat coil or 3D spring shape.",
        "common_uses": [
            "Springs and coils",
            "Spiral staircases",
            "DNA helix shapes"
        ],
        "pitfalls": [
            "Rotations: number of full turns",
            "Height: 0 = flat spiral, >0 = 3D helix",
            "Start/End Radius: controls growth"
        ],
        "commonly_used_with": [
            ("Curve to Mesh", "spring/coil tube"),
            ("Curve to Points", "objects along spiral"),
            ("Set Curve Radius", "tapered spring"),
            ("Trim Curve", "partial spiral")
        ],
        "example": "Spring: Rotations 10, Height 2, equal Start/End Radius → Curve to Mesh with Circle. Snail shell: Height 0, Start Radius 0, End Radius 1 (growing flat spiral)."
    },
    
    "GeometryNodeCurveStar": {
        "display_name": "Star",
        "category": "Curve Primitives",
        "description": "Creates star-shaped curve with alternating inner/outer radius points.",
        "common_uses": [
            "Star shapes",
            "Gear profiles",
            "Badge/medal outlines"
        ],
        "pitfalls": [
            "Points: number of star points (5 = classic)",
            "Inner < Outer Radius (or inverted star)",
            "Twist: rotates inner points for pinwheel effect"
        ],
        "commonly_used_with": [
            ("Fill Curve", "solid star"),
            ("Fillet Curve", "rounded points"),
            ("Curve to Mesh", "extruded star profile"),
            ("Transform Geometry", "rotate/scale")
        ],
        "example": "Classic 5-point star: Points 5, Outer 1.0, Inner 0.4. Sheriff badge: Points 6 or 7. Gear-like: many points, small inner/outer difference. Twist for spiral-arm effect."
    },
    
    # ==========================================================================
    # MORE TEXTURE NODES
    # ==========================================================================
    
    "ShaderNodeTexVoronoi": {
        "display_name": "Voronoi Texture",
        "category": "Texture",
        "description": "Creates cellular patterns from distance to random points - cracks, scales, cells.",
        "common_uses": [
            "Cracked mud/stone",
            "Cell/organic patterns",
            "Scales and skin textures"
        ],
        "pitfalls": [
            "Feature Output: Distance, Color, Position, or W",
            "Distance: gradient from cell center",
            "Randomness: 0 = grid, 1 = organic cells"
        ],
        "commonly_used_with": [
            ("Position", "3D coordinates"),
            ("Color Ramp", "threshold for cell edges"),
            ("Math (Less Than)", "sharp cell boundaries"),
            ("Set Position", "cellular displacement")
        ],
        "example": "Cracked earth: Distance output → Color Ramp with steep falloff near 0. Stone tiles: low Randomness + Smooth F1 mode. Cell centers: Position output gives each cell's center point."
    },
    
    "ShaderNodeTexGradient": {
        "display_name": "Gradient Texture",
        "category": "Texture",
        "description": "Creates simple gradient patterns - linear, radial, spherical, quadratic.",
        "common_uses": [
            "Distance falloffs",
            "Directional blends",
            "Simple masks"
        ],
        "pitfalls": [
            "Type: Linear, Quadratic, Easing, Diagonal, Spherical, Radial",
            "Output: 0-1 range (Fac) + Color",
            "Needs Position or UV as Vector input"
        ],
        "commonly_used_with": [
            ("Position", "world-space gradient"),
            ("Color Ramp", "custom color mapping"),
            ("Map Range", "adjust falloff"),
            ("Mix", "use as blend factor")
        ],
        "example": "Radial falloff: Gradient (Spherical) from object center. Linear wipe: Gradient (Linear) + animated threshold for reveal effect. Simplest procedural texture."
    },
    
    "ShaderNodeTexWave": {
        "display_name": "Wave Texture",
        "category": "Texture",
        "description": "Creates parallel bands or concentric rings - stripes, wood grain, ripples.",
        "common_uses": [
            "Wood grain texture",
            "Water ripples",
            "Contour lines"
        ],
        "pitfalls": [
            "Type: Bands (stripes) vs Rings (concentric)",
            "Profile: Sine, Saw, Triangle shapes",
            "Distortion adds organic irregularity"
        ],
        "commonly_used_with": [
            ("Position", "3D coordinates"),
            ("Color Ramp", "wood color variation"),
            ("Scene Time", "animated ripples"),
            ("Noise Texture", "add to Position for distortion")
        ],
        "example": "Wood grain: Bands + Saw profile + Scale 20 + Distortion 2. Animated ripples: Rings type, subtract Time from Scale for expanding waves."
    },
    
    "ShaderNodeTexMusgrave": {
        "display_name": "Musgrave Texture",
        "category": "Texture",
        "description": "Advanced fractal noise with terrain-specific algorithms - more control than Noise Texture.",
        "common_uses": [
            "Realistic terrain heightmaps",
            "Erosion/weathering patterns",
            "Complex organic surfaces"
        ],
        "pitfalls": [
            "Type: fBM, Multifractal, Ridged, Hybrid, Hetero",
            "More parameters = more tuning required",
            "Computationally heavier than Noise"
        ],
        "commonly_used_with": [
            ("Position", "3D coordinates"),
            ("Set Position", "terrain displacement"),
            ("Map Range", "control height range"),
            ("Noise Texture", "layer for detail")
        ],
        "example": "Mountain terrain: Ridged Multifractal (sharp peaks). Rolling hills: fBM. Eroded landscape: Hetero Terrain. Dimension ~2.0, Lacunarity ~2.0, Octaves 8+ for detail."
    },
    
    "ShaderNodeTexMagic": {
        "display_name": "Magic Texture",
        "category": "Texture",
        "description": "Generates hypnotic vortex patterns - unique psychedelic effects unavailable elsewhere.",
        "common_uses": [
            "Trippy/magical visuals",
            "Abstract art patterns",
            "Unique color distortions"
        ],
        "pitfalls": [
            "Outputs both Color AND Factor",
            "Depth: iteration count (higher = more complex)",
            "Distortion: twist intensity"
        ],
        "commonly_used_with": [
            ("Position", "coordinate input"),
            ("Color Ramp", "remap output palette"),
            ("Separate Color", "use channels individually"),
            ("Scene Time + W", "animate pattern")
        ],
        "example": "Basic swirl: Depth 2, Distortion 5, Scale 2. Complex chaos: Depth 5+, Distortion 10+. Animate: plug Time into W input for morphing pattern. Unique among textures - nothing else creates this effect."
    },
    
    "ShaderNodeTexChecker": {
        "display_name": "Checker Texture",
        "category": "Texture",
        "description": "Creates checkerboard pattern - alternating squares of two colors.",
        "common_uses": [
            "Chess/game boards",
            "UV test pattern",
            "Tile floors"
        ],
        "pitfalls": [
            "Only 2 colors (Color1, Color2)",
            "Scale affects square size",
            "Sharp edges (no anti-aliasing built-in)"
        ],
        "commonly_used_with": [
            ("Position", "3D checker pattern"),
            ("UV Map", "2D surface checker"),
            ("Color Ramp", "remap to custom colors"),
            ("Math (Floor)", "DIY checker with more control")
        ],
        "example": "Chess board: Scale 8 for 8×8 grid. UV test: any scale, helps visualize texture stretching. 3D checker: use Position for volumetric pattern."
    },
    
    "ShaderNodeTexBrick": {
        "display_name": "Brick Texture",
        "category": "Texture",
        "description": "Creates brick/tile pattern with mortar lines - staggered rows, customizable proportions.",
        "common_uses": [
            "Brick walls",
            "Tile floors",
            "Stone masonry"
        ],
        "pitfalls": [
            "Offset: row stagger amount (0.5 = standard brick)",
            "Mortar Size: gap between bricks",
            "Brick Width/Height: individual brick size"
        ],
        "commonly_used_with": [
            ("Position", "3D brick pattern"),
            ("Noise Texture", "color/displacement variation"),
            ("Bump", "mortar depth in shaders"),
            ("Color Ramp", "varied brick colors")
        ],
        "example": "Classic brick: Offset 0.5, Mortar 0.02, add Noise to Color1 for variation. Subway tile: Offset 0.5, wider bricks. Running bond: Offset 0.5, square bricks."
    },
    
    "ShaderNodeTexWhiteNoise": {
        "display_name": "White Noise Texture",
        "category": "Texture",
        "description": "Pure random values with no spatial pattern - TV static, not clouds.",
        "common_uses": [
            "Random seed generation",
            "Film grain/static",
            "Per-pixel randomness"
        ],
        "pitfalls": [
            "No smoothness or coherence (unlike Noise Texture)",
            "Dimension: 1D/2D/3D/4D input modes",
            "Outputs: Value (float) and Color (RGB)"
        ],
        "commonly_used_with": [
            ("Position", "spatially varying random"),
            ("Index", "per-element random"),
            ("Math", "scale and offset values"),
            ("Compare", "random threshold selection")
        ],
        "example": "Film grain: White Noise (small scale) × 0.05 + base color. Random per-face: use Index as W input for consistent per-element randomness. Different from Noise which has smooth variation."
    },
    
    "ShaderNodeTexImage": {
        "display_name": "Image Texture (Shader)",
        "category": "Texture",
        "description": "Samples image file in shader context - for materials, not geometry nodes.",
        "common_uses": [
            "Photo-based materials",
            "Diffuse/roughness/normal maps",
            "Decals and labels"
        ],
        "pitfalls": [
            "Needs UV coordinates (or Generated/Object)",
            "Color Space: sRGB for color, Non-Color for data",
            "Use GeometryNodeImageTexture for geometry nodes"
        ],
        "commonly_used_with": [
            ("Texture Coordinate", "UV/Generated/Object coordinates"),
            ("Mapping", "transform/tile/rotate UVs"),
            ("Normal Map", "for normal/bump textures"),
            ("Mix Shader", "blend texture-based materials")
        ],
        "example": "PBR workflow: Color Space sRGB for diffuse, Non-Color for roughness/normal. Projection: Generated for quick preview, UV for final."
    },
    
    # ==========================================================================
    # MESH OPERATIONS
    # ==========================================================================
    
    "GeometryNodeSplitEdges": {
        "display_name": "Split Edges",
        "category": "Mesh Operations",
        "description": "Disconnects faces at edges - each face gets its own vertices for independence.",
        "common_uses": [
            "Hard edge shading",
            "Explode effect preparation",
            "Per-face manipulation"
        ],
        "pitfalls": [
            "Increases vertex count (shared → individual)",
            "Selection controls which edges split",
            "After split, faces can move independently"
        ],
        "commonly_used_with": [
            ("Edge Angle", "split only sharp edges"),
            ("Scale Elements", "shrink split faces for gaps"),
            ("Set Position", "explode outward"),
            ("Set Shade Smooth (False)", "flat shading after")
        ],
        "example": "Explode effect: Split Edges (all) → Scale Elements (0.9) → Set Position (Normal × Random). Low-poly look: Split Edges → Set Shade Smooth (False) for faceted appearance."
    },
    
    "GeometryNodeEdgePathsToCurves": {
        "display_name": "Edge Paths to Curves",
        "category": "Mesh Operations",
        "description": "Converts connected edge sequences to curve splines - extracts paths from mesh edges.",
        "common_uses": [
            "Extract edge loops as curves",
            "Visualize shortest paths",
            "Wire frame from mesh edges"
        ],
        "pitfalls": [
            "Start Points: boolean selection for path starts",
            "Next Vertex Index: guides path direction",
            "Use with Shortest Edge Paths for routing"
        ],
        "commonly_used_with": [
            ("Shortest Edge Paths", "calculate path indices"),
            ("Curve to Mesh", "thicken resulting curves"),
            ("Edge Neighbors", "find boundary edges"),
            ("Compare", "select start/end vertices")
        ],
        "example": "Path visualization: Shortest Edge Paths (start→end) → Edge Paths to Curves → Curve to Mesh (thin tube). Edge loop extraction: select loop vertices, follow edge connectivity."
    },
    
    "GeometryNodeMeshCircle": {
        "display_name": "Mesh Circle",
        "category": "Mesh Primitives",
        "description": "Creates circular mesh - ring of edges or filled disk.",
        "common_uses": [
            "Flat platforms/bases",
            "Cylinder end caps",
            "Circular arrays"
        ],
        "pitfalls": [
            "Fill Type: None (ring only), N-gon (1 face), Triangle Fan",
            "N-gon: clean but doesn't subdivide well",
            "Triangle Fan: better for deformation"
        ],
        "commonly_used_with": [
            ("Extrude Mesh", "create cylinder"),
            ("Instance on Points", "arrange in circle"),
            ("Transform Geometry", "position disk"),
            ("Merge by Distance", "fix center vertex if needed")
        ],
        "example": "Quick cylinder: Mesh Circle (Fill N-gon) → Extrude Mesh. Smooth disk: Triangle Fan + Subdivision Surface. Vertices = smoothness (32+ for smooth circle)."
    },
    
    # ==========================================================================
    # POINT OPERATIONS
    # ==========================================================================
    
    "GeometryNodePointsToVertices": {
        "display_name": "Points to Vertices",
        "category": "Point",
        "description": "Converts point cloud to mesh vertices - no edges/faces, just vertex positions.",
        "common_uses": [
            "Prepare points for Convex Hull",
            "Convert scatter to mesh",
            "Vertex cloud creation"
        ],
        "pitfalls": [
            "Creates vertices only (no edges or faces)",
            "Use Convex Hull for solid mesh from points",
            "Attributes transfer from points to vertices"
        ],
        "commonly_used_with": [
            ("Convex Hull", "wrap in solid mesh"),
            ("Join Geometry", "combine with other meshes"),
            ("Merge by Distance", "weld close vertices"),
            ("Extrude Mesh", "spike from each vertex")
        ],
        "example": "Points to solid: Points to Vertices → Convex Hull. Vertex particles: Points to Vertices keeps visual as dots. Use when mesh operations need vertex input from point data."
    },
    
    "GeometryNodePointsToCurves": {
        "display_name": "Points to Curves",
        "category": "Point",
        "description": "Connects points into curve splines - connect-the-dots for geometry.",
        "common_uses": [
            "Create curves through points",
            "Drawing paths between locations",
            "Lightning/connection lines"
        ],
        "pitfalls": [
            "Point order determines curve shape (use Sort Elements)",
            "Curve Group ID: separate ID = separate spline",
            "Result is Poly curve (use Set Spline Type to smooth)"
        ],
        "commonly_used_with": [
            ("Sort Elements", "control connection order"),
            ("Set Spline Type (Catmull-Rom)", "smooth the result"),
            ("Curve to Mesh", "give curve thickness"),
            ("Index", "Group ID for multiple curves")
        ],
        "example": "Connect sorted points: Sort by X → Points to Curves → Set Spline Type (Catmull-Rom). Multiple curves: different Curve Group ID values create separate splines."
    },
    
    "GeometryNodeInstancesToPoints": {
        "display_name": "Instances to Points",
        "category": "Instances",
        "description": "Converts instances back to points at their locations - extracts positions, discards geometry.",
        "common_uses": [
            "Re-scatter with different objects",
            "Extract instance positions",
            "Chain instance operations"
        ],
        "pitfalls": [
            "Instance geometry is discarded",
            "Position/rotation/scale become point attributes",
            "Use Realize Instances to keep geometry"
        ],
        "commonly_used_with": [
            ("Instance on Points", "re-instance different geometry"),
            ("Points to Curves", "connect instance locations"),
            ("Capture Attribute", "preserve instance data"),
            ("Set Point Radius", "visualize as particles")
        ],
        "example": "Swap instances: existing instances → Instances to Points → Instance on Points (different object). Position transfer: get instance locations as points for further processing."
    },
    
    # ==========================================================================
    # SIMULATION & ZONES
    # ==========================================================================
    
    "GeometryNodeSimulationInput": {
        "display_name": "Simulation Zone",
        "category": "Simulation",
        "description": "Creates persistent state across frames - geometry remembers previous frame for physics and particles.",
        "common_uses": [
            "Custom particle systems",
            "Velocity-based motion",
            "Accumulating geometry over time"
        ],
        "pitfalls": [
            "Must start from frame 1 (or bake)",
            "Delta Time: use for frame-rate independent motion",
            "Skip output: marks data that resets each frame"
        ],
        "commonly_used_with": [
            ("Set Position", "velocity-based movement"),
            ("Delete Geometry", "particle death by age"),
            ("Join Geometry", "spawn new particles"),
            ("Scene Time", "age and lifetime logic")
        ],
        "example": "Particle system: Join new points each frame, store velocity attribute, Set Position += velocity × Delta Time, Delete when age > lifetime. Bake simulation for consistent playback."
    },
    
    "GeometryNodeRepeatInput": {
        "display_name": "Repeat Zone",
        "category": "Utilities",
        "description": "Loops operations N times in single frame - for-loop equivalent in geometry nodes.",
        "common_uses": [
            "Iterative subdivision",
            "Fractal branching patterns",
            "Cumulative transforms"
        ],
        "pitfalls": [
            "All iterations run instantly (not across frames)",
            "High iterations = slow evaluation",
            "Different from Simulation (no frame persistence)"
        ],
        "commonly_used_with": [
            ("Subdivide Mesh", "repeated subdivision"),
            ("Extrude Mesh", "fractal extrusion"),
            ("Transform Geometry", "cumulative rotation/scale"),
            ("Join Geometry", "accumulate copies")
        ],
        "example": "Fractal tree: Start with trunk, Repeat 5×: Extrude selected, Scale down 0.7, Rotate branches. Each iteration adds another generation of branches."
    },
    
    # ==========================================================================
    # VOLUME NODES
    # ==========================================================================
    
    "GeometryNodeMeshToVolume": {
        "display_name": "Mesh to Volume",
        "category": "Volume",
        "description": "Converts closed mesh to voxel density data - for fog rendering or volume operations.",
        "common_uses": [
            "Fog/smoke from mesh shape",
            "Volume-based smoothing pipeline",
            "Soft body approximation"
        ],
        "pitfalls": [
            "Mesh must be watertight (closed)",
            "Voxel Amount: higher = more detail, slower",
            "Interior Band Width affects shell thickness"
        ],
        "commonly_used_with": [
            ("Volume to Mesh", "smooth mesh workflow"),
            ("Set Material", "volume shader"),
            ("Distribute Points in Volume", "scatter inside"),
            ("Volume Cube", "combine volumes")
        ],
        "example": "Smooth mesh: Mesh to Volume (resolution 0.1) → Volume to Mesh (threshold 0.5). Rounds corners and fills gaps. For fog: assign Principled Volume material after conversion."
    },
    
    "GeometryNodeVolumeToMesh": {
        "display_name": "Volume to Mesh",
        "category": "Volume",
        "description": "Extracts mesh surface from volume at density threshold - creates organic, blob-like geometry.",
        "common_uses": [
            "Metaball-style merging",
            "Smooth mesh from volume",
            "Cloud/organic shapes"
        ],
        "pitfalls": [
            "Threshold: density level to create surface",
            "Adaptivity: higher = fewer polygons, less detail",
            "Thin areas may create holes"
        ],
        "commonly_used_with": [
            ("Mesh to Volume", "mesh smoothing workflow"),
            ("Volume Cube", "procedural volume source"),
            ("Set Shade Smooth", "smooth resulting mesh"),
            ("Decimate", "reduce polygon count")
        ],
        "example": "Metaball effect: multiple meshes → Mesh to Volume each → Join volumes → Volume to Mesh. Overlapping areas merge smoothly. Threshold 0 = outer surface, higher = shrinks inward."
    },
    
    "GeometryNodeVolumeCube": {
        "display_name": "Volume Cube",
        "category": "Volume",
        "description": "Creates a box-shaped volume filled with density - simplest volume primitive.",
        "common_uses": [
            "Fog/cloud base shape",
            "Testing volume workflows",
            "Procedural volume effects"
        ],
        "pitfalls": [
            "Density: fill value (0 = empty, 1 = solid)",
            "Resolution X/Y/Z: voxels per axis",
            "Background: value outside the cube"
        ],
        "commonly_used_with": [
            ("Volume to Mesh", "extract surface"),
            ("Set Material", "Principled Volume shader"),
            ("Distribute Points in Volume", "scatter inside"),
            ("Transform Geometry", "position the volume")
        ],
        "example": "Simple fog box: Volume Cube (density 1.0) → Set Material with Principled Volume (density 0.1, white color). Increase resolution for finer detail in renders."
    },
    
    # ==========================================================================
    # UV NODES
    # ==========================================================================
    
    "GeometryNodeUVUnwrap": {
        "display_name": "UV Unwrap",
        "category": "UV",
        "description": "Generates UV coordinates by flattening mesh - essential for texturing procedural geometry.",
        "common_uses": [
            "Texture mapping procedural meshes",
            "Auto-UV for generated geometry",
            "Preparing for image textures"
        ],
        "pitfalls": [
            "Seam selection crucial for quality",
            "Method: Angle Based vs Conformal",
            "Margin prevents texture bleeding between islands"
        ],
        "commonly_used_with": [
            ("Store Named Attribute", "save as 'UVMap'"),
            ("Edge Angle", "auto-select seams"),
            ("Pack UV Islands", "optimize layout"),
            ("Named Attribute", "read existing UVs")
        ],
        "example": "Auto-UV: Edge Angle > 45° as Seam selection → UV Unwrap → Store Named Attribute 'UVMap' (Vector, Face Corner). Material's Image Texture now works on procedural mesh."
    },
    
    "GeometryNodeUVPackIslands": {
        "display_name": "Pack UV Islands",
        "category": "UV",
        "description": "Rearranges UV islands to maximize texture space usage - optimizes UV layout.",
        "common_uses": [
            "Optimize UV efficiency",
            "Consistent texel density",
            "Clean up scattered UVs"
        ],
        "pitfalls": [
            "Works on existing UV attribute",
            "Margin: gap between islands (prevents bleeding)",
            "Rotate: allows rotation for better fit"
        ],
        "commonly_used_with": [
            ("UV Unwrap", "create UVs first"),
            ("Named Attribute", "read UV input"),
            ("Store Named Attribute", "save packed result"),
            ("Scale UV", "adjust before packing")
        ],
        "example": "After UV Unwrap: Pack UV Islands (margin 0.01, rotate enabled) → Store Named Attribute. Islands fill 0-1 UV space efficiently. Higher margin = safer texture seams."
    },
    
    # ==========================================================================
    # INDEX / MENU SWITCH
    # ==========================================================================
    
    "GeometryNodeIndexSwitch": {
        "display_name": "Index Switch",
        "category": "Utilities",
        "description": "Selects from multiple inputs using integer index - array-style access.",
        "common_uses": [
            "Multi-option selection",
            "Index-based variation",
            "Sequential cycling"
        ],
        "pitfalls": [
            "Index 0 = first input, 1 = second, etc.",
            "Out-of-range index clamps to valid range",
            "All inputs evaluate regardless of selection"
        ],
        "commonly_used_with": [
            ("Random Value (Integer)", "random selection"),
            ("Index", "per-element variation"),
            ("Math (Modulo)", "cycling through options"),
            ("Group Input", "user dropdown")
        ],
        "example": "4 material variations: Index Switch with 4 materials, Random Value (Integer 0-3) as index. Each face gets random material. Or use Index % 4 for repeating pattern."
    },
    
    "GeometryNodeMenuSwitch": {
        "display_name": "Menu Switch",
        "category": "Utilities",
        "description": "Dropdown menu for selecting between named options - user-friendly modifier interface.",
        "common_uses": [
            "Preset/style selection",
            "Mode toggles",
            "Clean user interface"
        ],
        "pitfalls": [
            "Options defined in node editor",
            "Fixed choice set (not dynamic)",
            "Exposed as dropdown in modifier panel"
        ],
        "commonly_used_with": [
            ("Group Input", "expose to modifier"),
            ("Any geometry/value", "different options"),
            ("Collection Info", "object set selection"),
            ("Material", "material presets")
        ],
        "example": "Building styles: Menu Switch with 'Modern', 'Victorian', 'Industrial' items, each connecting different geometry setups. User sees clean dropdown instead of index numbers."
    },
    
    # ==========================================================================
    # SPLINE UTILITIES
    # ==========================================================================
    
    "GeometryNodeSplineParameter": {
        "display_name": "Spline Parameter",
        "category": "Curve Operations",
        "description": "Returns 0-1 position factor along curve - essential for gradients and tapers.",
        "common_uses": [
            "Tapered curve radius",
            "Color gradient along path",
            "Position-based effects"
        ],
        "pitfalls": [
            "Factor: 0 = start, 1 = end (normalized)",
            "Length: actual distance in scene units",
            "Per-spline in multi-spline curves"
        ],
        "commonly_used_with": [
            ("Set Curve Radius", "taper thickness"),
            ("Color Ramp", "gradient along curve"),
            ("Map Range", "adjust taper profile"),
            ("Compare", "select end portion")
        ],
        "example": "Tapered tentacle: Spline Parameter Factor → Map Range (1 to 0.1) → Set Curve Radius. Thick at base, thin at tip. Invert range for opposite taper."
    },
    
    "GeometryNodeSplineLength": {
        "display_name": "Spline Length",
        "category": "Curve Operations",
        "description": "Returns total length and point count of each spline - for length-based calculations.",
        "common_uses": [
            "Calculate instance spacing",
            "Length-based filtering",
            "Normalize by curve size"
        ],
        "pitfalls": [
            "Length: scene units (usually meters)",
            "Point Count: integer vertex count",
            "Per-spline value (not per-point)"
        ],
        "commonly_used_with": [
            ("Math (Divide)", "spacing calculations"),
            ("Resample Curve", "points based on length"),
            ("Compare", "filter short/long curves"),
            ("Spline Parameter", "combine for position math")
        ],
        "example": "Fence posts every 2m: Spline Length ÷ 2 = post count for Resample. Or compare length to filter out curves shorter than 1m."
    },
    
    # ==========================================================================
    # ALIGN / ROTATION UTILITIES
    # ==========================================================================
    
    "FunctionNodeAlignEulerToVector": {
        "display_name": "Align Euler to Vector",
        "category": "Utilities",
        "description": "Creates rotation pointing an axis along a vector - essential for orienting instances.",
        "common_uses": [
            "Instances pointing along normals",
            "Objects following curve tangent",
            "Aim-at-target rotation"
        ],
        "pitfalls": [
            "Axis: which local axis points along vector (usually Z)",
            "Pivot Axis: constrains rotation around this axis",
            "Output is Euler (radians), use with Rotate Instances"
        ],
        "commonly_used_with": [
            ("Normal", "grass/hair pointing from surface"),
            ("Curve to Points Tangent", "objects along path"),
            ("Rotate Instances", "apply the rotation"),
            ("Vector Math (Subtract)", "direction to target")
        ],
        "example": "Grass on terrain: Normal → Align Euler to Vector (Axis Z) → Rotate Instances. Add Random Value to Rotation for natural tilt variation."
    },
    
    "FunctionNodeRotateEuler": {
        "display_name": "Rotate Euler",
        "category": "Utilities",
        "description": "Combines/modifies Euler rotations - add offset to existing rotation.",
        "common_uses": [
            "Add random rotation offset",
            "Combine base alignment + variation",
            "Incremental rotation"
        ],
        "pitfalls": [
            "Type: Local (relative) vs Global (absolute)",
            "Rotation order affects result",
            "Gimbal lock possible with Euler angles"
        ],
        "commonly_used_with": [
            ("Align Euler to Vector", "base alignment"),
            ("Random Value", "random offset"),
            ("Rotate Instances", "apply result"),
            ("Scene Time", "animated rotation")
        ],
        "example": "Natural scatter: Align Euler to Vector (base) → Rotate Euler + Random Value (small Z offset). Objects align to surface but face random directions."
    },
    
    # ==========================================================================
    # VALUE INPUT
    # ==========================================================================
    
    "FunctionNodeInputFloat": {
        "display_name": "Value",
        "category": "Input",
        "description": "Single floating-point number input - becomes slider in modifier panel.",
        "common_uses": [
            "User-adjustable parameters",
            "Constant values",
            "Scale/strength factors"
        ],
        "pitfalls": [
            "Can be negative or decimal",
            "No automatic min/max clamping",
            "Use Integer node for whole numbers only"
        ],
        "commonly_used_with": [
            ("Math", "in calculations"),
            ("Map Range", "as range bounds"),
            ("Compare", "as threshold"),
            ("Group Input", "alternative for exposed params")
        ],
        "example": "Noise Scale parameter: Value → Noise Texture Scale. Displacement strength: Value → multiply with displacement. In Group: becomes labeled slider."
    },
    
    "FunctionNodeInputColor": {
        "display_name": "Color",
        "category": "Input",
        "description": "RGBA color input - becomes color picker in modifier panel.",
        "common_uses": [
            "User-selectable colors",
            "Tint/multiply colors",
            "Vertex color source"
        ],
        "pitfalls": [
            "Values can exceed 0-1 (HDR colors)",
            "Alpha is fourth component",
            "Linear color space internally"
        ],
        "commonly_used_with": [
            ("Store Named Attribute", "save as vertex color"),
            ("Mix", "blend/tint colors"),
            ("Separate Color", "extract components"),
            ("Set Material", "material uses color")
        ],
        "example": "Tint control: Color → Mix with procedural color. Base color: Color → Store Named Attribute (Color). In Group: becomes color picker widget."
    },
    
    # ==========================================================================
    # GROUP NODES
    # ==========================================================================
    
    "NodeGroupInput": {
        "display_name": "Group Input",
        "category": "Input",
        "description": "Defines inputs for node group - becomes modifier panel controls.",
        "common_uses": [
            "User-adjustable parameters",
            "Geometry input connection",
            "Reusable node group interface"
        ],
        "pitfalls": [
            "First socket typically Geometry (input mesh)",
            "Socket names = modifier panel labels",
            "Drag to edge to add new input sockets"
        ],
        "commonly_used_with": [
            ("Group Output", "every group needs both"),
            ("Any node", "feeds all calculations"),
            ("Switch", "boolean toggle controls"),
            ("Math", "process numeric inputs")
        ],
        "example": "Add Float socket named 'Scale' → appears as slider in modifier. Add Object socket → picker for target object. Add Boolean → checkbox toggle. Socket order = panel order."
    },
    
    "NodeGroupOutput": {
        "display_name": "Group Output",
        "category": "Output",
        "description": "Defines outputs from node group - Geometry output is the visible result.",
        "common_uses": [
            "Final geometry delivery",
            "Return calculated values",
            "Multiple outputs for nested groups"
        ],
        "pitfalls": [
            "Unconnected Geometry = invisible result",
            "Must connect something for visible output",
            "Additional outputs available to parent groups"
        ],
        "commonly_used_with": [
            ("Group Input", "every group needs both"),
            ("Join Geometry", "combine before final output"),
            ("Set Material", "assign material before output"),
            ("Realize Instances", "if needed for certain operations")
        ],
        "example": "Connect final geometry to Geometry output. Add extra outputs (Float, Vector) to pass data to parent node groups. Nothing connected = nothing visible."
    },
    
    # ==========================================================================
    # ADDITIONAL GEOMETRY NODES
    # ==========================================================================
    
    "GeometryNodeSampleNearest": {
        "display_name": "Sample Nearest",
        "category": "Geometry",
        "description": "Finds index of closest element on target geometry - pair with Sample Index for value lookup.",
        "common_uses": [
            "Transfer attributes between meshes",
            "Find closest point/face",
            "Proximity-based data lookup"
        ],
        "pitfalls": [
            "Returns INDEX, not position",
            "Use with Sample Index to get actual values",
            "Domain: search Points, Edges, Faces, or Corners"
        ],
        "commonly_used_with": [
            ("Sample Index", "retrieve value at found index"),
            ("Object Info", "target geometry source"),
            ("Position", "sample position input"),
            ("Geometry Proximity", "alternative: gives position directly")
        ],
        "example": "Transfer vertex colors: Sample Nearest (target mesh) → Sample Index (color attribute, found index). Each point gets color from nearest vertex on other mesh."
    },
    
    "GeometryNodeInputMaterialIndex": {
        "display_name": "Material Index",
        "category": "Material",
        "description": "Returns material slot number per face - for material-based selection and effects.",
        "common_uses": [
            "Select by material slot",
            "Different effects per material",
            "Material-based distribution"
        ],
        "pitfalls": [
            "0 = first material slot, 1 = second, etc.",
            "Only valid on mesh faces",
            "Returns -1 if no material assigned"
        ],
        "commonly_used_with": [
            ("Compare", "select specific material"),
            ("Index Switch", "different value per material"),
            ("Delete Geometry", "remove by material"),
            ("Set Material Index", "reassign materials")
        ],
        "example": "Select red material faces: Material Index = 2 (if red is 3rd slot) → use as selection. Different scatter density per material: Compare Material Index, different Density per branch."
    },
    
    "GeometryNodeInputSelection": {
        "display_name": "Selection",
        "category": "Input",
        "description": "Reads edit mode selection state - True for selected, False for unselected elements.",
        "common_uses": [
            "Affect only selected geometry",
            "Edit mode selection as input",
            "Combine with procedural selection"
        ],
        "pitfalls": [
            "Empty/all-false in object mode",
            "Per-element boolean output",
            "Requires 'Apply on Spline' etc. to work"
        ],
        "commonly_used_with": [
            ("Delete Geometry", "delete selected"),
            ("Set Position", "move selected only"),
            ("Boolean Math", "combine with other selection"),
            ("Separate Geometry", "extract selected")
        ],
        "example": "Selection-based extrude: Selection as Extrude Selection. Invert: Boolean Math NOT on Selection. Only works when modifier applied with selection active."
    },
    
    "GeometryNodeMeshPrimitiveCircle": {
        "display_name": "Circle (Mesh)",
        "category": "Mesh Primitives",
        "description": "Creates circular mesh - filled disk or edge ring only.",
        "common_uses": [
            "Flat circular platforms",
            "Disc/coin shapes",
            "Starting point for cylinders"
        ],
        "pitfalls": [
            "Fill Type: None (edges only), Ngon (1 face), Triangle Fan",
            "Ngon = single n-sided face",
            "Triangle Fan = triangles meeting at center"
        ],
        "commonly_used_with": [
            ("Extrude Mesh", "create cylinder"),
            ("Curve Circle", "alternative as curve"),
            ("Subdivide Mesh", "more geometry for deformation"),
            ("Set Shade Smooth", "smooth disc")
        ],
        "example": "Disc: Fill Type Ngon. Cylinder base: Fill Type Triangle Fan → Extrude. Edge ring only: Fill Type None for profile curves."
    },
    
    # ==========================================================================
    # MESH READ NODES (from Blender 5.0 Manual)
    # ==========================================================================
    
    "GeometryNodeInputMeshEdgeAngle": {
        "display_name": "Edge Angle",
        "category": "Mesh Read",
        "description": "Measures angle between faces sharing an edge - for sharp edge detection.",
        "common_uses": [
            "Auto-smooth edge selection",
            "Find creases for beveling",
            "Sharp edge marking"
        ],
        "pitfalls": [
            "Output in radians (π = 180°)",
            "Unsigned: 0 to π, Signed: considers face winding",
            "Boundary edges return 0"
        ],
        "commonly_used_with": [
            ("Compare", "threshold for sharp edges"),
            ("Set Shade Smooth", "auto-smooth effect"),
            ("Split Edges", "split at sharp angles"),
            ("Math (Degrees)", "convert to degrees")
        ],
        "example": "Auto-smooth: Edge Angle > 0.5 (≈30°) → Set Shade Smooth (False). Finds sharp edges where faces meet at steep angles, keeps them crisp."
    },
    
    "GeometryNodeInputMeshEdgeNeighbors": {
        "display_name": "Edge Neighbors",
        "category": "Mesh Read",
        "description": "Counts faces connected to each edge - finds boundaries and loose edges.",
        "common_uses": [
            "Select boundary edges (=1 face)",
            "Find non-manifold edges (>2 faces)",
            "Detect loose edges (=0 faces)"
        ],
        "pitfalls": [
            "0 = loose edge (no faces)",
            "1 = boundary edge (open mesh edge)",
            "2 = manifold interior edge"
        ],
        "commonly_used_with": [
            ("Compare", "boundary selection (= 1)"),
            ("Mesh to Curve", "convert boundaries"),
            ("Delete Geometry", "remove loose edges"),
            ("Extrude Mesh", "extrude boundaries")
        ],
        "example": "Extract mesh outline: Edge Neighbors = 1 → Mesh to Curve. Clean mesh: Edge Neighbors = 0 → Delete Geometry removes loose edges. Non-manifold check: > 2 indicates problems."
    },
    
    "GeometryNodeInputMeshEdgeVertices": {
        "display_name": "Edge Vertices",
        "category": "Mesh Read",
        "description": "Returns positions and indices of both vertices forming each edge.",
        "common_uses": [
            "Calculate edge direction vectors",
            "Find edge midpoints",
            "Edge length calculations"
        ],
        "pitfalls": [
            "Vertex order is arbitrary (no guaranteed start/end)",
            "Must evaluate in Edge domain",
            "Outputs: Vertex Index 1/2, Position 1/2"
        ],
        "commonly_used_with": [
            ("Vector Math (Subtract)", "edge direction"),
            ("Vector Math (Length)", "edge length"),
            ("Mix", "edge midpoint"),
            ("Sample Index", "get vertex attributes")
        ],
        "example": "Edge length: Length(Position 2 - Position 1). Edge midpoint: Mix (Position 1, Position 2, 0.5). Edge direction: Normalize(Position 2 - Position 1)."
    },
    
    "GeometryNodeInputMeshFaceArea": {
        "display_name": "Face Area",
        "category": "Mesh Read",
        "description": "Outputs surface area of each face - for density and size-based selection.",
        "common_uses": [
            "Remove tiny/degenerate faces",
            "Area-weighted distribution",
            "Select large/small faces"
        ],
        "pitfalls": [
            "Units are scene units² (usually m²)",
            "0 area = degenerate face (should delete)",
            "N-gon areas can be unexpected"
        ],
        "commonly_used_with": [
            ("Compare", "size threshold selection"),
            ("Delete Geometry", "remove tiny faces"),
            ("Distribute Points on Faces", "density proportional to area"),
            ("Attribute Statistic", "find min/max/average")
        ],
        "example": "Clean mesh: Face Area < 0.0001 → Delete Geometry. Even distribution: Distribute Points uses area automatically. Select large faces: Face Area > threshold."
    },
    
    "GeometryNodeInputMeshFaceNeighbors": {
        "display_name": "Face Neighbors",
        "category": "Mesh Read",
        "description": "Counts vertices/edges per face and adjacent faces - detects tris, quads, n-gons.",
        "common_uses": [
            "Select triangles (=3) or quads (=4)",
            "Find n-gons for cleanup (>4)",
            "Topology analysis"
        ],
        "pitfalls": [
            "Vertex Count = Edge Count for faces",
            "3 = triangle, 4 = quad, 5+ = n-gon",
            "Face Count = adjacent face count"
        ],
        "commonly_used_with": [
            ("Compare", "select by vertex count"),
            ("Triangulate", "fix n-gons after detection"),
            ("Delete Geometry", "remove problem faces"),
            ("Separate Geometry", "isolate by type")
        ],
        "example": "Find n-gons: Vertex Count > 4. Select only quads: Vertex Count = 4. Triangulate only n-gons: Vertex Count > 4 as Triangulate selection."
    },
    
    "GeometryNodeInputMeshFaceIsPlanar": {
        "display_name": "Is Face Planar",
        "category": "Mesh Read",
        "description": "Tests if face vertices lie in same plane - detects warped quads/ngons.",
        "common_uses": [
            "Find warped faces",
            "Mesh quality validation",
            "3D printing preparation"
        ],
        "pitfalls": [
            "Threshold: planarity tolerance",
            "Triangles always return True",
            "Non-planar faces may render/print poorly"
        ],
        "commonly_used_with": [
            ("Triangulate", "fix non-planar faces"),
            ("Delete Geometry", "remove problem faces"),
            ("Separate Geometry", "isolate non-planar"),
            ("Boolean Math (NOT)", "select non-planar")
        ],
        "example": "Find problems: NOT(Is Face Planar) = warped faces. Fix: Triangulate non-planar selection. Low threshold = strict planarity check."
    },
    
    "GeometryNodeInputMeshIsland": {
        "display_name": "Mesh Island",
        "category": "Mesh Read",
        "description": "Returns unique index per disconnected mesh piece - for per-island operations.",
        "common_uses": [
            "Random color/transform per island",
            "Select specific mesh pieces",
            "Explode/separate effects"
        ],
        "pitfalls": [
            "Island Index: 0, 1, 2... per disconnected piece",
            "Island Count: total number of islands",
            "Connection = shared vertices (not proximity)"
        ],
        "commonly_used_with": [
            ("Random Value", "Island Index as seed"),
            ("Separate Geometry", "extract specific island"),
            ("Accumulate Field", "per-island grouping"),
            ("Compare", "select island by index")
        ],
        "example": "Random per-island color: Island Index as Random seed. Separate pieces: Island Index = 0 as selection → Separate Geometry. Each loose mesh part gets unique index."
    },
    
    "GeometryNodeInputMeshVertexNeighbors": {
        "display_name": "Vertex Neighbors",
        "category": "Mesh Read",
        "description": "Counts edges and faces connected to each vertex - for topology analysis.",
        "common_uses": [
            "Find boundary vertices (fewer neighbors)",
            "Detect poles (5+ edge connections)",
            "Select loose vertices (0 neighbors)"
        ],
        "pitfalls": [
            "Edge Count: edges meeting at vertex",
            "Face Count: faces touching vertex",
            "Boundary verts have unequal edge/face counts"
        ],
        "commonly_used_with": [
            ("Compare", "detect poles (Edge Count > 4)"),
            ("Delete Geometry", "remove loose (= 0)"),
            ("Separate Geometry", "isolate by connectivity"),
            ("Edge Neighbors", "complementary for edges")
        ],
        "example": "Find poles: Edge Count > 4. Boundary vertices: Edge Count ≠ Face Count. Clean loose: Face Count = 0 → Delete. Regular quads have Edge Count = 4."
    },
    
    "GeometryNodeInputShortestEdgePaths": {
        "display_name": "Shortest Edge Paths",
        "category": "Mesh Read",
        "description": "Calculates shortest path along edges from source vertices - geodesic pathfinding.",
        "common_uses": [
            "Visualize mesh paths",
            "Distance-from-source effects",
            "Path-based animation"
        ],
        "pitfalls": [
            "End Vertex: True for destination vertices",
            "Edge Cost: weight per edge (default 1)",
            "Next Vertex Index: step toward destination"
        ],
        "commonly_used_with": [
            ("Edge Paths to Curves", "visualize paths"),
            ("Map Range", "normalize distances"),
            ("Compare", "distance threshold selection"),
            ("Set Position", "path-based deformation")
        ],
        "example": "Distance gradient: select one vertex as End → Total Cost = distance from it → Color Ramp. Path visualization: → Edge Paths to Curves → Curve to Mesh (thin tube)."
    },
    
    # ==========================================================================
    # TEXT / STRING NODES (from Blender 5.0 Manual)
    # ==========================================================================
    
    "GeometryNodeStringToCurves": {
        "display_name": "String to Curves",
        "category": "Text",
        "description": "Converts text to curve geometry - procedural 3D text generation.",
        "common_uses": [
            "3D text and titles",
            "Dynamic labels and counters",
            "Logo typography"
        ],
        "pitfalls": [
            "Font: must select .ttf/.otf file",
            "Characters are instances (efficient but linked)",
            "Pivot Point affects text alignment"
        ],
        "commonly_used_with": [
            ("Fill Curve", "flat solid text"),
            ("Extrude Mesh", "3D extruded letters"),
            ("Realize Instances", "per-character manipulation"),
            ("Join Strings", "build dynamic text content")
        ],
        "example": "3D title: String to Curves → Fill Curve → Extrude (0.1m) → Set Shade Smooth. For per-character animation, Realize Instances first, then use Index for staggered effects."
    },
    
    "FunctionNodeJoinStrings": {
        "display_name": "Join Strings",
        "category": "Text",
        "description": "Concatenates multiple strings with optional delimiter - builds text from parts.",
        "common_uses": [
            "Dynamic label construction",
            "Path/filename building",
            "Formatted output text"
        ],
        "pitfalls": [
            "Delimiter only between strings (not at ends)",
            "Add more inputs via + button",
            "Empty strings still count for delimiter"
        ],
        "commonly_used_with": [
            ("Value to String", "include numbers"),
            ("String to Curves", "display result"),
            ("Special Characters", "newlines, tabs"),
            ("String", "constant text parts")
        ],
        "example": "Counter display: 'Score: ' + Value to String(score) = 'Score: 42'. CSV: Join with delimiter ',' creates comma-separated values."
    },
    
    "FunctionNodeValueToString": {
        "display_name": "Value to String",
        "category": "Text",
        "description": "Converts numbers to text with decimal precision control.",
        "common_uses": [
            "Numeric displays/counters",
            "Debug value readouts",
            "Labels with measurements"
        ],
        "pitfalls": [
            "Decimals: 0 = integer, 2 = '3.14'",
            "Very large numbers may overflow",
            "Negative decimals round to powers of 10"
        ],
        "commonly_used_with": [
            ("Join Strings", "combine with labels"),
            ("String to Curves", "display as 3D text"),
            ("Math", "calculate value first"),
            ("Attribute Statistic", "show min/max/average")
        ],
        "example": "Frame counter: Scene Time (Frame) → Value to String (Decimals 0) → Join with 'Frame: ' → String to Curves. Precision: Decimals 2 turns 3.14159 → '3.14'."
    },
    
    "FunctionNodeReplaceString": {
        "display_name": "Replace String",
        "category": "Text",
        "description": "Find and replace text within strings - template substitution.",
        "common_uses": [
            "Template variable replacement",
            "Text cleanup/sanitization",
            "Format conversion"
        ],
        "pitfalls": [
            "Replaces ALL occurrences",
            "Case-sensitive matching",
            "Empty Find returns original unchanged"
        ],
        "commonly_used_with": [
            ("String", "template with placeholders"),
            ("Value to String", "replacement values"),
            ("String to Curves", "display result"),
            ("Join Strings", "build replacement text")
        ],
        "example": "Template: 'Hello {NAME}!' → Replace '{NAME}' with 'World' = 'Hello World!'. Batch processing: replace all '\\n' with space for single-line output."
    },
    
    "FunctionNodeSliceString": {
        "display_name": "Slice String",
        "category": "Text",
        "description": "Extracts substring by position and length - text parsing and truncation.",
        "common_uses": [
            "Extract first N characters",
            "Get file extension",
            "Truncate long text"
        ],
        "pitfalls": [
            "Position 0 = first character",
            "Negative position counts from end",
            "Length beyond string returns what's available"
        ],
        "commonly_used_with": [
            ("String Length", "calculate positions"),
            ("Join Strings", "recombine parts"),
            ("Compare", "check specific characters"),
            ("String to Curves", "display result")
        ],
        "example": "First 3 chars: Slice(0, 3). Last 4 chars: Slice(-4, 4). Middle portion: use String Length to calculate positions dynamically."
    },
    
    "FunctionNodeStringLength": {
        "display_name": "String Length",
        "category": "Text",
        "description": "Returns character count of a string - for validation and position calculations.",
        "common_uses": [
            "Validate input length",
            "Calculate slice end position",
            "Conditional text processing"
        ],
        "pitfalls": [
            "Counts ALL characters (including spaces)",
            "Empty string = 0",
            "Some Unicode characters count as multiple"
        ],
        "commonly_used_with": [
            ("Slice String", "dynamic end position"),
            ("Compare", "length validation"),
            ("Switch", "length-based branching"),
            ("Math", "arithmetic with length")
        ],
        "example": "Truncate to 10 chars: if String Length > 10, Slice(0, 10) + '...'. Get last character: Slice(Length-1, 1)."
    },
    
    "FunctionNodeSpecialCharacters": {
        "display_name": "Special Characters",
        "category": "Text",
        "description": "Outputs newline, tab, and other non-typeable characters.",
        "common_uses": [
            "Multi-line text",
            "Tab-separated formatting",
            "Text file structure"
        ],
        "pitfalls": [
            "Line Break = Enter/newline character",
            "Tab = horizontal indent",
            "String to Curves may not render all special chars"
        ],
        "commonly_used_with": [
            ("Join Strings", "insert between lines"),
            ("Replace String", "add/remove line breaks"),
            ("String to Curves", "multi-line display"),
            ("Slice String", "split on newlines")
        ],
        "example": "Multi-line label: Join Strings with Line Break delimiter. Address block: 'Name' + LineBreak + 'Street' + LineBreak + 'City'. Tab-separated: delimiter = Tab."
    },
    
    # ==========================================================================
    # MESH OPERATIONS (from Blender 5.0 Manual)
    # ==========================================================================
    
    "GeometryNodeMeshToCurve": {
        "display_name": "Mesh to Curve",
        "category": "Mesh Operations",
        "description": "Converts mesh edges to curve splines - extracts wireframe as curves.",
        "common_uses": [
            "Wireframe to tubes",
            "Extract boundary edges",
            "Edge loop to curve path"
        ],
        "pitfalls": [
            "Only converts edges (not faces)",
            "Connected edges = single spline",
            "Vertices at intersections split curves"
        ],
        "commonly_used_with": [
            ("Edge Neighbors", "select boundary (=1) edges"),
            ("Curve to Mesh", "give curves thickness"),
            ("Set Spline Type", "smooth result"),
            ("Resample Curve", "even point spacing")
        ],
        "example": "Wireframe tube: Mesh to Curve (all edges) → Curve to Mesh with small Circle profile. Extract outline: Edge Neighbors = 1 as selection → Mesh to Curve."
    },
    
    "GeometryNodeMeshToPoints": {
        "display_name": "Mesh to Points",
        "category": "Mesh Operations",
        "description": "Converts mesh elements to point cloud - vertices, edge centers, face centers, or corners.",
        "common_uses": [
            "Instance at mesh element positions",
            "Convert mesh to particles",
            "Sample mesh positions as points"
        ],
        "pitfalls": [
            "Mode: Vertices, Edges, Faces, or Corners",
            "Position input can override locations",
            "Attributes transfer from mesh to points"
        ],
        "commonly_used_with": [
            ("Instance on Points", "scatter on mesh elements"),
            ("Set Point Radius", "vary point sizes"),
            ("Points to Vertices", "convert back to mesh"),
            ("Random Value", "add point variation")
        ],
        "example": "Objects at face centers: Mesh to Points (Faces mode) → Instance on Points. Vertex particles: Mesh to Points (Vertices) → Set Point Radius for display."
    },
    
    "GeometryNodeSampleNearestSurface": {
        "display_name": "Sample Nearest Surface",
        "category": "Geometry",
        "description": "Samples attribute values from closest point on mesh surface - for projection and transfer.",
        "common_uses": [
            "Project points onto surface",
            "Transfer attributes between meshes",
            "Surface snapping"
        ],
        "pitfalls": [
            "Target must be mesh geometry",
            "Position output = closest surface point",
            "Interpolates between face corners"
        ],
        "commonly_used_with": [
            ("Object Info", "target mesh source"),
            ("Set Position", "snap to Position output"),
            ("Vector Math (Subtract)", "get direction to surface"),
            ("Raycast", "alternative with direction")
        ],
        "example": "Snap to surface: Sample Nearest Surface → Set Position to result. Transfer color: sample Color attribute from target mesh. Distance to surface: Length(Position - Sample Position)."
    },
    
    "GeometryNodeSampleUVSurface": {
        "display_name": "Sample UV Surface",
        "category": "Geometry",
        "description": "Samples mesh data at UV coordinates - maps 2D UV space to 3D surface.",
        "common_uses": [
            "UV-based positioning",
            "2D pattern to 3D surface",
            "Decal/sticker placement"
        ],
        "pitfalls": [
            "Requires valid UV map on mesh",
            "Source UV: which UV map to use",
            "Is Valid: False if UV not found"
        ],
        "commonly_used_with": [
            ("Named Attribute (UVMap)", "get UV coordinates"),
            ("Set Position", "position at UV location"),
            ("Grid", "2D UV source points"),
            ("Image Texture", "sample same UVs")
        ],
        "example": "Place object at UV: Sample UV Surface (0.5, 0.5) = center of UV space on 3D surface. Grid of points: UV Grid → Sample UV Surface = distribute on mesh via UVs."
    },
    
    "GeometryNodeViewer": {
        "display_name": "Viewer",
        "category": "Output",
        "description": "Debug tool - displays geometry or field values in viewport and Spreadsheet editor.",
        "common_uses": [
            "Debug intermediate results",
            "Inspect attribute values",
            "Visualize field outputs"
        ],
        "pitfalls": [
            "Only ONE viewer active at a time",
            "Ctrl+Shift+Click: quick add viewer",
            "Value socket: shows as color/number overlay"
        ],
        "commonly_used_with": [
            ("Any node output", "debug connection"),
            ("Position", "visualize point locations"),
            ("Index", "check element numbering"),
            ("Named Attribute", "inspect stored data")
        ],
        "example": "Debug workflow: Ctrl+Shift+Click any socket to view its output. Check Spreadsheet editor for detailed per-element data. Only one viewer shows at a time - click viewer node to activate it."
    },
    
    "GeometryNodeSetPointRadius": {
        "display_name": "Set Point Radius",
        "category": "Point",
        "description": "Sets size attribute on point cloud points - affects display and volume conversion.",
        "common_uses": [
            "Vary particle sizes",
            "Distance-based point scaling",
            "Points to Volume influence"
        ],
        "pitfalls": [
            "Only affects Point Cloud geometry (not mesh vertices)",
            "Radius stored as 'radius' attribute",
            "Default display may not show size (check viewport settings)"
        ],
        "commonly_used_with": [
            ("Random Value", "varied point sizes"),
            ("Points to Volume", "radius affects blob size"),
            ("Map Range", "controlled size range"),
            ("Spline Parameter", "size along curve")
        ],
        "example": "Varied particles: Set Point Radius with Random (0.05 to 0.2). Distance falloff: Proximity distance → Map Range → Set Point Radius. Affects Points to Volume blob merging."
    },
    
    "GeometryNodePointsToVolume": {
        "display_name": "Points to Volume",
        "category": "Point",
        "description": "Creates volume from point cloud - each point becomes a density blob, overlapping areas merge.",
        "common_uses": [
            "Metaball-like blobby shapes",
            "Fog/cloud from particles",
            "Soft organic forms"
        ],
        "pitfalls": [
            "Point Radius controls blob size",
            "Resolution: voxels per unit (higher = more detail, slower)",
            "Output is volume (use Volume to Mesh for solid)"
        ],
        "commonly_used_with": [
            ("Set Point Radius", "control blob sizes"),
            ("Volume to Mesh", "convert to solid mesh"),
            ("Distribute Points", "scatter source points"),
            ("Set Material", "Principled Volume shader")
        ],
        "example": "Metaball effect: scattered points + Set Point Radius (varied) → Points to Volume → Volume to Mesh. Overlapping radii merge smoothly. Fog particles: Points to Volume + volume shader."
    },
    
    # ==========================================================================
    # COLOR NODES
    # ==========================================================================
    
    "ShaderNodeValToRGB": {
        "display_name": "Color Ramp",
        "category": "Color",
        "description": "Converts values to colors via customizable gradient - the universal value-to-color converter.",
        "common_uses": [
            "Height-based terrain coloring",
            "Visualize data as colors",
            "Contrast/threshold control"
        ],
        "pitfalls": [
            "Input expects 0-1 range (use Map Range)",
            "Color stops define gradient points",
            "Constant interpolation = hard bands"
        ],
        "commonly_used_with": [
            ("Map Range", "normalize input to 0-1"),
            ("Noise Texture", "colorize noise"),
            ("Position", "height-based coloring"),
            ("Store Named Attribute", "save as vertex color")
        ],
        "example": "Terrain colors: Z position → Map Range (min elevation, max elevation to 0,1) → Color Ramp with green at 0, brown at 0.5, white at 1.0. Move stops closer for sharper transitions."
    },
    
    "ShaderNodeSeparateColor": {
        "display_name": "Separate Color",
        "category": "Color",
        "description": "Splits color into channels - RGB, HSV, or HSL modes for different use cases.",
        "common_uses": [
            "Extract individual channels",
            "Modify hue/saturation separately",
            "Color-based selection (by channel)"
        ],
        "pitfalls": [
            "Mode: RGB (0-1), HSV (H:0-1, S:0-1, V:0-1), HSL",
            "Hue is cyclic (0 and 1 are same red)",
            "Alpha output separate from color channels"
        ],
        "commonly_used_with": [
            ("Combine Color", "reassemble after modification"),
            ("Math", "adjust single channel"),
            ("Compare", "select by channel value"),
            ("Map Range", "remap channel range")
        ],
        "example": "Desaturate: Separate HSV → set S to 0 → Combine. Shift hue: Separate HSV → add to H → Combine. Extract brightness: V channel from HSV."
    },
    
    "ShaderNodeCombineColor": {
        "display_name": "Combine Color",
        "category": "Color",
        "description": "Builds color from channel values - RGB, HSV, or HSL assembly.",
        "common_uses": [
            "Procedural color creation",
            "Reassemble after channel modification",
            "Random/calculated colors"
        ],
        "pitfalls": [
            "Mode must match your values (RGB vs HSV vs HSL)",
            "Values typically 0-1 range",
            "No alpha input (use Set Material for alpha)"
        ],
        "commonly_used_with": [
            ("Separate Color", "modify and recombine"),
            ("Random Value", "random color components"),
            ("Noise Texture", "procedural color variation"),
            ("Store Named Attribute", "save as vertex color")
        ],
        "example": "Random colors: Random H (0-1), fixed S (0.8), fixed V (0.9) → Combine HSV = varied hues, consistent saturation. Gradient: Map Range → R channel, constants for G, B."
    },
    
    "ShaderNodeRGBCurve": {
        "display_name": "RGB Curves",
        "category": "Color",
        "description": "Color correction via curve controls - like Photoshop Curves for procedural colors.",
        "common_uses": [
            "Contrast adjustment",
            "Color grading",
            "Per-channel color correction"
        ],
        "pitfalls": [
            "C curve: affects all channels (master)",
            "R/G/B curves: individual channel control",
            "Fac input blends with original"
        ],
        "commonly_used_with": [
            ("Noise Texture", "contrast/remap noise"),
            ("Image Texture", "color correct images"),
            ("Store Named Attribute", "save adjusted color"),
            ("Mix", "blend adjusted with original")
        ],
        "example": "Increase contrast: S-curve on C channel. Warm tint: lift R curve, lower B curve. Crush blacks: pull bottom-left of C curve up. More control than Color Ramp for color adjustment."
    },
    
    # ==========================================================================
    # ROTATION NODES (from Blender 5.0 Manual)
    # ==========================================================================
    
    "FunctionNodeEulerToRotation": {
        "display_name": "Euler to Rotation",
        "category": "Rotation",
        "description": "Converts XYZ angle values to Rotation type - standard rotation creation from angles.",
        "common_uses": [
            "Create rotation from angle values",
            "Animated rotations via Scene Time",
            "User-controllable rotation input"
        ],
        "pitfalls": [
            "Input is RADIANS (π = 180°)",
            "Use Math (Radians) to convert from degrees",
            "Gimbal lock possible at certain angles"
        ],
        "commonly_used_with": [
            ("Rotate Instances", "apply the rotation"),
            ("Combine XYZ", "build euler from components"),
            ("Math (Radians)", "convert degrees to radians"),
            ("Scene Time", "animated rotation")
        ],
        "example": "Spin animation: (0, 0, Seconds × 2) as Euler → Euler to Rotation. 45° tilt: use π/4 (≈0.785) or Radians(45). XYZ order matters for complex rotations."
    },
    
    "FunctionNodeRotationToEuler": {
        "display_name": "Rotation to Euler",
        "category": "Rotation",
        "description": "Extracts XYZ angles from Rotation type - for reading/modifying rotation components.",
        "common_uses": [
            "Read individual rotation angles",
            "Modify then reconstruct rotation",
            "Debug rotation values"
        ],
        "pitfalls": [
            "Output is RADIANS",
            "Multiple valid Euler representations exist",
            "Use Math (Degrees) to convert for display"
        ],
        "commonly_used_with": [
            ("Instance Rotation", "read instance orientation"),
            ("Separate XYZ", "get individual angles"),
            ("Euler to Rotation", "after modification"),
            ("Math (Degrees)", "human-readable output")
        ],
        "example": "Add to Z rotation: Rotation to Euler → Separate XYZ → add to Z → Combine XYZ → Euler to Rotation. Read angles: → Degrees for display values."
    },
    
    "FunctionNodeAxisAngleToRotation": {
        "display_name": "Axis Angle to Rotation",
        "category": "Rotation",
        "description": "Creates rotation from axis vector + angle - rotate around any arbitrary direction.",
        "common_uses": [
            "Rotate around surface normal",
            "Custom pivot axis rotation",
            "Procedural orientation"
        ],
        "pitfalls": [
            "Axis should be normalized (length 1)",
            "Angle is in radians",
            "Zero-length axis = no rotation"
        ],
        "commonly_used_with": [
            ("Normal", "rotate around surface"),
            ("Vector Math (Normalize)", "ensure valid axis"),
            ("Rotate Instances", "apply rotation"),
            ("Random Value", "random angle amount")
        ],
        "example": "Spin around normal: Normal as Axis, Random angle → Axis Angle to Rotation. More intuitive than Euler for 'rotate around this direction' scenarios."
    },
    
    "FunctionNodeInvertRotation": {
        "display_name": "Invert Rotation",
        "category": "Rotation",
        "description": "Returns opposite rotation - applying inverted rotation undoes the original.",
        "common_uses": [
            "Undo a rotation transform",
            "Calculate relative rotation",
            "Counter-rotate for alignment"
        ],
        "pitfalls": [
            "Invert(R) × R = no rotation (identity)",
            "Not same as negating angles",
            "Order matters when combining"
        ],
        "commonly_used_with": [
            ("Rotate Rotation", "combine with other rotations"),
            ("Instance Rotation", "read then invert"),
            ("Transform Geometry", "inverse transform"),
            ("Align Euler to Vector", "counter-rotation")
        ],
        "example": "Undo rotation: Original × Invert(Original) = identity. Counter-rotate child to keep world-aligned despite parent rotation."
    },
    
    "FunctionNodeRotateRotation": {
        "display_name": "Rotate Rotation",
        "category": "Rotation",
        "description": "Combines two rotations - applies one rotation on top of another.",
        "common_uses": [
            "Add rotation offset to existing",
            "Layer multiple rotations",
            "Relative rotation adjustments"
        ],
        "pitfalls": [
            "Order matters: A then B ≠ B then A",
            "Rotate By: the additional rotation",
            "Different from adding Euler angles"
        ],
        "commonly_used_with": [
            ("Instance Rotation", "read current, add offset"),
            ("Euler to Rotation", "create offset rotation"),
            ("Random Value", "random rotation offset"),
            ("Rotate Instances", "apply combined result")
        ],
        "example": "Random tilt on aligned: Align to Normal → Rotate Rotation (add random Z spin). Stack rotations: base orientation + animated offset."
    },
    
    # ==========================================================================
    # CURVE READ NODES
    # ==========================================================================
    
    "GeometryNodeInputCurveTangent": {
        "display_name": "Curve Tangent",
        "category": "Curve Read",
        "description": "Returns curve direction at each point - the 'forward' vector along the path.",
        "common_uses": [
            "Orient instances along curve",
            "Calculate flow direction",
            "Align objects to path"
        ],
        "pitfalls": [
            "Output is normalized (length 1)",
            "Reverse Curve flips tangent direction",
            "Smooth curves have interpolated tangents"
        ],
        "commonly_used_with": [
            ("Align Euler to Vector", "create rotation from direction"),
            ("Instance on Points", "oriented scatter"),
            ("Vector Math (Cross)", "calculate perpendicular"),
            ("Curve to Points", "also outputs tangent")
        ],
        "example": "Arrows along path: Instance on Points → Align Euler to Vector (Tangent as direction). Calculate curve 'right' direction: Tangent × (0,0,1) = perpendicular vector."
    },
    
    "GeometryNodeCurveLength": {
        "display_name": "Curve Length",
        "category": "Curve Read",
        "description": "Returns total length of all splines combined - single value for entire curve geometry.",
        "common_uses": [
            "Calculate total path distance",
            "Determine spacing count",
            "Proportional effects by length"
        ],
        "pitfalls": [
            "Single value (not per-point)",
            "All splines summed together",
            "Use Spline Length for per-spline values"
        ],
        "commonly_used_with": [
            ("Math (Divide)", "spacing calculation"),
            ("Resample Curve", "points based on length"),
            ("Spline Length", "individual spline lengths"),
            ("Trim Curve", "length-based trim")
        ],
        "example": "Even spacing: Curve Length ÷ spacing = point count → Resample. Trees every 10m: Curve Length ÷ 10 = tree count."
    },
    
    "GeometryNodeInputCurveTilt": {
        "display_name": "Curve Tilt",
        "category": "Curve Read",
        "description": "Reads tilt angle at each curve point - rotation around tangent axis.",
        "common_uses": [
            "Read existing tilt values",
            "Tilt-based effects",
            "Profile twist analysis"
        ],
        "pitfalls": [
            "Value in radians (π = 180° twist)",
            "Only visible with Curve to Mesh + profile",
            "Per-point value (not per-spline)"
        ],
        "commonly_used_with": [
            ("Set Curve Tilt", "modify tilt values"),
            ("Curve to Mesh", "tilt rotates profile"),
            ("Math (Add)", "add to existing tilt"),
            ("Map Range", "rescale tilt values")
        ],
        "example": "Read and modify: Curve Tilt + (Spline Parameter × 2π) → Set Curve Tilt = one full twist added. Current tilt as base for relative adjustments."
    },
    
    "GeometryNodeInputSplineResolution": {
        "display_name": "Spline Resolution",
        "category": "Curve Read",
        "description": "Reads resolution setting per spline - smoothness for Bezier/NURBS evaluation.",
        "common_uses": [
            "Read curve quality settings",
            "Resolution-based filtering",
            "Conditional processing"
        ],
        "pitfalls": [
            "Only affects Bezier/NURBS (Poly ignores)",
            "Per-spline value (not per-point)",
            "Higher = smoother, more geometry"
        ],
        "commonly_used_with": [
            ("Set Spline Resolution", "modify resolution"),
            ("Compare", "filter by quality"),
            ("Curve to Mesh", "resolution affects output"),
            ("Is Viewport", "LOD switching")
        ],
        "example": "Quality check: Spline Resolution < 8 selection for low-quality curves. Read before conditionally increasing for render."
    },
    
    "GeometryNodeInputSplineCyclic": {
        "display_name": "Is Spline Cyclic",
        "category": "Curve Read",
        "description": "Returns True if spline is closed loop, False if open-ended.",
        "common_uses": [
            "Detect closed vs open curves",
            "Conditional processing by curve type",
            "Filter curves for Fill Curve"
        ],
        "pitfalls": [
            "Per-spline boolean (not per-point)",
            "Cyclic = end connects to start (no gap)",
            "Fill Curve works best on cyclic curves"
        ],
        "commonly_used_with": [
            ("Set Spline Cyclic", "open/close curves"),
            ("Fill Curve", "only fills cyclic properly"),
            ("Separate Geometry", "split open from closed"),
            ("Curve to Mesh", "cyclic affects end caps")
        ],
        "example": "Filter for Fill: Is Spline Cyclic → Separate Geometry → Fill only closed curves. Check imported curves: some may be open when expected closed."
    },
    
    "GeometryNodeCurveEndpointSelection": {
        "display_name": "Endpoint Selection",
        "category": "Curve Read",
        "description": "Selects points at curve start/end - for endpoint-specific operations.",
        "common_uses": [
            "Place objects at curve ends",
            "Select hair/strand tips",
            "Apply effects to endpoints"
        ],
        "pitfalls": [
            "Start/End Size: how many points from each end",
            "Size 1 = just first/last point",
            "No effect on cyclic curves (no true endpoints)"
        ],
        "commonly_used_with": [
            ("Instance on Points", "caps/markers at ends"),
            ("Set Position", "move endpoints"),
            ("Set Curve Radius", "tapered tips"),
            ("Delete Geometry", "trim from ends")
        ],
        "example": "Hair tips: Endpoint Selection (Start 0, End 1) = select only end points. Cap markers: selection → Instance on Points with sphere. Tapered ends: use as weight for radius."
    },
    
    "GeometryNodeCurveHandleTypeSelection": {
        "display_name": "Handle Type Selection",
        "category": "Curve Read",
        "description": "Selects Bezier points by handle type - Free, Auto, Vector, or Align.",
        "common_uses": [
            "Find sharp corners (Vector handles)",
            "Select smooth points (Auto handles)",
            "Filter by handle configuration"
        ],
        "pitfalls": [
            "Only works on Bezier curves (not Poly/NURBS)",
            "Mode: Left, Right, or Both handles",
            "Handle Type: which type to match"
        ],
        "commonly_used_with": [
            ("Set Handle Type", "change matched handles"),
            ("Set Handle Positions", "adjust selected handles"),
            ("Separate Geometry", "split by handle type"),
            ("Delete Geometry", "remove specific points")
        ],
        "example": "Find corners: Handle Type Selection (Vector) = sharp points. Find smooth: Handle Type Selection (Auto) = smooth curves. Convert selected via Set Handle Type."
    },
    
    # ==========================================================================
    # CURVE WRITE NODES
    # ==========================================================================
    
    "GeometryNodeSetCurveTilt": {
        "display_name": "Set Curve Tilt",
        "category": "Curve Write",
        "description": "Sets twist angle per curve point - rotates profile in Curve to Mesh.",
        "common_uses": [
            "Twisted ribbon/tape",
            "Spiral tube effect",
            "Rollercoaster banking"
        ],
        "pitfalls": [
            "Value in radians (2π = full rotation)",
            "Only visible with Curve to Mesh + profile",
            "Per-point value (varies along curve)"
        ],
        "commonly_used_with": [
            ("Spline Parameter", "position-based twist"),
            ("Curve to Mesh", "visualize tilt"),
            ("Math (Multiply)", "control twist amount"),
            ("Noise Texture", "organic twist variation")
        ],
        "example": "One full twist: Spline Parameter × 2π (6.28) → Set Curve Tilt. DNA helix: Spline Parameter × 4π = two full rotations. Ribbon: gradual tilt change along length."
    },
    
    "GeometryNodeSetSplineCyclic": {
        "display_name": "Set Spline Cyclic",
        "category": "Curve Write",
        "description": "Opens or closes curves - True connects end to start, False leaves gap.",
        "common_uses": [
            "Close open curves into loops",
            "Open closed shapes",
            "Toggle for Fill Curve compatibility"
        ],
        "pitfalls": [
            "Doesn't add/remove points",
            "Only changes topology connection",
            "Fill Curve requires cyclic curves"
        ],
        "commonly_used_with": [
            ("Fill Curve", "must be cyclic to fill"),
            ("Is Spline Cyclic", "read before changing"),
            ("Curve to Mesh", "cyclic = no end caps"),
            ("Curve Line", "close into triangle/polygon")
        ],
        "example": "Close line into loop: Set Spline Cyclic (True). Open circle: Set Spline Cyclic (False) = C-shape with gap. Required before Fill Curve for solid shapes."
    },
    
    "GeometryNodeSetSplineResolution": {
        "display_name": "Set Spline Resolution",
        "category": "Curve Write",
        "description": "Controls Bezier/NURBS curve smoothness - segments between control points.",
        "common_uses": [
            "Curve quality control",
            "Performance optimization",
            "Per-curve detail levels"
        ],
        "pitfalls": [
            "Only affects Bezier and NURBS (Poly ignores)",
            "Higher = smoother but more geometry",
            "Default is 12 segments between points"
        ],
        "commonly_used_with": [
            ("Curve to Mesh", "resolution affects tube smoothness"),
            ("Resample Curve", "alternative: fixed point count"),
            ("Is Viewport", "lower resolution for preview"),
            ("Spline Resolution", "read current value")
        ],
        "example": "Preview optimization: Is Viewport → Switch (6 vs 24 resolution). Smooth tubes: Set Resolution 24+ before Curve to Mesh. Poly curves don't use resolution."
    },
    
    "GeometryNodeSetCurveNormal": {
        "display_name": "Set Curve Normal",
        "category": "Curve Write",
        "description": "Controls curve normal calculation method - affects profile orientation in Curve to Mesh.",
        "common_uses": [
            "Fix twisted tube profiles",
            "Consistent ribbon orientation",
            "Control up-direction along curve"
        ],
        "pitfalls": [
            "Minimum Twist: least rotation overall",
            "Z-Up: normal points toward world Z",
            "Free: uses Tilt only"
        ],
        "commonly_used_with": [
            ("Curve to Mesh", "normal orients profile"),
            ("Set Curve Tilt", "additional twist control"),
            ("Curve Normal", "read resulting normal"),
            ("Align Euler to Vector", "align instances to normal")
        ],
        "example": "Fix twisted ribbon: Set Curve Normal (Minimum Twist). Railroad tracks: Set Curve Normal (Z-Up) keeps sleepers level. Rollercoaster: Minimum Twist + Set Tilt for banking."
    },
    
    # ==========================================================================
    # CURVE SAMPLE NODE
    # ==========================================================================
    
    "GeometryNodeSampleCurve": {
        "display_name": "Sample Curve",
        "category": "Curve",
        "description": "Gets position, tangent, and normal at any point along curve - by factor (0-1) or length.",
        "common_uses": [
            "Object following curve path",
            "Position at curve percentage",
            "Animated path movement"
        ],
        "pitfalls": [
            "Factor: 0 = start, 0.5 = middle, 1 = end",
            "Length: actual distance in scene units",
            "Curve Index: which spline to sample"
        ],
        "commonly_used_with": [
            ("Scene Time", "animated path following"),
            ("Object Info", "get curve from object"),
            ("Transform Geometry", "position at sampled point"),
            ("Align Euler to Vector", "orient using Tangent output")
        ],
        "example": "Path animation: Scene Time × speed as Factor → Sample Curve → use Position for object location, Tangent for orientation. Sample at 0.5 = exact midpoint."
    },
    
    # ==========================================================================
    # CURVE OPERATIONS (additional)
    # ==========================================================================
    
    "GeometryNodeReverseCurve": {
        "display_name": "Reverse Curve",
        "category": "Curve Operations",
        "description": "Swaps curve start and end - flips direction without changing shape.",
        "common_uses": [
            "Fix inside-out tube normals",
            "Reverse animation direction",
            "Flip taper direction"
        ],
        "pitfalls": [
            "Shape unchanged, only direction flips",
            "Tangent, Normal outputs flip direction",
            "Spline Parameter 0↔1 swaps meaning"
        ],
        "commonly_used_with": [
            ("Curve to Mesh", "reverse profile = flip normals"),
            ("Spline Parameter", "now counts from other end"),
            ("Trim Curve", "start/end interpretation changes"),
            ("Set Curve Radius", "taper direction reverses")
        ],
        "example": "Fix inverted tube: Reverse Curve on profile before Curve to Mesh. Reverse taper: if thick-to-thin becomes thin-to-thick, reverse the curve."
    },
    
    "GeometryNodeInterpolateCurves": {
        "display_name": "Interpolate Curves",
        "category": "Curve Operations",
        "description": "Generates curves blending between guide curves - for hair/fur systems.",
        "common_uses": [
            "Hair from sparse guides",
            "Fur generation",
            "Fill between guide strands"
        ],
        "pitfalls": [
            "Guide Curves: sparse control strands",
            "Points: where to generate new curves",
            "Guide Index: which guides influence each point"
        ],
        "commonly_used_with": [
            ("Distribute Points on Faces", "generation points"),
            ("Curve primitives", "guide curves"),
            ("Set Curve Radius", "tapered strands"),
            ("Deform Curves on Surface", "animate with mesh")
        ],
        "example": "Hair system: few guide curves + many distributed points → Interpolate Curves blends shapes. More guides = better shape control. Guide Index assigns influence regions."
    },
    
    "GeometryNodeDeformCurvesOnSurface": {
        "display_name": "Deform Curves on Surface",
        "category": "Curve Operations",
        "description": "Attaches curves to mesh surface - curves follow surface deformation.",
        "common_uses": [
            "Hair on animated characters",
            "Fur following mesh deformation",
            "Surface-attached effects"
        ],
        "pitfalls": [
            "Surface needs UV coordinates",
            "Curves need surface_uv_coordinate attribute",
            "Only works with mesh surfaces"
        ],
        "commonly_used_with": [
            ("Interpolate Curves", "generate attached hair"),
            ("Object Info", "animated surface mesh"),
            ("Curve to Mesh", "render attached curves"),
            ("Set Curve Radius", "hair thickness")
        ],
        "example": "Character hair: generate curves on rest pose → Deform Curves on Surface with animated mesh = hair follows movement. UV coordinates track attachment points."
    },
    
    # ==========================================================================
    # GEOMETRY OPERATIONS (additional)
    # ==========================================================================
    
    "GeometryNodeDuplicateElements": {
        "display_name": "Duplicate Elements",
        "category": "Geometry",
        "description": "Creates copies of selected elements - faces, points, edges, splines, or instances.",
        "common_uses": [
            "Create arrays from elements",
            "Duplicate for offset patterns",
            "Per-face or per-point copies"
        ],
        "pitfalls": [
            "Domain: what element type to duplicate",
            "Amount: copies per element (can vary)",
            "Duplicate Index output: 0=original, 1=first copy..."
        ],
        "commonly_used_with": [
            ("Set Position", "offset using Duplicate Index"),
            ("Random Value", "varied duplicate transforms"),
            ("Scale Elements", "scale copies differently"),
            ("Extrude Mesh", "alternative for face copies")
        ],
        "example": "Stacked copies: Duplicate (Amount 5) → Set Position Z = Duplicate Index × spacing. Radial array: Rotate by Duplicate Index × (360°/Amount). Each original spawns Amount copies."
    },
    
    "GeometryNodeGeometryToInstance": {
        "display_name": "Geometry to Instance",
        "category": "Geometry",
        "description": "Packages geometry as instance - efficient for repeated use with Instance on Points.",
        "common_uses": [
            "Prepare procedural geometry for instancing",
            "Optimize repeated geometry",
            "Create instanceable from node output"
        ],
        "pitfalls": [
            "Output is instance (not mesh)",
            "Realize Instances to convert back",
            "Multiple inputs become one merged instance"
        ],
        "commonly_used_with": [
            ("Instance on Points", "scatter the package"),
            ("Join Geometry", "combine before packaging"),
            ("Realize Instances", "unpack when needed"),
            ("Object Info (As Instance)", "alternative approach")
        ],
        "example": "Procedural scatter: Complex procedural mesh → Geometry to Instance → Instance on Points. Thousands of copies share same data = memory efficient vs duplicating all vertices."
    },
    
    "GeometryNodeSeparateComponents": {
        "display_name": "Separate Components",
        "category": "Geometry",
        "description": "Splits mixed geometry into typed outputs - Mesh, Curve, Point Cloud, Volume, Instances.",
        "common_uses": [
            "Extract specific geometry type",
            "Process components separately",
            "Filter after Join Geometry"
        ],
        "pitfalls": [
            "Each output contains only that type",
            "Empty output if type not present",
            "Doesn't separate by mesh islands (use Separate Geometry)"
        ],
        "commonly_used_with": [
            ("Join Geometry", "then separate for type-specific ops"),
            ("Realize Instances", "before separating"),
            ("Curve/Mesh operations", "on specific type"),
            ("Switch", "select which component to use")
        ],
        "example": "Mixed geometry processing: Join various geo → Separate Components → apply Subdivision to Mesh only, Resample to Curves only → Join back. Type-specific operations on mixed input."
    },
    
    "GeometryNodeSortElements": {
        "display_name": "Sort Elements",
        "category": "Geometry",
        "description": "Reorders elements by sort key value - changes Index order.",
        "common_uses": [
            "Sort points by position",
            "Order for Points to Curves",
            "Z-sorting for rendering"
        ],
        "pitfalls": [
            "Changes element indices",
            "Group ID: keep groups together while sorting",
            "Affects Index node output"
        ],
        "commonly_used_with": [
            ("Position (X/Y/Z)", "sort by location"),
            ("Points to Curves", "needs ordered points"),
            ("Index", "read new order"),
            ("Noise Texture", "random sort key")
        ],
        "example": "Left-to-right curve: Sort by Position.X → Points to Curves. Per-group sort: Mesh Island as Group ID, Position.Z as Sort Key. Affects subsequent Index values."
    },
    
    "GeometryNodeSplitToInstances": {
        "display_name": "Split to Instances",
        "category": "Geometry",
        "description": "Separates geometry by Group ID into individual instances - for per-group transforms.",
        "common_uses": [
            "Split islands for independent transform",
            "Explode effects",
            "Per-material separation"
        ],
        "pitfalls": [
            "Group ID determines splits (unique ID = instance)",
            "Output is instances (not mesh)",
            "Use Realize Instances to convert back"
        ],
        "commonly_used_with": [
            ("Mesh Island", "Island Index as Group ID"),
            ("Material Index", "split by material"),
            ("Rotate/Scale/Translate Instances", "transform pieces"),
            ("Realize Instances", "back to mesh")
        ],
        "example": "Explode: Mesh Island as Group ID → Split to Instances → Translate Instances (outward). Each island becomes independent instance for separate animation."
    },
    
    # ==========================================================================
    # INSTANCE NODES (additional)
    # ==========================================================================
    
    "GeometryNodeInstanceTransform": {
        "display_name": "Instance Transform",
        "category": "Instances",
        "description": "Reads full 4×4 transformation matrix of instances - combined position/rotation/scale.",
        "common_uses": [
            "Copy entire transform",
            "Matrix-based calculations",
            "Advanced transform manipulation"
        ],
        "pitfalls": [
            "Output is 4×4 matrix (not separate values)",
            "Use Instance Rotation/Scale for components",
            "Only valid in Instance domain"
        ],
        "commonly_used_with": [
            ("Set Instance Transform", "apply matrix"),
            ("Instance Rotation", "just rotation component"),
            ("Instance Scale", "just scale component"),
            ("Matrix math nodes", "combine/modify")
        ],
        "example": "Copy transform: Instance Transform → Set Instance Transform on other instances. For most uses, prefer Translate/Rotate/Scale Instances nodes instead."
    },
    
    "GeometryNodeSetInstanceTransform": {
        "display_name": "Set Instance Transform",
        "category": "Instances",
        "description": "Sets full 4×4 transformation matrix - replaces position/rotation/scale in one operation.",
        "common_uses": [
            "Apply copied transforms",
            "Matrix-based positioning",
            "Complex transform operations"
        ],
        "pitfalls": [
            "Replaces entire transform (not additive)",
            "Input is 4×4 matrix",
            "For simple ops, use Translate/Rotate/Scale nodes"
        ],
        "commonly_used_with": [
            ("Instance Transform", "copy from other instances"),
            ("Combine Transform", "build matrix from components"),
            ("Invert Transform", "undo transform"),
            ("Multiply Matrices", "combine transforms")
        ],
        "example": "Copy instance transform: Instance Transform from source → Set Instance Transform on target. Matrix workflow for advanced animation/rigging scenarios."
    },
    
    "GeometryNodeInputInstanceRotation": {
        "display_name": "Instance Rotation",
        "category": "Instances",
        "description": "Reads current rotation of each instance - for relative rotation modifications.",
        "common_uses": [
            "Read existing instance orientation",
            "Relative rotation adjustments",
            "Rotation-based filtering"
        ],
        "pitfalls": [
            "Output is Rotation type (not Euler)",
            "Use Rotation to Euler for angle values",
            "Only meaningful on instance geometry"
        ],
        "commonly_used_with": [
            ("Rotate Rotation", "add to current rotation"),
            ("Rotate Instances", "apply modified rotation"),
            ("Rotation to Euler", "extract angles"),
            ("Compare", "filter by orientation")
        ],
        "example": "Relative rotation: Instance Rotation → Rotate Rotation (add offset) → Rotate Instances. Spin existing: read current, add animated rotation, apply back."
    },
    
    "GeometryNodeInputInstanceScale": {
        "display_name": "Instance Scale",
        "category": "Instances",
        "description": "Reads current scale of each instance - for relative size modifications.",
        "common_uses": [
            "Read existing instance sizes",
            "Relative scale adjustments",
            "Size-based filtering"
        ],
        "pitfalls": [
            "Output is Vector (X, Y, Z scale)",
            "1.0 = original size",
            "Only meaningful on instance geometry"
        ],
        "commonly_used_with": [
            ("Vector Math (Multiply)", "relative scaling"),
            ("Scale Instances", "apply modified scale"),
            ("Separate XYZ", "individual axis scale"),
            ("Compare", "filter by size")
        ],
        "example": "Grow 20%: Instance Scale × 1.2 → Scale Instances. Clamp large: if Instance Scale > 2 then limit. Read to adjust material based on instance size."
    },
    
    # ==========================================================================
    # FIELD UTILITY NODES
    # ==========================================================================
    
    "GeometryNodeAccumulateField": {
        "display_name": "Accumulate Field",
        "category": "Field",
        "description": "Running total of values - cumulative sum for stacking and sequences.",
        "common_uses": [
            "Stack objects by varying heights",
            "Cumulative positioning",
            "Running totals and sequences"
        ],
        "pitfalls": [
            "Leading: sum of previous elements (starts at 0)",
            "Trailing: sum including current element",
            "Group Index: separate accumulations per group"
        ],
        "commonly_used_with": [
            ("Random Value", "varied stacking heights"),
            ("Set Position", "use Leading as Z offset"),
            ("Index", "ordered accumulation"),
            ("Mesh Island", "as Group Index")
        ],
        "example": "Stack boxes: each box has random height stored. Accumulate (Leading) = sum of heights below. Set Position Z = Leading. Box 1 at Z=0, Box 2 at Z=height1, Box 3 at Z=height1+height2."
    },
    
    "GeometryNodeFieldAtIndex": {
        "display_name": "Evaluate at Index",
        "category": "Field",
        "description": "Retrieves field value from specific element by index - lookup in current geometry.",
        "common_uses": [
            "Access neighbor element data",
            "Copy value from specific element",
            "Cross-reference by index"
        ],
        "pitfalls": [
            "Uses context geometry (no geometry input)",
            "Similar to Sample Index but no separate geometry",
            "Index out of range = undefined behavior"
        ],
        "commonly_used_with": [
            ("Edge Vertices", "get connected vertex indices"),
            ("Index", "current or offset index"),
            ("Position", "commonly sampled field"),
            ("Math", "calculate target index")
        ],
        "example": "Get previous vertex position: Evaluate at Index (Index - 1, Position). Access neighbor: Edge Vertices gives vertex indices, evaluate Position at those indices."
    },
    
    "GeometryNodeFieldOnDomain": {
        "display_name": "Evaluate on Domain",
        "category": "Field",
        "description": "Evaluates field on different domain - converts between Point, Edge, Face, Corner contexts.",
        "common_uses": [
            "Use face data on vertices",
            "Access vertex values from faces",
            "Cross-domain calculations"
        ],
        "pitfalls": [
            "Interpolation: Face→Vertex averages touching faces",
            "Vertex→Face uses face's first vertex or average",
            "Domain dropdown selects evaluation context"
        ],
        "commonly_used_with": [
            ("Face Area", "access on Point domain"),
            ("Index", "domain-specific index"),
            ("Normal", "face normal on vertices"),
            ("Position", "evaluated in different context")
        ],
        "example": "Face area per vertex: Face Area → Evaluate on Domain (Point) = each vertex gets average area of connected faces. Smooth selection: edge selection evaluated on faces."
    },
    
    "GeometryNodeFieldAverage": {
        "display_name": "Field Average",
        "category": "Field",
        "description": "Calculates mean value across all elements - single average or per-group averages.",
        "common_uses": [
            "Find geometry center",
            "Average attribute value",
            "Per-island centers"
        ],
        "pitfalls": [
            "Returns one value (or one per group)",
            "Group Index: separate averages per group",
            "Different from Blur (neighbor average) - this is global"
        ],
        "commonly_used_with": [
            ("Position", "find center point"),
            ("Mesh Island", "per-island average"),
            ("Set Position", "center geometry"),
            ("Math (Subtract)", "offset from average")
        ],
        "example": "Center geometry: Position average → subtract from all positions. Per-island centers: Mesh Island Index as Group → Position average gives each island's center separately."
    },
    
    # ==========================================================================
    # REPEAT ZONE
    # ==========================================================================
    
    "GeometryNodeRepeatInput": {
        "display_name": "Repeat Zone",
        "category": "Utilities",
        "description": "Loops operations multiple times in single frame - iterative/fractal patterns.",
        "common_uses": [
            "Iterative subdivision",
            "Fractal generation",
            "Repeated transformations"
        ],
        "pitfalls": [
            "All iterations run instantly (not animated)",
            "Iteration output: current loop number (0 to N-1)",
            "High iterations = slow performance"
        ],
        "commonly_used_with": [
            ("Transform Geometry", "repeated transforms"),
            ("Subdivide Mesh", "iterative subdivision"),
            ("Extrude Mesh", "repeated extrusion"),
            ("Simulation Zone", "alternative for frame-by-frame")
        ],
        "example": "Fractal: Repeat 5× → Subdivide + random displacement each iteration. Spiral: Repeat → rotate + translate each iteration. Each loop uses previous result."
    },
    
    # ==========================================================================
    # FOR EACH ZONE
    # ==========================================================================
    
    "GeometryNodeForEachGeometryElementInput": {
        "display_name": "For Each Element Zone",
        "category": "Utilities",
        "description": "Processes each element individually - per-face/per-point operations.",
        "common_uses": [
            "Per-element processing",
            "Individual face operations",
            "Complex per-item logic"
        ],
        "pitfalls": [
            "Slow for many elements (use bulk operations when possible)",
            "Each element processed separately",
            "Element Index available inside zone"
        ],
        "commonly_used_with": [
            ("Extrude Mesh", "per-face extrusion variations"),
            ("Transform Geometry", "per-element transform"),
            ("Random Value", "per-element randomness"),
            ("Boolean", "per-element operations")
        ],
        "example": "Per-face random extrusion: For Each Face → Extrude with random height. Operations impossible with bulk nodes - each element gets full node tree processing."
    },
    
    # ==========================================================================
    # VECTOR NODES
    # ==========================================================================
    
    "ShaderNodeVectorRotate": {
        "display_name": "Vector Rotate",
        "category": "Vector",
        "description": "Rotates vector around axis or point - for spinning positions/directions.",
        "common_uses": [
            "Rotate positions around axis",
            "Spin direction vectors",
            "Create circular patterns"
        ],
        "pitfalls": [
            "Angle in radians (π = 180°)",
            "Modes: Axis Angle, X/Y/Z Euler",
            "Center: rotation pivot point"
        ],
        "commonly_used_with": [
            ("Position", "rotate geometry positions"),
            ("Normal", "rotate direction vectors"),
            ("Scene Time", "animated rotation"),
            ("Math (Radians)", "convert from degrees")
        ],
        "example": "Rotate around Y: Vector Rotate (Axis Y, Angle) on Position. Radial pattern: Position → Vector Rotate by Index × (2π/count). Simpler than Transform Geometry for vector operations."
    },
    
    "ShaderNodeVectorCurve": {
        "display_name": "Vector Curves",
        "category": "Vector",
        "description": "Remaps vector components via curve controls - X, Y, Z adjusted independently.",
        "common_uses": [
            "Non-linear vector remapping",
            "Custom falloff shapes",
            "Artistic vector adjustment"
        ],
        "pitfalls": [
            "Separate curve per axis (X, Y, Z)",
            "Fac: blend with original vector",
            "Input range affects curve interpretation"
        ],
        "commonly_used_with": [
            ("Position", "position remapping"),
            ("Noise Texture", "shape noise output"),
            ("Normal", "normal adjustment"),
            ("Map Range", "pre-normalize input")
        ],
        "example": "Ease-in displacement: Position → Vector Curves (S-curve on Z). Custom falloff: shape noise output with curve. More control than Math for complex remapping."
    },
    
    "FunctionNodeRotateVector": {
        "display_name": "Rotate Vector",
        "category": "Vector",
        "description": "Rotates vector by Rotation value - applies rotation to direction/position.",
        "common_uses": [
            "Apply rotation to direction",
            "Transform positions by rotation",
            "Match instance orientation"
        ],
        "pitfalls": [
            "Rotation input (not Euler angles)",
            "Rotates around origin",
            "Use Euler to Rotation for angle input"
        ],
        "commonly_used_with": [
            ("Instance Rotation", "match instance orientation"),
            ("Euler to Rotation", "create rotation from angles"),
            ("Normal", "rotate direction vectors"),
            ("Position", "rotate positions")
        ],
        "example": "Transform normal by rotation: Normal → Rotate Vector (Instance Rotation) = normal in instance space. Offset in rotated direction: (0,1,0) → Rotate Vector = forward in rotated orientation."
    },
    
    # ==========================================================================
    # MATERIAL NODES (additional)
    # ==========================================================================
    
    "GeometryNodeReplaceMaterial": {
        "display_name": "Replace Material",
        "category": "Material",
        "description": "Swaps one material for another - find and replace for materials.",
        "common_uses": [
            "Material variations on imported models",
            "Batch material changes",
            "Procedural material swapping"
        ],
        "pitfalls": [
            "Only replaces exact material match",
            "Old material must exist on faces",
            "Doesn't modify material slots list"
        ],
        "commonly_used_with": [
            ("Object Info", "imported geometry"),
            ("Set Material", "alternative: assign directly"),
            ("Switch", "conditional replacement"),
            ("Material Selection", "check before replacing")
        ],
        "example": "Color variation: Replace Material (Red → Blue). Batch swap: chain multiple Replace Material nodes. Works on any geometry with materials assigned."
    },
    
    "GeometryNodeMaterialSelection": {
        "display_name": "Material Selection",
        "category": "Material",
        "description": "Selects faces by assigned material - boolean output for material-based operations.",
        "common_uses": [
            "Select faces with specific material",
            "Material-based effects",
            "Process only certain material areas"
        ],
        "pitfalls": [
            "Matches by material reference (pick from dropdown)",
            "Works on Face domain",
            "Different from Material Index (this uses actual material)"
        ],
        "commonly_used_with": [
            ("Delete Geometry", "remove by material"),
            ("Separate Geometry", "extract material group"),
            ("Extrude Mesh", "extrude specific material"),
            ("Set Position", "affect only that material")
        ],
        "example": "Extrude only windows: Material Selection (Glass) → Extrude. Remove labels: Material Selection (Label) → Delete Geometry. Works on imported models with materials."
    },
    
    "GeometryNodeSetMaterialIndex": {
        "display_name": "Set Material Index",
        "category": "Material",
        "description": "Assigns faces to material slot by index - 0 = first slot, 1 = second, etc.",
        "common_uses": [
            "Procedural multi-material",
            "Random material assignment",
            "Pattern-based materials"
        ],
        "pitfalls": [
            "Index = material slot number on object",
            "Materials must exist in object's slots",
            "Use Set Material for single material assignment"
        ],
        "commonly_used_with": [
            ("Random Value (Integer)", "random material per face"),
            ("Modulo", "repeating material pattern"),
            ("Mesh Island", "material per island"),
            ("Material Index", "read current assignment")
        ],
        "example": "Checkerboard materials: (floor(X) + floor(Y)) % 2 as Material Index (0 or 1). Random 3 materials: Random Integer (0-2) as Material Index. Object needs 3 material slots."
    },
    
    # ==========================================================================
    # MESH TOPOLOGY NODES
    # ==========================================================================
    
    "GeometryNodeCornersOfFace": {
        "display_name": "Corners of Face",
        "category": "Mesh Topology",
        "description": "Gets corner indices belonging to a face - for accessing per-corner data (UVs, vertex colors).",
        "common_uses": [
            "Access face corner UVs",
            "Per-corner vertex colors",
            "Face corner iteration"
        ],
        "pitfalls": [
            "Corner ≠ Vertex (corners are face-specific)",
            "Quad = 4 corners, Triangle = 3 corners",
            "Sort Index: which corner (0 to Total-1)"
        ],
        "commonly_used_with": [
            ("Sample Index", "read corner attribute"),
            ("Face Neighbors", "Vertex Count = corner count"),
            ("Store Named Attribute (Face Corner)", "save per-corner data"),
            ("Offset Corner in Face", "step through corners")
        ],
        "example": "Read first corner UV: Corners of Face (Sort Index 0) → Sample Index (UVMap). Iterate all corners using Sort Index 0 through Total-1."
    },
    
    "GeometryNodeCornersOfVertex": {
        "display_name": "Corners of Vertex",
        "category": "Mesh Topology",
        "description": "Gets all face corners touching a vertex - one corner per connected face.",
        "common_uses": [
            "Find faces around a vertex",
            "Access UVs at vertex from each face",
            "Vertex-to-face traversal"
        ],
        "pitfalls": [
            "Multiple corners per vertex (one per touching face)",
            "Sort Index selects which corner",
            "Total = number of faces touching vertex"
        ],
        "commonly_used_with": [
            ("Face of Corner", "get face from corner"),
            ("Sample Index", "read corner data"),
            ("Vertex Neighbors", "Face Count = Total"),
            ("Offset Corner in Face", "step around face")
        ],
        "example": "Faces around vertex: Corners of Vertex → Face of Corner = face indices. Center vertex in quad grid has 4 corners (4 touching faces)."
    },
    
    "GeometryNodeEdgesOfCorner": {
        "display_name": "Edges of Corner",
        "category": "Mesh Topology",
        "description": "Gets the two edges meeting at a face corner - previous and next edge indices.",
        "common_uses": [
            "Find edges around a corner",
            "Edge loop traversal",
            "Corner-to-edge topology"
        ],
        "pitfalls": [
            "Returns two edges: Previous and Next",
            "Direction follows face winding order",
            "Edge indices are mesh-wide (not face-local)"
        ],
        "commonly_used_with": [
            ("Corners of Face", "get corners first"),
            ("Edge Vertices", "get edge endpoints"),
            ("Sample Index", "read edge attributes"),
            ("Edge Angle", "edge properties")
        ],
        "example": "Edge loop: start at corner → Next Edge → other corner of edge → repeat. Previous/Next relative to face's winding direction (counter-clockwise typically)."
    },
    
    "GeometryNodeFaceOfCorner": {
        "display_name": "Face of Corner",
        "category": "Mesh Topology",
        "description": "Gets which face a corner belongs to - corner index to face index lookup.",
        "common_uses": [
            "Find face from corner",
            "Access face data from corner context",
            "Corner-to-face navigation"
        ],
        "pitfalls": [
            "Each corner belongs to exactly one face",
            "Index in Face: corner's position within face (0 to N-1)",
            "Reverse of Corners of Face"
        ],
        "commonly_used_with": [
            ("Sample Index", "read face attributes"),
            ("Face Area", "face size from corner"),
            ("Corners of Vertex", "corner → face path"),
            ("Face Neighbors", "face topology from corner")
        ],
        "example": "Corner to face data: Face of Corner → Sample Index (face attribute). Get corner position: Index in Face output (0 = first corner of face)."
    },
    
    "GeometryNodeOffsetCornerInFace": {
        "display_name": "Offset Corner in Face",
        "category": "Mesh Topology",
        "description": "Steps to adjacent corner within same face - navigate around face corners.",
        "common_uses": [
            "Find next/previous corner",
            "Cycle through face corners",
            "Compare adjacent UVs"
        ],
        "pitfalls": [
            "+1 = next corner (counter-clockwise typically)",
            "-1 = previous corner",
            "Wraps around: offset +4 on quad = same corner"
        ],
        "commonly_used_with": [
            ("Corners of Face", "get starting corner"),
            ("Sample Index", "read adjacent corner data"),
            ("Evaluate at Index", "compare corners"),
            ("Edges of Corner", "edges between corners")
        ],
        "example": "Compare UV seams: corner UV vs Offset(+1) UV - different values = UV seam. Walk face: start corner → offset +1 repeatedly to visit all corners."
    },
    
    # ==========================================================================
    # EDGE TOPOLOGY NODES
    # ==========================================================================
    
    "GeometryNodeEdgesOfVertex": {
        "display_name": "Edges of Vertex",
        "category": "Mesh Topology",
        "description": "Gets edges connected to a vertex - with optional sorting by weight.",
        "common_uses": [
            "Find connected edges",
            "Edge selection from vertex",
            "Sorted edge access"
        ],
        "pitfalls": [
            "Multiple edges per vertex possible",
            "Sort Index: which edge (0 to Total-1)",
            "Weight sorts results (e.g., by angle)"
        ],
        "commonly_used_with": [
            ("Vertex Neighbors", "Edge Count = Total"),
            ("Edge Angle", "as Weight for sorting"),
            ("Sample Index", "read edge attributes"),
            ("Edge Vertices", "traverse to other end")
        ],
        "example": "Steepest edge: Edge Angle as Weight → Sort Index 0 = sharpest edge. Interior vertex has 4 edges in quad grid."
    },
    
    "GeometryNodeVertexOfCorner": {
        "display_name": "Vertex of Corner",
        "category": "Mesh Topology",
        "description": "Gets which vertex a corner is attached to - corner to vertex index lookup.",
        "common_uses": [
            "Find vertex from corner",
            "Access vertex position from corner",
            "Corner-to-vertex navigation"
        ],
        "pitfalls": [
            "Each corner has exactly one vertex",
            "Multiple corners can share same vertex",
            "Reverse of Corners of Vertex"
        ],
        "commonly_used_with": [
            ("Evaluate at Index", "get vertex Position"),
            ("Sample Index", "read vertex attributes"),
            ("Corners of Vertex", "vertex → corners"),
            ("Position", "via vertex index lookup")
        ],
        "example": "Vertex position from corner: Vertex of Corner → Evaluate at Index (Position). Compare with corner UV to detect UV seams."
    },
    
    # ==========================================================================
    # SELECTION NODES
    # ==========================================================================
    
    "GeometryNodeBoxSelection": {
        "display_name": "Box Selection",
        "category": "Selection",
        "description": "Selects elements inside a rectangular box region - axis-aligned spatial filtering.",
        "common_uses": [
            "Select region by position",
            "Cut/clip geometry",
            "Rectangular spatial filter"
        ],
        "pitfalls": [
            "Box aligned to world axes (not rotated)",
            "Min/Max: opposite corners of box",
            "Use Transform Geometry first for angled boxes"
        ],
        "commonly_used_with": [
            ("Delete Geometry", "remove box region"),
            ("Separate Geometry", "extract box contents"),
            ("Boolean Math", "combine with other selections"),
            ("Object Info", "animated box position")
        ],
        "example": "Select ground floor: Min (-100,-100,0), Max (100,100,3). Clip to bounds: Delete Geometry with inverted Box Selection. Simpler than Compare + Boolean for rectangular regions."
    },
    
    "GeometryNodeSphereSelection": {
        "display_name": "Sphere Selection",
        "category": "Selection",
        "description": "Selects elements inside a spherical region - radial spatial filtering.",
        "common_uses": [
            "Select by distance from point",
            "Spherical region filter",
            "Radial effects"
        ],
        "pitfalls": [
            "Position: sphere center",
            "Radius: selection distance",
            "Simpler than Proximity + Compare for round regions"
        ],
        "commonly_used_with": [
            ("Object Info", "animated/object-controlled center"),
            ("Delete Geometry", "carve spherical holes"),
            ("Separate Geometry", "extract sphere contents"),
            ("Boolean Math", "combine selections")
        ],
        "example": "Select near origin: Position (0,0,0), Radius 5. Interactive: Object Info Location as Position = selection follows empty. Explosion: animated expanding Radius."
    },
    
    # ==========================================================================
    # SET ID NODE
    # ==========================================================================
    
    "GeometryNodeSetID": {
        "display_name": "Set ID",
        "category": "Geometry",
        "description": "Assigns stable ID attribute to elements - persists through some topology changes.",
        "common_uses": [
            "Stable identification for randomness",
            "Track elements through operations",
            "Custom element tagging"
        ],
        "pitfalls": [
            "ID ≠ Index (ID can be any value)",
            "Not all operations preserve ID",
            "Use ID node to read values back"
        ],
        "commonly_used_with": [
            ("ID", "read ID values"),
            ("Index", "common ID source"),
            ("Random Value", "ID as stable seed"),
            ("Simulation Zone", "track particles")
        ],
        "example": "Stable random: Set ID (Index) before topology changes → Random Value with ID seed = consistent randomness. Particle tracking: Set ID at spawn, ID persists through simulation."
    },
    
    # ==========================================================================
    # CURVE TOPOLOGY NODES
    # ==========================================================================
    
    "GeometryNodeCurveOfPoint": {
        "display_name": "Curve of Point",
        "category": "Curve Topology",
        "description": "Gets which spline a control point belongs to - point to curve index lookup.",
        "common_uses": [
            "Find which curve owns a point",
            "Per-curve operations from point context",
            "Curve index for grouping"
        ],
        "pitfalls": [
            "Curve Index: which spline (0, 1, 2...)",
            "Index in Curve: position within spline (0 = first point)",
            "Multi-spline curves have separate indices"
        ],
        "commonly_used_with": [
            ("Random Value", "Curve Index as seed = per-curve random"),
            ("Evaluate at Index", "access spline properties"),
            ("Points of Curve", "reverse operation"),
            ("Accumulate Field", "Curve Index as Group")
        ],
        "example": "Per-curve color: Curve Index as Random seed. Point position: Index in Curve ÷ point count = 0-1 along spline. Find if first point: Index in Curve = 0."
    },
    
    "GeometryNodeOffsetPointInCurve": {
        "display_name": "Offset Point in Curve",
        "category": "Curve Topology",
        "description": "Gets index of neighboring point on same curve - step forward/backward along spline.",
        "common_uses": [
            "Find next/previous point",
            "Calculate point-to-point direction",
            "Curve neighbor queries"
        ],
        "pitfalls": [
            "Offset +1 = next point, -1 = previous",
            "Is Valid: False at curve ends (unless cyclic)",
            "Point Index output for use with Evaluate at Index"
        ],
        "commonly_used_with": [
            ("Evaluate at Index", "get neighbor's Position"),
            ("Vector Math (Subtract)", "direction to neighbor"),
            ("Is Spline Cyclic", "check wrapping behavior"),
            ("Compare", "detect endpoints via Is Valid")
        ],
        "example": "Smooth direction: Offset(-1) position, Offset(+1) position → average direction. Check Is Valid before using - False at non-cyclic curve ends."
    },
    
    "GeometryNodePointsOfCurve": {
        "display_name": "Points of Curve",
        "category": "Curve Topology",
        "description": "Gets control point indices of a spline - access points by sorted position.",
        "common_uses": [
            "Find first/last point of curve",
            "Access specific point by position",
            "Get point count per spline"
        ],
        "pitfalls": [
            "Sort Index: which point (0 = first by Weight)",
            "Weight: sorts points (e.g., by Position.Z)",
            "Total: number of points in spline"
        ],
        "commonly_used_with": [
            ("Evaluate at Index", "get point data"),
            ("Endpoint Selection", "simpler for first/last"),
            ("Spline Parameter", "alternative for position"),
            ("Curve of Point", "reverse operation")
        ],
        "example": "First point: Sort Index 0. Last point: Sort Index (Total-1). Lowest point: Position.Z as Weight, Sort Index 0 = lowest. Point count: Total output."
    },
    
    # ==========================================================================
    # UTILITY MATH NODES (additional)
    # ==========================================================================
    
    "FunctionNodeFloatToInt": {
        "display_name": "Float to Integer",
        "category": "Utilities",
        "description": "Converts decimal to whole number - multiple rounding modes.",
        "common_uses": [
            "Integer indices from calculations",
            "Stepped/discrete values",
            "Round random values"
        ],
        "pitfalls": [
            "Round: nearest integer",
            "Floor: always down (3.9 → 3)",
            "Ceiling: always up (3.1 → 4)",
            "Truncate: toward zero"
        ],
        "commonly_used_with": [
            ("Index Switch", "integer index required"),
            ("Sample Index", "integer indices"),
            ("Random Value", "discrete random"),
            ("Math (Divide)", "before converting")
        ],
        "example": "Stepped gradient: value × 5 → Floor = 5 discrete steps. Random index: Random (0-3.99) → Floor = 0,1,2,3. Grid snapping: Position / grid_size → Floor × grid_size."
    },
    
    "ShaderNodeFloatCurve": {
        "display_name": "Float Curve",
        "category": "Utilities",
        "description": "Remaps values through a drawable curve - custom easing and falloff shapes.",
        "common_uses": [
            "Ease-in/ease-out timing",
            "Custom falloff curves",
            "Non-linear value transformation"
        ],
        "pitfalls": [
            "X axis = input value, Y axis = output",
            "Factor: 0 = original, 1 = curved result",
            "Input typically 0-1 (use Map Range first)"
        ],
        "commonly_used_with": [
            ("Map Range", "normalize input to 0-1"),
            ("Spline Parameter", "shaped curve radius"),
            ("Noise Texture", "reshape noise contrast"),
            ("Scene Time", "animation easing")
        ],
        "example": "Ease-in-out: S-curve shape. Sharp threshold: steep curve at midpoint. Custom taper: draw exact radius profile. More control than Map Range's linear interpolation."
    },
    
    # ==========================================================================
    # BLUR ATTRIBUTE NODE
    # ==========================================================================
    
    "GeometryNodeBlurAttribute": {
        "display_name": "Blur Attribute",
        "category": "Attribute",
        "description": "Smooths values by averaging with neighbors - softens sharp transitions.",
        "common_uses": [
            "Smooth vertex colors",
            "Soften random values",
            "Gradual selection edges"
        ],
        "pitfalls": [
            "Iterations: blur passes (more = smoother)",
            "Weight: per-element blur strength",
            "Works along mesh connectivity"
        ],
        "commonly_used_with": [
            ("Random Value", "smooth random variation"),
            ("Store Named Attribute", "save blurred result"),
            ("Compare", "before blur for soft selection edges"),
            ("Color", "smooth vertex colors")
        ],
        "example": "Smooth random colors: Random Color → Blur (iterations 5). Soft selection edge: Boolean selection → Blur Weight for falloff. Each iteration averages with neighbors."
    },
    
    # ==========================================================================
    # GEOMETRY READ NODES (additional)
    # ==========================================================================
    
    "GeometryNodeInputRadius": {
        "display_name": "Radius",
        "category": "Input",
        "description": "Reads radius attribute of points/curve control points - for thickness calculations.",
        "common_uses": [
            "Read current radius",
            "Relative radius modifications",
            "Thickness-based effects"
        ],
        "pitfalls": [
            "Only on Point Cloud and Curve points",
            "Default is often 1.0",
            "Use Set Curve Radius / Set Point Radius to modify"
        ],
        "commonly_used_with": [
            ("Set Curve Radius", "modify curve thickness"),
            ("Set Point Radius", "modify point size"),
            ("Math (Multiply)", "relative scaling"),
            ("Curve to Mesh", "radius affects tube size")
        ],
        "example": "Double thickness: Radius × 2 → Set Curve Radius. Relative modification: read current, apply change, write back. Curve to Mesh uses radius for tube diameter."
    },
    
    "GeometryNodeInputCurveHandlePositions": {
        "display_name": "Curve Handle Positions",
        "category": "Curve Read",
        "description": "Reads Bezier handle positions - Left and Right handles as vectors.",
        "common_uses": [
            "Read existing handle positions",
            "Calculate handle lengths",
            "Analyze curve smoothness"
        ],
        "pitfalls": [
            "Only works on Bezier curves",
            "Relative: offset from control point",
            "Left/Right: separate vector outputs"
        ],
        "commonly_used_with": [
            ("Set Handle Positions", "read then modify"),
            ("Vector Math (Length)", "handle length"),
            ("Position", "compare to point location"),
            ("Set Handle Type", "change behavior")
        ],
        "example": "Handle length: Vector Math Length on Left/Right output. Symmetric check: compare Left and Right lengths. Read → modify → Set Handle Positions workflow."
    },
    
    "GeometryNodeSetHandlePositions": {
        "display_name": "Set Handle Positions",
        "category": "Curve Write",
        "description": "Sets Bezier handle positions - controls curve shape by moving handles.",
        "common_uses": [
            "Adjust curve smoothness",
            "Custom handle placement",
            "Procedural curve shaping"
        ],
        "pitfalls": [
            "Only affects Bezier curves",
            "Mode: Left, Right, or both handles",
            "Offset: adds to current vs replaces"
        ],
        "commonly_used_with": [
            ("Curve Handle Positions", "read first"),
            ("Vector Math (Scale)", "adjust handle length"),
            ("Noise Texture", "organic variation"),
            ("Random Value", "randomize handles")
        ],
        "example": "Longer handles = smoother curves. Shorten: Scale current handles × 0.5. Add variation: Noise Texture × small value as Offset. Mode Offset preserves relative positions."
    },
    
    "GeometryNodeSetHandleType": {
        "display_name": "Set Handle Type",
        "category": "Curve Write",
        "description": "Sets Bezier handle behavior mode - Free, Auto, Vector, or Align.",
        "common_uses": [
            "Create sharp corners (Vector)",
            "Auto-smooth curves (Auto)",
            "Independent handle control (Free)"
        ],
        "pitfalls": [
            "Auto: automatically calculates smooth handles",
            "Vector: points straight to adjacent point (sharp)",
            "Free: handles move independently",
            "Align: handles stay collinear through point"
        ],
        "commonly_used_with": [
            ("Handle Type Selection", "find current types"),
            ("Set Handle Positions", "adjust after type change"),
            ("Endpoint Selection", "modify end handles"),
            ("Set Spline Type (Bezier)", "convert to Bezier first")
        ],
        "example": "Sharp corner: Set Handle Type (Vector). Smooth curve: Set Handle Type (Auto). Custom control: Set Handle Type (Free) then Set Handle Positions manually."
    },
    
    # ==========================================================================
    # IMAGE TEXTURE NODE
    # ==========================================================================
    
    "GeometryNodeImageTexture": {
        "display_name": "Image Texture",
        "category": "Texture",
        "description": "Samples colors from image file - reads pixels at UV coordinates.",
        "common_uses": [
            "Apply image textures procedurally",
            "Height maps for displacement",
            "Mask/stencil from images"
        ],
        "pitfalls": [
            "Image: select image datablock (not file path)",
            "Vector: UV coordinates (0-1 range typically)",
            "Extension: Repeat, Clip, Extend (for edges)"
        ],
        "commonly_used_with": [
            ("Named Attribute (UVMap)", "get UV coordinates"),
            ("Position", "projected/world-space texturing"),
            ("Set Position", "image-driven displacement"),
            ("Store Named Attribute", "save sampled colors")
        ],
        "example": "Displacement from heightmap: Image Texture (grayscale) → multiply by strength → Set Position along Normal. UV texturing: Named Attribute 'UVMap' as Vector input."
    },
    
    # ==========================================================================
    # BAKE NODE
    # ==========================================================================
    
    "GeometryNodeBake": {
        "display_name": "Bake",
        "category": "Utilities",
        "description": "Caches geometry/values to disk - pre-compute for smooth playback.",
        "common_uses": [
            "Cache simulation results",
            "Store expensive calculations",
            "Smooth animation playback"
        ],
        "pitfalls": [
            "Must click Bake button in modifier panel",
            "Uses disk space (check cache folder)",
            "Re-bake after changes"
        ],
        "commonly_used_with": [
            ("Simulation Zone", "bake physics/particles"),
            ("Complex calculations", "pre-compute once"),
            ("Animation", "real-time playback after bake"),
            ("Any heavy node tree", "performance optimization")
        ],
        "example": "Simulation workflow: Build sim → test small frame range → Bake full animation → playback at full speed. Delete bake to re-calculate changes."
    },
    
    # ==========================================================================
    # RANDOM ROTATION NODE
    # ==========================================================================
    
    "FunctionNodeRandomRotation": {
        "display_name": "Random Rotation",
        "category": "Utilities",
        "description": "Generates random rotations - uniform or constrained to axis ranges.",
        "common_uses": [
            "Randomize instance orientation",
            "Natural scatter rotation",
            "Controlled random spinning"
        ],
        "pitfalls": [
            "Min/Max: rotation range per axis (radians)",
            "Seed: different sequence, ID: per-element variation",
            "Full random = Min (-π,-π,-π), Max (π,π,π)"
        ],
        "commonly_used_with": [
            ("Rotate Instances", "apply the rotation"),
            ("Instance on Points", "Rotation input"),
            ("ID", "stable per-element randomness"),
            ("Rotate Rotation", "combine with base alignment")
        ],
        "example": "Z-only spin: Min (0,0,-π), Max (0,0,π) - random heading, upright. Full random: all axes ±π. Use ID as seed for consistent randomness through operations."
    },
    
    # ==========================================================================
    # INSTANCE BOUNDS NODE
    # ==========================================================================
    
    "GeometryNodeInstanceBounds": {
        "display_name": "Instance Bounds",
        "category": "Instances",
        "description": "Gets bounding box of each instance - min/max corners for size calculation.",
        "common_uses": [
            "Calculate instance size",
            "Stacking instances",
            "Bounds-based positioning"
        ],
        "pitfalls": [
            "Returns local bounds (not world-transformed)",
            "Min/Max are opposite corners",
            "Size = Max - Min"
        ],
        "commonly_used_with": [
            ("Vector Math (Subtract)", "calculate size"),
            ("Accumulate Field", "stack by height"),
            ("Translate Instances", "bounds-based offset"),
            ("Instance Scale", "combine with scale")
        ],
        "example": "Instance height: (Max - Min).Z. Stack instances: Accumulate height → Translate by accumulated. Size-aware spacing using bounds."
    },
    
    # ==========================================================================
    # DISPLACE / SMOOTH GEOMETRY NODES
    # ==========================================================================
    
    "GeometryNodeDisplaceGeometry": {
        "display_name": "Displace Geometry",
        "category": "Geometry",
        "description": "Moves geometry along normals by distance - simpler than Set Position for displacement.",
        "common_uses": [
            "Procedural surface detail",
            "Height map displacement",
            "Inflate/deflate geometry"
        ],
        "pitfalls": [
            "Direction defaults to Normal",
            "Needs dense geometry (Subdivide first)",
            "Distance can be negative (inward)"
        ],
        "commonly_used_with": [
            ("Noise Texture", "procedural displacement"),
            ("Subdivide Mesh", "add geometry first"),
            ("Image Texture", "height map"),
            ("Map Range", "scale displacement")
        ],
        "example": "Terrain: Subdivide → Noise Texture as Distance → Displace. Height map: Image Texture (grayscale) as Distance. Simpler than Normal × Distance → Set Position."
    },
    
    "GeometryNodeSmoothGeometry": {
        "display_name": "Smooth Geometry",
        "category": "Geometry",
        "description": "Relaxes vertex positions by averaging with neighbors - softens sharp features.",
        "common_uses": [
            "Smooth rough meshes",
            "Soften Boolean results",
            "Relax procedural geometry"
        ],
        "pitfalls": [
            "Iterations: smoothing passes",
            "Factor: blend with original (1 = full smooth)",
            "Different from Subdivision Surface (no new geometry)"
        ],
        "commonly_used_with": [
            ("Mesh Boolean", "clean up results"),
            ("Noise displacement", "soften after"),
            ("Extrude Mesh", "smooth extruded parts"),
            ("Subdivide Mesh", "after for smooth shape")
        ],
        "example": "Smooth noise: Subdivide → Displace → Smooth (iterations 3). Boolean cleanup: Boolean → Smooth. Factor 0.5 for partial smoothing."
    },
    
    # ==========================================================================
    # NODE GROUPS (custom/asset nodes)
    # ==========================================================================
    
    "GeometryNodeGroup": {
        "display_name": "Node Group",
        "category": "Group",
        "description": "A custom node group - either user-created or from an asset library. Contains other nodes packaged together as a reusable unit.",
        "common_uses": [
            "Reusing node setups",
            "Organizing complex trees",
            "Sharing node tools",
            "Asset library nodes"
        ],
        "pitfalls": [
            "Tab into group to see contents",
            "Inputs/outputs defined inside",
            "May come from asset libraries"
        ],
        "commonly_used_with": [
            ("Any nodes", "groups can contain anything"),
            ("Group Input", "defines group inputs"),
            ("Group Output", "defines group outputs"),
            ("Asset Browser", "to find pre-made groups")
        ],
        "example": "This is a custom node group - a package of nodes bundled together. It could be something you made, downloaded, or from Blender's asset library. Press Tab to look inside and see what nodes it contains. The inputs and outputs are defined by Group Input/Output nodes inside."
    },
    
    "ShaderNodeGroup": {
        "display_name": "Shader Node Group",
        "category": "Group",
        "description": "Custom shader node group - packaged shader nodes for material reuse.",
        "common_uses": [
            "Reusable shader setups",
            "Complex material components",
            "Shared shader assets"
        ],
        "pitfalls": [
            "Tab to enter group and see contents",
            "Shader context (not geometry nodes)",
            "Inputs/outputs defined inside"
        ],
        "commonly_used_with": [
            ("Shader nodes", "contents"),
            ("Group Input/Output", "define interface"),
            ("Material Output", "final destination"),
            ("Asset Browser", "shared groups")
        ],
        "example": "Custom PBR shader: inputs for color/roughness → internal shader math → output to Material. Tab to edit, Ctrl+Tab to exit. Different from Geometry Node Groups."
    },
    
    # ==========================================================================
    # SCENE INPUT NODES
    # ==========================================================================
    
    "GeometryNodeActiveCamera": {
        "display_name": "Active Camera",
        "category": "Input",
        "description": "Returns scene's active camera object - for camera-dependent effects.",
        "common_uses": [
            "Camera-facing billboards",
            "View-dependent LOD",
            "Camera position reference"
        ],
        "pitfalls": [
            "Returns camera Object (not properties)",
            "Use Camera Info for focal length etc.",
            "May be None if no active camera"
        ],
        "commonly_used_with": [
            ("Camera Info", "get camera properties"),
            ("Object Info", "get camera transform"),
            ("Is Viewport", "viewport vs render camera"),
            ("Vector Math", "direction to camera")
        ],
        "example": "Billboard: Active Camera → Object Info → calculate direction → Align Euler to Vector. Camera distance: Position - Camera Location → Length."
    },
    
    "GeometryNodeCameraInfo": {
        "display_name": "Camera Info",
        "category": "Input",
        "description": "Outputs detailed camera properties like focal length, sensor size, and projection matrix.",
        "common_uses": [
            "Getting camera focal length",
            "Projection calculations",
            "Camera-based effects",
            "View alignment"
        ],
        "pitfalls": [
            "Needs camera object input",
            "Use Active Camera node for input",
            "Projection matrix is 4x4"
        ],
        "commonly_used_with": [
            ("Active Camera", "to get camera"),
            ("Object Info", "for camera position"),
            ("Transform Point", "for projection"),
            ("Matrix nodes", "for projection math")
        ],
        "example": "Gets all the camera settings - focal length, sensor size, clipping distances. Use the projection matrix to convert 3D points to screen space, or the focal length to scale things based on zoom level."
    },
    
    "GeometryNodeSelfObject": {
        "display_name": "Self Object",
        "category": "Input",
        "description": "Returns the object owning this modifier - for self-referencing transform data.",
        "common_uses": [
            "Get own object's transform",
            "Self-relative positioning",
            "Access own object properties"
        ],
        "pitfalls": [
            "Cannot get own geometry (causes recursion)",
            "In Tool mode: returns active object",
            "Use with Object Info for transform data"
        ],
        "commonly_used_with": [
            ("Object Info", "extract Location/Rotation/Scale"),
            ("Transform Geometry", "world-space alignment"),
            ("Vector Math", "relative calculations"),
            ("Is Viewport", "context-aware behavior")
        ],
        "example": "Self-centering: Self Object → Object Info → use Location for reference. World alignment: Self Object transform for local-to-world conversion. Avoids hardcoded object references."
    },
    
    "GeometryNodeIsViewport": {
        "display_name": "Is Viewport",
        "category": "Input",
        "description": "Returns True in viewport, False during render - for LOD and optimization switching.",
        "common_uses": [
            "Viewport optimization",
            "Render vs preview quality",
            "Performance management"
        ],
        "pitfalls": [
            "True: viewport/preview",
            "False: final render (F12)",
            "Use with Switch for different setups"
        ],
        "commonly_used_with": [
            ("Switch", "toggle between setups"),
            ("Subdivide Mesh", "less detail in viewport"),
            ("Resample Curve", "fewer points in viewport"),
            ("Realize Instances", "only for render")
        ],
        "example": "LOD system: Is Viewport → Switch (True: low-poly, False: high-poly). Auto-optimize: lower subdivision in viewport, full detail only when rendering."
    },
    
    "GeometryNodeInputMousePosition": {
        "display_name": "Mouse Position",
        "category": "Input",
        "description": "Returns mouse cursor position - for interactive Tool node trees only.",
        "common_uses": [
            "Interactive sculpting tools",
            "Click-based placement",
            "Mouse-following effects"
        ],
        "pitfalls": [
            "Only works in Tool context (not modifiers)",
            "Multiple outputs: Screen, Region, 3D",
            "Updates every mouse move"
        ],
        "commonly_used_with": [
            ("Raycast", "find surface under mouse"),
            ("Set Position", "move geometry to mouse"),
            ("Compare", "distance-based effects"),
            ("Geometry Proximity", "nearest to click")
        ],
        "example": "Interactive brush: Mouse Position → Raycast to surface → affect nearby geometry. Only for custom Tool node trees, not regular Geometry Nodes modifiers."
    },
    
    "GeometryNodeTool3DCursor": {
        "display_name": "3D Cursor",
        "category": "Input",
        "description": "Outputs the 3D cursor's position and rotation in the scene.",
        "common_uses": [
            "Cursor-relative placement",
            "Tool positioning",
            "Reference point",
            "User-defined location"
        ],
        "pitfalls": [
            "Scene-level property",
            "Position and rotation outputs",
            "Shift+RMB to place cursor"
        ],
        "commonly_used_with": [
            ("Set Position", "move to cursor"),
            ("Transform Geometry", "align to cursor"),
            ("Instance on Points", "place at cursor"),
            ("Vector Math", "offset from cursor")
        ],
        "example": "Gets where the 3D cursor is - that little crosshair you can place with Shift+Right-click. Use it as a reference point: spawn objects at the cursor, measure distances from it, or use it as a pivot point for transformations."
    },
    
    "GeometryNodeImageInfo": {
        "display_name": "Image Info",
        "category": "Input",
        "description": "Outputs information about an image - width, height, frame count, and whether it has alpha.",
        "common_uses": [
            "Getting image dimensions",
            "Aspect ratio calculations",
            "Animation frame info",
            "Alpha detection"
        ],
        "pitfalls": [
            "Needs image data-block",
            "Dimensions in pixels",
            "Frames for image sequences"
        ],
        "commonly_used_with": [
            ("Image Texture", "use same image"),
            ("Math", "calculate aspect ratio"),
            ("Grid", "match image dimensions"),
            ("Scene Time", "for animated textures")
        ],
        "example": "Gets info about an image - its width, height, whether it has transparency, and how many frames (for sequences). Use to create a plane with the exact proportions of your image, or to check if an image has alpha for masking."
    },
    
    "GeometryNodeViewportTransform": {
        "display_name": "Viewport Transform",
        "category": "Input",
        "description": "Returns current viewport's view/projection matrices - for view-dependent effects.",
        "common_uses": [
            "Billboard orientation",
            "View-facing geometry",
            "Screen-space effects"
        ],
        "pitfalls": [
            "Changes as viewport orbits",
            "Different per 3D viewport",
            "Real-time only (not render)"
        ],
        "commonly_used_with": [
            ("Align Euler to Vector", "face viewport"),
            ("Rotate Instances", "billboard effect"),
            ("Is Viewport", "viewport-only logic"),
            ("Project Point", "screen projection")
        ],
        "example": "Billboards: extract view direction → Align Euler to Vector → Rotate Instances to face viewer. Updates live as you orbit viewport."
    },
    
    # ==========================================================================
    # IMPORT NODES
    # ==========================================================================
    
    "GeometryNodeImportOBJ": {
        "display_name": "Import OBJ",
        "category": "Import",
        "description": "Loads geometry from .obj file - supports meshes, UVs, materials.",
        "common_uses": [
            "Load external models",
            "Procedural asset loading",
            "Dynamic geometry import"
        ],
        "pitfalls": [
            "Path must be valid file path",
            "Reloads on every evaluation (can be slow)",
            "UVs and materials preserved"
        ],
        "commonly_used_with": [
            ("Join Geometry", "combine imported parts"),
            ("Transform Geometry", "position imported model"),
            ("Realize Instances", "work with imported data"),
            ("Set Material", "override materials")
        ],
        "example": "Dynamic loading: file path string → Import OBJ → process geometry. Asset variation: different paths for variety. Consider caching for performance."
    },
    
    "GeometryNodeImportSTL": {
        "display_name": "Import STL",
        "category": "Import",
        "description": "Imports geometry from an STL file. Common format for 3D printing - triangles only, no colors.",
        "common_uses": [
            "Loading 3D print files",
            "CAD model import",
            "Simple mesh loading",
            "Procedural STL processing"
        ],
        "pitfalls": [
            "Triangulated mesh only",
            "No color or UV data",
            "ASCII or binary format"
        ],
        "commonly_used_with": [
            ("Transform Geometry", "scale imported"),
            ("Set Material", "add material"),
            ("Merge by Distance", "clean up"),
            ("Set Shade Smooth", "smooth shading")
        ],
        "example": "Loads 3D models from STL files - the format used for 3D printing. STL files are just triangles with no color info, so you'll need to add materials after importing. Good for loading CAD exports."
    },
    
    "GeometryNodeImportPLY": {
        "display_name": "Import PLY",
        "category": "Import",
        "description": "Loads geometry from .ply file - supports vertex colors and point clouds.",
        "common_uses": [
            "3D scan import",
            "Point cloud data",
            "Colored mesh loading"
        ],
        "pitfalls": [
            "May include vertex colors as attribute",
            "Can be mesh or point cloud",
            "ASCII or binary format supported"
        ],
        "commonly_used_with": [
            ("Store Named Attribute", "preserve vertex colors"),
            ("Points to Vertices", "convert point cloud to mesh"),
            ("Transform Geometry", "scale/position"),
            ("Set Shade Smooth", "smooth imported mesh")
        ],
        "example": "Photogrammetry: Import PLY → vertex colors preserved → Set Material using vertex color. Point cloud: may need conversion for further processing."
    },
    
    "GeometryNodeImportCSV": {
        "display_name": "Import CSV",
        "category": "Import",
        "description": "Loads point data from .csv file - rows become points, columns become attributes.",
        "common_uses": [
            "Data visualization",
            "Spreadsheet to 3D",
            "Scientific data plotting"
        ],
        "pitfalls": [
            "Each row = one point",
            "Column headers = attribute names",
            "Delimiter (comma/tab) configurable"
        ],
        "commonly_used_with": [
            ("Named Attribute", "read imported columns"),
            ("Set Position", "XYZ from columns"),
            ("Instance on Points", "visualize data points"),
            ("Points to Curves", "connect data points")
        ],
        "example": "Data visualization: Import CSV with X,Y,Z columns → Set Position from attributes → Instance spheres. Scientific plot: column values as position/scale/color."
    },
    
    "GeometryNodeImportText": {
        "display_name": "Import Text",
        "category": "Import",
        "description": "Imports text content from a .txt file as a string value.",
        "common_uses": [
            "Loading external text",
            "Dynamic text content",
            "Configuration files",
            "String data import"
        ],
        "pitfalls": [
            "Returns string output",
            "Entire file as one string",
            "Use String nodes to process"
        ],
        "commonly_used_with": [
            ("String to Curves", "display the text"),
            ("Slice String", "extract parts"),
            ("Replace String", "modify content"),
            ("Join Strings", "combine with other text")
        ],
        "example": "Reads a text file and outputs its contents as a string. Feed it to String to Curves to display the text as 3D geometry, or process it with string nodes. Good for dynamic text that you can edit without touching the node tree."
    },
    
    # ==========================================================================
    # GREASE PENCIL NODES
    # ==========================================================================
    
    "GeometryNodeInputNamedLayerSelection": {
        "display_name": "Named Layer Selection",
        "category": "Grease Pencil",
        "description": "Selects grease pencil strokes that belong to a specific named layer.",
        "common_uses": [
            "Selecting GP layers",
            "Layer-based effects",
            "Organizing GP strokes",
            "Per-layer processing"
        ],
        "pitfalls": [
            "Grease pencil specific",
            "Layer name must match exactly",
            "Case sensitive"
        ],
        "commonly_used_with": [
            ("Delete Geometry", "remove layers"),
            ("Set Material", "per-layer materials"),
            ("Transform Geometry", "move layers"),
            ("Separate Geometry", "split by layer")
        ],
        "example": "Selects all grease pencil strokes on a specific layer by name. Like selecting all strokes on the 'Sketch' layer to give them a different color or move them separately from other layers."
    },
    
    "GeometryNodeSetGreasePencilColor": {
        "display_name": "Set Grease Pencil Color",
        "category": "Grease Pencil",
        "description": "Sets the stroke and fill colors of grease pencil strokes.",
        "common_uses": [
            "Coloring GP strokes",
            "Procedural coloring",
            "Gradient effects",
            "Animation coloring"
        ],
        "pitfalls": [
            "Separate stroke/fill colors",
            "Opacity also settable",
            "Per-point or per-stroke"
        ],
        "commonly_used_with": [
            ("Named Layer Selection", "select what to color"),
            ("Random Value", "random colors"),
            ("Gradient Texture", "color gradients"),
            ("Spline Parameter", "along-stroke color")
        ],
        "example": "Colors grease pencil strokes - both the stroke outline and the fill. You can set different colors for stroke vs fill, and control opacity. Great for procedurally coloring hand-drawn elements."
    },
    
    "GeometryNodeSetGreasePencilDepth": {
        "display_name": "Set Grease Pencil Depth",
        "category": "Grease Pencil",
        "description": "Sets the depth ordering of grease pencil strokes for 2D layering.",
        "common_uses": [
            "Stroke ordering",
            "2D layer depth",
            "Draw order control",
            "Overlap management"
        ],
        "pitfalls": [
            "Affects draw order",
            "2D depth, not 3D position",
            "Higher = in front"
        ],
        "commonly_used_with": [
            ("Named Layer Selection", "select layers"),
            ("Index", "automatic ordering"),
            ("Random Value", "varied depths"),
            ("Compare", "conditional depth")
        ],
        "example": "Controls the stacking order of grease pencil strokes - which strokes appear in front of others. Higher depth values draw on top. Useful for 2D animation where you need to control which elements overlap."
    },
    
    "GeometryNodeSetGreasePencilSoftness": {
        "display_name": "Set Grease Pencil Softness",
        "category": "Grease Pencil",
        "description": "Sets the softness/blur of grease pencil stroke edges.",
        "common_uses": [
            "Soft brush effects",
            "Edge blur",
            "Airbrush look",
            "Stylized strokes"
        ],
        "pitfalls": [
            "Affects stroke edges",
            "0 = sharp, higher = softer",
            "Visual effect only"
        ],
        "commonly_used_with": [
            ("Named Layer Selection", "select strokes"),
            ("Spline Parameter", "along-stroke softness"),
            ("Random Value", "varied softness"),
            ("Map Range", "control softness range")
        ],
        "example": "Makes grease pencil stroke edges soft and blurry - like an airbrush effect. Higher values create more blur. Use to mix sharp and soft strokes in the same drawing for depth or focus effects."
    },
    
    "GeometryNodeGreasePencilToCurves": {
        "display_name": "Grease Pencil to Curves",
        "category": "Grease Pencil",
        "description": "Converts grease pencil strokes to curve geometry for further processing.",
        "common_uses": [
            "Converting GP to curves",
            "Processing GP as curves",
            "GP to mesh workflow",
            "Curve operations on GP"
        ],
        "pitfalls": [
            "One curve per stroke",
            "Loses some GP attributes",
            "Use Curve to Mesh after"
        ],
        "commonly_used_with": [
            ("Curve to Mesh", "create 3D strokes"),
            ("Resample Curve", "control point count"),
            ("Set Curve Radius", "stroke thickness"),
            ("Trim Curve", "shorten strokes")
        ],
        "example": "Turns grease pencil strokes into regular curves. Each stroke becomes a curve, preserving the path but converting to curve data. Then you can use all the curve nodes - like Curve to Mesh to make 3D tubes from your drawings."
    },
    
    "GeometryNodeMergeGreasePencilLayers": {
        "display_name": "Merge Layers",
        "category": "Grease Pencil",
        "description": "Merges multiple grease pencil layers into one layer.",
        "common_uses": [
            "Combining GP layers",
            "Simplifying layer structure",
            "Flattening GP",
            "Layer consolidation"
        ],
        "pitfalls": [
            "Combines into single layer",
            "Layer attributes may be lost",
            "Selection controls which merge"
        ],
        "commonly_used_with": [
            ("Named Layer Selection", "select layers to merge"),
            ("Join Geometry", "alternative for curves"),
            ("Set Grease Pencil Color", "unify colors after"),
            ("Realize Instances", "flatten first")
        ],
        "example": "Combines multiple grease pencil layers into one. Like flattening layers in a drawing app. Select which layers to merge using a selection input, then they all become part of a single layer."
    },
    
    # ==========================================================================
    # OUTPUT NODES
    # ==========================================================================
    
    "GeometryNodeWarning": {
        "display_name": "Warning",
        "category": "Output",
        "description": "Displays a warning message in the modifier panel when a condition is true.",
        "common_uses": [
            "User warnings",
            "Invalid input alerts",
            "Debug messages",
            "Condition feedback"
        ],
        "pitfalls": [
            "Shows in modifier panel",
            "Only when condition true",
            "Message is a string"
        ],
        "commonly_used_with": [
            ("Compare", "create warning condition"),
            ("Boolean Math", "combine conditions"),
            ("String", "warning message"),
            ("Attribute Statistic", "check for issues")
        ],
        "example": "Shows a warning message to the user when something's wrong. Like alerting 'Scale is zero!' when a value that shouldn't be zero is zero. The warning appears in the modifier panel so users know to fix something."
    },
    
    "GeometryNodeEnableOutput": {
        "display_name": "Enable Output",
        "category": "Output",
        "description": "Conditionally enables or disables a group output based on a boolean condition.",
        "common_uses": [
            "Conditional outputs",
            "Optional results",
            "Debug outputs",
            "Feature toggles"
        ],
        "pitfalls": [
            "Controls output visibility",
            "Use in node groups",
            "Boolean enables/disables"
        ],
        "commonly_used_with": [
            ("Group Output", "controls this output"),
            ("Compare", "create enable condition"),
            ("Boolean", "manual toggle"),
            ("Switch", "alternative approach")
        ],
        "example": "Turns a node group output on or off based on a condition. When disabled, that output won't show up in the modifier panel. Useful for optional features or debug outputs that you can toggle."
    },
    
    # ==========================================================================
    # GIZMO NODES
    # ==========================================================================
    
    "GeometryNodeGizmoDial": {
        "display_name": "Dial Gizmo",
        "category": "Gizmo",
        "description": "Creates a rotational dial gizmo for interactive angle input in the viewport.",
        "common_uses": [
            "Interactive rotation control",
            "Angle input",
            "Rotational parameters",
            "Visual angle feedback"
        ],
        "pitfalls": [
            "Tool context mainly",
            "Returns rotation value",
            "Visual feedback in viewport"
        ],
        "commonly_used_with": [
            ("Rotate Instances", "apply dial rotation"),
            ("Transform Geometry", "rotation input"),
            ("Math", "convert angle units"),
            ("Euler to Rotation", "create rotation")
        ],
        "example": "Adds a dial you can rotate in the viewport - like a volume knob. Drag it around to set an angle value. Great for tools where you want users to interactively set rotation by clicking and dragging."
    },
    
    "GeometryNodeGizmoLinear": {
        "display_name": "Linear Gizmo",
        "category": "Gizmo",
        "description": "Creates a linear slider gizmo for interactive value input along an axis.",
        "common_uses": [
            "Interactive distance control",
            "Linear value input",
            "Position adjustment",
            "Size/scale control"
        ],
        "pitfalls": [
            "Drag along axis",
            "Returns float value",
            "Customize axis direction"
        ],
        "commonly_used_with": [
            ("Set Position", "offset by value"),
            ("Scale Elements", "size control"),
            ("Extrude Mesh", "extrude distance"),
            ("Map Range", "scale the value")
        ],
        "example": "Adds a slider you can drag in the viewport - click and drag along a line to set a value. Perfect for distance or size controls where you want users to visually drag to set how far or how big."
    },
    
    "GeometryNodeGizmoTransform": {
        "display_name": "Transform Gizmo",
        "category": "Gizmo",
        "description": "Creates a full transform gizmo with move, rotate, and scale handles.",
        "common_uses": [
            "Interactive transform control",
            "Complete manipulation",
            "Object-like control",
            "Tool transform input"
        ],
        "pitfalls": [
            "Full transform output",
            "Position, rotation, scale",
            "Complex interaction"
        ],
        "commonly_used_with": [
            ("Transform Geometry", "apply transform"),
            ("Instance on Points", "place instances"),
            ("Combine Transform", "build matrix"),
            ("Set Position", "position only")
        ],
        "example": "Adds a full transform gizmo - the familiar move/rotate/scale handles you use on objects. Gives you a complete transformation that users can manipulate interactively, outputting position, rotation, and scale."
    },
    
    # ==========================================================================
    # ADDITIONAL INSTANCE NODES
    # ==========================================================================
    
    "GeometryNodeInstanceOnElements": {
        "display_name": "Instance on Elements",
        "category": "Instances",
        "description": "Places instances on mesh elements (vertices, edges, faces) with automatic orientation.",
        "common_uses": [
            "Instancing on faces",
            "Edge decoration",
            "Per-element instances",
            "Automatic alignment"
        ],
        "pitfalls": [
            "Domain selects element type",
            "Auto-aligns to element",
            "Different from Instance on Points"
        ],
        "commonly_used_with": [
            ("Face Area", "for face-based"),
            ("Edge Vertices", "for edge-based"),
            ("Random Value", "randomize instances"),
            ("Collection Info", "varied instances")
        ],
        "example": "Places instances directly on mesh elements - faces, edges, or vertices - with automatic alignment. Put tiles on every face, decorations on every edge, or markers on every vertex. Handles orientation automatically."
    },
    
    "GeometryNodeRandomizeTransforms": {
        "display_name": "Randomize Transforms",
        "category": "Instances",
        "description": "Adds random position, rotation, and scale variation to instances.",
        "common_uses": [
            "Natural-looking scatter",
            "Transform variation",
            "Organic placement",
            "Breaking uniformity"
        ],
        "pitfalls": [
            "Separate position/rotation/scale controls",
            "Seed for reproducibility",
            "Applied to existing instances"
        ],
        "commonly_used_with": [
            ("Instance on Points", "then randomize"),
            ("Collection Info", "varied objects"),
            ("Random Value", "additional control"),
            ("ID", "stable randomization")
        ],
        "example": "Adds random variation to instance transforms - jitter the position, randomly rotate, randomly scale. Makes scattered objects look natural instead of perfectly uniform. Like making a forest where each tree is slightly different."
    },
    
    # ==========================================================================
    # ARRAY NODE
    # ==========================================================================
    
    "GeometryNodeArray": {
        "display_name": "Array",
        "category": "Geometry",
        "description": "Creates multiple copies of geometry in linear, circular, or custom patterns.",
        "common_uses": [
            "Linear duplication",
            "Circular arrays",
            "Pattern creation",
            "Repeated elements"
        ],
        "pitfalls": [
            "Multiple arrangement modes",
            "Count controls copies",
            "Randomization options"
        ],
        "commonly_used_with": [
            ("Transform Geometry", "custom offsets"),
            ("Realize Instances", "merge copies"),
            ("Boolean", "combine results"),
            ("Random Value", "varied copies")
        ],
        "example": "Makes copies of geometry arranged in patterns - a row of columns, a circle of chairs, or custom arrangements. Control count, spacing, rotation per copy, and even add randomization. Like the array modifier but as a node."
    },
    
    # ==========================================================================
    # REMOVE NAMED ATTRIBUTE
    # ==========================================================================
    
    "GeometryNodeRemoveAttribute": {
        "display_name": "Remove Named Attribute",
        "category": "Attribute",
        "description": "Deletes named attribute from geometry - cleanup for temporary data.",
        "common_uses": [
            "Remove temporary attributes",
            "Clean up after processing",
            "Reduce file size"
        ],
        "pitfalls": [
            "Name must match exactly (case-sensitive)",
            "Deletion is permanent",
            "No error if attribute doesn't exist"
        ],
        "commonly_used_with": [
            ("Store Named Attribute", "create then remove"),
            ("Named Attribute", "verify existence first"),
            ("Capture Attribute", "clean up captures"),
            ("Realize Instances", "clean instance attributes")
        ],
        "example": "Cleanup workflow: Store Named Attribute for processing → use data → Remove Named Attribute. Export prep: remove internal attributes before exporting."
    },
    
    # ==========================================================================
    # ADDITIONAL GEOMETRY NODES
    # ==========================================================================
    
    "GeometryNodeSetGeometryName": {
        "display_name": "Set Geometry Name",
        "category": "Geometry",
        "description": "Assigns name to geometry - metadata for organization and debugging.",
        "common_uses": [
            "Label geometry parts",
            "Debug identification",
            "Export naming"
        ],
        "pitfalls": [
            "Metadata only (doesn't affect processing)",
            "Visible in Spreadsheet editor",
            "Useful for complex setups"
        ],
        "commonly_used_with": [
            ("Join Geometry", "name parts before joining"),
            ("Separate Components", "identify separated parts"),
            ("Viewer", "debug which geometry is which"),
            ("String", "dynamic names")
        ],
        "example": "Debug: Set Geometry Name before Viewer to track geometry flow. Organization: name parts before joining for clarity in Spreadsheet."
    },
    
    "GeometryNodeSetSelection": {
        "display_name": "Set Selection",
        "category": "Geometry",
        "description": "Stores boolean selection as attribute - makes selection persistent on geometry.",
        "common_uses": [
            "Save selection for later use",
            "Pass selection between groups",
            "Persistent selection attribute"
        ],
        "pitfalls": [
            "Stores as hidden '.selection' attribute",
            "Selection node reads it back",
            "Domain must match usage"
        ],
        "commonly_used_with": [
            ("Selection", "read stored selection"),
            ("Compare", "create selection to store"),
            ("Boolean Math", "combine before storing"),
            ("Separate Geometry", "use stored selection")
        ],
        "example": "Store for reuse: Compare → Set Selection → later: Selection node retrieves it. Useful when selection calculated early but used later in tree."
    },
    
    "GeometryNodeActiveElement": {
        "display_name": "Active Element",
        "category": "Geometry",
        "description": "Returns index of active element in edit mode - Tool context only.",
        "common_uses": [
            "Custom edit mode tools",
            "Active element detection",
            "Tool interactions"
        ],
        "pitfalls": [
            "Tool context only (not modifiers)",
            "Returns index (not data)",
            "Active ≠ Selected (active is highlighted one)"
        ],
        "commonly_used_with": [
            ("Sample Index", "get active element's data"),
            ("Compare", "check if element is active"),
            ("Index", "compare against"),
            ("Set Position", "modify active specifically")
        ],
        "example": "Custom tool: Active Element index → Sample Index (get position) → process active element differently. Only for Tool node trees."
    },
    
    "GeometryNodeIndexOfNearest": {
        "display_name": "Index of Nearest",
        "category": "Geometry",
        "description": "Returns index of closest element to each position - fast spatial lookup.",
        "common_uses": [
            "Find nearest neighbor",
            "Spatial matching",
            "Proximity queries"
        ],
        "pitfalls": [
            "Returns index (not position/data)",
            "Use Evaluate at Index to get data",
            "Group ID for separate searches"
        ],
        "commonly_used_with": [
            ("Evaluate at Index", "get nearest element's data"),
            ("Position", "as query position"),
            ("Sample Nearest", "simpler for just position"),
            ("Set Position", "snap to nearest")
        ],
        "example": "Nearest neighbor data: Index of Nearest → Evaluate at Index (Position) = nearest point's position. Snap: Set Position to evaluated nearest position."
    },
    
    # ==========================================================================
    # CORNERS OF EDGE NODE
    # ==========================================================================
    
    "GeometryNodeCornersOfEdge": {
        "display_name": "Corners of Edge",
        "category": "Mesh Topology",
        "description": "Gets face corners using an edge - for edge-to-face topology traversal.",
        "common_uses": [
            "Find faces sharing edge",
            "Boundary edge detection",
            "Edge-based topology"
        ],
        "pitfalls": [
            "Total 0 = loose edge (no faces)",
            "Total 1 = boundary edge",
            "Total 2 = manifold (internal) edge"
        ],
        "commonly_used_with": [
            ("Face of Corner", "get face from corner"),
            ("Edge Neighbors", "simpler face count"),
            ("Compare (Total = 1)", "find boundary edges"),
            ("Sample Index", "get corner data")
        ],
        "example": "Boundary detection: Corners of Edge Total = 1 → boundary edges. Get adjacent faces: corner indices → Face of Corner. Non-manifold: Total > 2."
    },
    
    # ==========================================================================
    # ROTATION NODES (additional)
    # ==========================================================================
    
    "FunctionNodeAxesToRotation": {
        "display_name": "Axes to Rotation",
        "category": "Rotation",
        "description": "Creates a rotation that aligns specified axes to given direction vectors.",
        "common_uses": [
            "Creating orientation from normals",
            "Aligning to surface",
            "Direction-based rotation",
            "Instance orientation"
        ],
        "pitfalls": [
            "Primary axis aligns exactly",
            "Secondary axis aligns as close as possible",
            "Directions should be orthogonal"
        ],
        "commonly_used_with": [
            ("Normal", "as primary direction"),
            ("Curve Tangent", "as secondary"),
            ("Rotate Instances", "apply rotation"),
            ("Instance on Points", "orient instances")
        ],
        "example": "Creates a rotation from two direction vectors - like pointing 'up' at a surface normal and 'forward' along a tangent. Primary axis aligns exactly to its direction, secondary aligns as close as possible. Perfect for orienting objects to surfaces."
    },
    
    "FunctionNodeQuaternionToRotation": {
        "display_name": "Quaternion to Rotation",
        "category": "Rotation",
        "description": "Converts quaternion values (W, X, Y, Z) to a standard rotation.",
        "common_uses": [
            "Importing quaternion data",
            "Animation data conversion",
            "External rotation data",
            "Math-based rotations"
        ],
        "pitfalls": [
            "WXYZ component order",
            "Should be normalized",
            "Different from Euler"
        ],
        "commonly_used_with": [
            ("Rotation to Quaternion", "reverse operation"),
            ("Math", "quaternion math"),
            ("Named Attribute", "read quaternion data"),
            ("Rotate Instances", "apply rotation")
        ],
        "example": "Converts quaternion rotation format (W, X, Y, Z components) to Blender's standard rotation. Quaternions are great for smooth interpolation and avoiding gimbal lock. Use when importing rotation data from other software."
    },
    
    "FunctionNodeRotationToQuaternion": {
        "display_name": "Rotation to Quaternion",
        "category": "Rotation",
        "description": "Converts a standard rotation to quaternion values (W, X, Y, Z).",
        "common_uses": [
            "Exporting rotation data",
            "Quaternion math",
            "Rotation interpolation",
            "Data conversion"
        ],
        "pitfalls": [
            "Outputs WXYZ components",
            "For advanced rotation math",
            "Normalized output"
        ],
        "commonly_used_with": [
            ("Quaternion to Rotation", "reverse operation"),
            ("Mix", "interpolate quaternions"),
            ("Store Named Attribute", "save quaternion"),
            ("Math", "quaternion operations")
        ],
        "example": "Converts standard rotation to quaternion format - four numbers (W, X, Y, Z) that represent rotation. Useful for smooth rotation blending, exporting to other software, or advanced rotation math."
    },
    
    "FunctionNodeMixRotation": {
        "display_name": "Mix Rotation",
        "category": "Rotation",
        "description": "Blends between two rotations - smooth quaternion interpolation (slerp).",
        "common_uses": [
            "Smooth rotation transitions",
            "Blend between orientations",
            "Animation interpolation"
        ],
        "pitfalls": [
            "Factor: 0 = A, 1 = B, 0.5 = halfway",
            "Takes shortest path (no flipping)",
            "Better than mixing Euler angles"
        ],
        "commonly_used_with": [
            ("Instance Rotation", "blend existing rotations"),
            ("Spline Parameter", "rotate along curve"),
            ("Scene Time", "animated blend"),
            ("Rotate Instances", "apply result")
        ],
        "example": "Smooth transition: Mix Rotation (A, B, animated Factor). Along curve: Spline Parameter as Factor between start/end rotations. Avoids gimbal lock unlike Euler mixing."
    },
    
    # ==========================================================================
    # MATRIX NODES
    # ==========================================================================
    
    "FunctionNodeCombineMatrix": {
        "display_name": "Combine Matrix",
        "category": "Matrix",
        "description": "Creates a 4x4 matrix from 16 individual values arranged in rows/columns.",
        "common_uses": [
            "Custom transformation matrices",
            "Mathematical transforms",
            "Advanced transform control",
            "Importing matrix data"
        ],
        "pitfalls": [
            "4x4 = 16 values",
            "Row-major order",
            "Homogeneous coordinates"
        ],
        "commonly_used_with": [
            ("Separate Matrix", "reverse operation"),
            ("Transform Point", "apply matrix"),
            ("Multiply Matrices", "combine transforms"),
            ("Invert Matrix", "reverse transform")
        ],
        "example": "Builds a 4x4 transformation matrix from 16 individual numbers. For advanced users who need complete control over transformations, or importing matrix data from external sources."
    },
    
    "FunctionNodeCombineTransform": {
        "display_name": "Combine Transform",
        "category": "Matrix",
        "description": "Creates a transformation matrix from translation, rotation, and scale values.",
        "common_uses": [
            "Building transforms",
            "Transform composition",
            "Matrix from components",
            "Instance transforms"
        ],
        "pitfalls": [
            "Order: translate, rotate, scale",
            "Creates 4x4 matrix",
            "Use for full transforms"
        ],
        "commonly_used_with": [
            ("Separate Transform", "reverse operation"),
            ("Set Instance Transform", "apply to instances"),
            ("Transform Point", "apply to positions"),
            ("Multiply Matrices", "chain transforms")
        ],
        "example": "Builds a complete transformation matrix from position, rotation, and scale. Like packaging up a transform to apply all at once. Use with Set Instance Transform to completely control how instances are placed."
    },
    
    "FunctionNodeSeparateMatrix": {
        "display_name": "Separate Matrix",
        "category": "Matrix",
        "description": "Extracts all 16 individual values from a 4x4 matrix.",
        "common_uses": [
            "Analyzing matrices",
            "Extracting matrix components",
            "Matrix debugging",
            "Advanced transform analysis"
        ],
        "pitfalls": [
            "Outputs 16 values",
            "Row and column indices",
            "For advanced use"
        ],
        "commonly_used_with": [
            ("Combine Matrix", "reverse operation"),
            ("Instance Transform", "analyze instance"),
            ("Math", "matrix component math"),
            ("Camera Info", "analyze projection")
        ],
        "example": "Breaks a 4x4 matrix into its 16 individual numbers. For advanced analysis of transformation matrices, like examining what a camera's projection matrix is actually doing."
    },
    
    "FunctionNodeSeparateTransform": {
        "display_name": "Separate Transform",
        "category": "Matrix",
        "description": "Extracts translation, rotation, and scale from a transformation matrix.",
        "common_uses": [
            "Decomposing transforms",
            "Reading instance transforms",
            "Transform analysis",
            "Component extraction"
        ],
        "pitfalls": [
            "May not perfectly reconstruct",
            "Shear is lost",
            "Scale can be approximate"
        ],
        "commonly_used_with": [
            ("Combine Transform", "reverse operation"),
            ("Instance Transform", "get instance TRS"),
            ("Object Info", "decompose object transform"),
            ("Set Position", "use translation only")
        ],
        "example": "Breaks a transformation matrix into its translation (position), rotation, and scale components. Use to read where an instance is, how it's rotated, and how big it is."
    },
    
    "FunctionNodeInvertMatrix": {
        "display_name": "Invert Matrix",
        "category": "Matrix",
        "description": "Calculates matrix inverse - applying then inverting returns identity.",
        "common_uses": [
            "Undo transforms",
            "World to local conversion",
            "Relative transforms"
        ],
        "pitfalls": [
            "Not all matrices invertible (zero scale fails)",
            "M × Inverse(M) = Identity",
            "Used for coordinate space conversion"
        ],
        "commonly_used_with": [
            ("Object Info", "world to local space"),
            ("Multiply Matrices", "apply then unapply"),
            ("Transform Point", "reverse transformation"),
            ("Instance Transform", "undo instance transform")
        ],
        "example": "World to local: Invert(Object Transform) → Transform Point = local coordinates. Undo transform: apply matrix, do work, apply inverse to return."
    },
    
    "FunctionNodeMultiplyMatrices": {
        "display_name": "Multiply Matrices",
        "category": "Matrix",
        "description": "Multiplies matrices to chain transformations - order matters.",
        "common_uses": [
            "Chain multiple transforms",
            "Combine transformations",
            "Sequential operations"
        ],
        "pitfalls": [
            "Order matters: A × B ≠ B × A",
            "Right matrix applies first (B then A)",
            "Combines rotation, scale, translation"
        ],
        "commonly_used_with": [
            ("Combine Transform", "create matrices to multiply"),
            ("Invert Matrix", "relative transforms"),
            ("Transform Point", "apply combined result"),
            ("Object Info", "chain with object transform")
        ],
        "example": "Parent-child: Parent × Child = combined transform. Chain: Rotate × Translate = rotate then translate. Order: B applies first, then A."
    },
    
    "FunctionNodeTransformPoint": {
        "display_name": "Transform Point",
        "category": "Matrix",
        "description": "Applies a transformation matrix to a point or vector.",
        "common_uses": [
            "Transforming positions",
            "Coordinate conversion",
            "Applying matrix to points",
            "Space transformation"
        ],
        "pitfalls": [
            "Point vs direction mode",
            "Directions ignore translation",
            "Full matrix application"
        ],
        "commonly_used_with": [
            ("Combine Transform", "create matrix"),
            ("Object Info", "object's transform"),
            ("Position", "points to transform"),
            ("Set Position", "apply result")
        ],
        "example": "Applies a transformation matrix to a point or direction. Use to convert positions between coordinate spaces, or apply complex transformations. 'Point' mode includes translation, 'Direction' mode ignores it."
    },
    
    "FunctionNodeTransformDirection": {
        "display_name": "Transform Direction",
        "category": "Matrix",
        "description": "Transforms a direction vector by a matrix, ignoring translation.",
        "common_uses": [
            "Rotating directions",
            "Normal transformation",
            "Direction space conversion",
            "Vector rotation"
        ],
        "pitfalls": [
            "No translation applied",
            "Only rotation and scale",
            "For direction vectors"
        ],
        "commonly_used_with": [
            ("Normal", "transform normals"),
            ("Curve Tangent", "transform tangents"),
            ("Object Info", "object's rotation"),
            ("Combine Transform", "create matrix")
        ],
        "example": "Transforms a direction vector (like a normal) using a matrix, but ignores the translation part. Directions don't have positions, so translation doesn't make sense for them."
    },
    
    "FunctionNodeProjectPoint": {
        "display_name": "Project Point",
        "category": "Matrix",
        "description": "Projects 3D point using projection matrix - for camera/screen space conversion.",
        "common_uses": [
            "3D to screen space",
            "Camera projection",
            "Render-based effects"
        ],
        "pitfalls": [
            "Uses 4×4 projection matrix",
            "Returns normalized device coordinates (-1 to 1)",
            "Behind camera = clipped"
        ],
        "commonly_used_with": [
            ("Camera Info", "get projection matrix"),
            ("Viewport Transform", "viewport projection"),
            ("Position", "points to project"),
            ("Map Range", "scale to pixel coordinates")
        ],
        "example": "Screen position: Camera projection matrix → Project Point on Position = where point appears on screen. Useful for billboards, screen-space effects."
    },
    
    "FunctionNodeMatrixDeterminant": {
        "display_name": "Matrix Determinant",
        "category": "Matrix",
        "description": "Calculates matrix determinant - indicates scale factor and invertibility.",
        "common_uses": [
            "Check if invertible",
            "Detect mirrored transforms",
            "Volume scale factor"
        ],
        "pitfalls": [
            "Zero = matrix not invertible",
            "Negative = orientation flipped (mirrored)",
            "|det| = volume scale factor"
        ],
        "commonly_used_with": [
            ("Compare", "check if zero"),
            ("Invert Matrix", "verify invertible first"),
            ("Math (Absolute)", "get scale factor"),
            ("Instance Transform", "analyze instances")
        ],
        "example": "Invertible check: Determinant ≠ 0. Mirror detection: Determinant < 0 = flipped. Scale factor: |Determinant| = how much volume changes."
    },
    
    "FunctionNodeTransposeMatrix": {
        "display_name": "Transpose Matrix",
        "category": "Matrix",
        "description": "Swaps matrix rows and columns - for orthogonal matrices equals inverse.",
        "common_uses": [
            "Fast rotation inverse",
            "Matrix math operations",
            "Normal transformation"
        ],
        "pitfalls": [
            "Rows become columns, columns become rows",
            "For pure rotation: Transpose = Inverse",
            "Advanced linear algebra operation"
        ],
        "commonly_used_with": [
            ("Invert Matrix", "alternative for rotations"),
            ("Multiply Matrices", "matrix math"),
            ("Transform Direction", "normal transformation"),
            ("Combine/Separate Matrix", "analyze")
        ],
        "example": "Fast rotation inverse: Transpose instead of Invert (same result, faster). Normal transform: use Transpose of inverse for correct normal rotation."
    },
    
    # ==========================================================================
    # COLOR NODES (additional)
    # ==========================================================================
    
    "ShaderNodeBlackbody": {
        "display_name": "Blackbody",
        "category": "Color",
        "description": "Converts temperature (Kelvin) to color - physically accurate light colors.",
        "common_uses": [
            "Realistic light colors",
            "Fire/flame coloring",
            "Sun/star colors"
        ],
        "pitfalls": [
            "Temperature in Kelvin (1000-10000 typical)",
            "1000K = warm red, 6500K = daylight, 10000K = blue",
            "Returns RGB color"
        ],
        "commonly_used_with": [
            ("Math", "temperature calculations"),
            ("Map Range", "normalize temperature"),
            ("Mix", "blend with other colors"),
            ("Emission shader", "realistic lights")
        ],
        "example": "Candle: 1800K. Tungsten bulb: 2700K. Daylight: 6500K. Blue sky: 10000K. Physically accurate light sources."
    },
    
    "ShaderNodeGamma": {
        "display_name": "Gamma",
        "category": "Color",
        "description": "Adjusts color gamma - brightens/darkens midtones while preserving black/white.",
        "common_uses": [
            "Adjust image contrast",
            "Color correction",
            "Texture tweaking"
        ],
        "pitfalls": [
            "Gamma < 1 = brighter midtones",
            "Gamma > 1 = darker midtones",
            "Gamma 1.0 = no change"
        ],
        "commonly_used_with": [
            ("Image Texture", "correct texture gamma"),
            ("Color Ramp", "additional control"),
            ("Brightness/Contrast", "alternative"),
            ("RGB Curves", "more control")
        ],
        "example": "Brighten texture: Gamma 0.5. Darken: Gamma 2.0. Linear to sRGB: Gamma 2.2. sRGB to Linear: Gamma 0.454."
    },
    
    "ShaderNodeCombineColor": {
        "display_name": "Combine Color",
        "category": "Color",
        "description": "Combines separate channels into single color - RGB, HSV, or HSL modes.",
        "common_uses": [
            "Build colors from components",
            "Procedural color generation",
            "Color manipulation"
        ],
        "pitfalls": [
            "Mode: RGB, HSV, or HSL",
            "RGB: Red/Green/Blue 0-1",
            "HSV: Hue 0-1 (wraps), Saturation 0-1, Value 0-1"
        ],
        "commonly_used_with": [
            ("Separate Color", "modify then recombine"),
            ("Math", "calculate channel values"),
            ("Noise Texture", "procedural channels"),
            ("Map Range", "normalize inputs")
        ],
        "example": "Rainbow: Noise → Hue input (HSV mode). Grayscale to color: value → all RGB channels. Saturation control: separate HSV, modify S, recombine."
    },
    
    "ShaderNodeSeparateColor": {
        "display_name": "Separate Color",
        "category": "Color",
        "description": "Splits color into separate channels - RGB, HSV, or HSL modes.",
        "common_uses": [
            "Extract color components",
            "Modify single channels",
            "Color analysis"
        ],
        "pitfalls": [
            "Mode: RGB, HSV, or HSL",
            "HSV Hue: 0-1 representing 0-360°",
            "Alpha not included (use Separate RGBA)"
        ],
        "commonly_used_with": [
            ("Combine Color", "modify then recombine"),
            ("Math", "process individual channels"),
            ("Compare", "color-based selection"),
            ("Map Range", "remap channel values")
        ],
        "example": "Desaturate: Separate HSV → set S to 0 → Combine. Hue shift: add to H channel. Extract luminance: V channel in HSV."
    },
    
    # ==========================================================================
    # CURVE OPERATIONS (additional)
    # ==========================================================================
    
    "GeometryNodeCurvesToGreasePencil": {
        "display_name": "Curves to Grease Pencil",
        "category": "Curve Operations",
        "description": "Converts curves to Grease Pencil strokes - for 2D drawing/animation.",
        "common_uses": [
            "Procedural Grease Pencil",
            "Convert 3D curves to 2D strokes",
            "Animated line art"
        ],
        "pitfalls": [
            "Output is Grease Pencil data",
            "Curves become strokes",
            "Material/color attributes transfer"
        ],
        "commonly_used_with": [
            ("Curve primitives", "source curves"),
            ("Set Curve Radius", "stroke thickness"),
            ("Resample Curve", "point density"),
            ("Grease Pencil modifier", "further processing")
        ],
        "example": "Procedural strokes: Curve Circle → Curves to Grease Pencil. Animated drawing: curves with animated trim → GP strokes."
    },
    
    # ==========================================================================
    # CURVE PRIMITIVES (additional)
    # ==========================================================================
    
    "GeometryNodeCurveQuadraticBezier": {
        "display_name": "Quadratic Bezier",
        "category": "Curve Primitives",
        "description": "Creates quadratic Bezier curve from 3 control points - simpler than cubic.",
        "common_uses": [
            "Simple curved paths",
            "Parabolic shapes",
            "UI/motion curves"
        ],
        "pitfalls": [
            "3 points: Start, Control, End",
            "Curve passes through Start and End only",
            "Control point pulls curve toward it"
        ],
        "commonly_used_with": [
            ("Curve to Mesh", "create ribbon"),
            ("Resample Curve", "add more points"),
            ("Instance on Points", "distribute along"),
            ("Trim Curve", "animate reveal")
        ],
        "example": "Arc: Start (0,0,0), Control (0.5,1,0), End (1,0,0) = parabolic arc. Resolution controls smoothness."
    },
    
    # ==========================================================================
    # CURVE READ (additional)
    # ==========================================================================
    
    "GeometryNodeInputTangent": {
        "display_name": "Curve Tangent",
        "category": "Curve Read",
        "description": "Reads tangent direction at each curve point - direction curve is heading.",
        "common_uses": [
            "Align objects along curve",
            "Flow direction",
            "Curve-based orientation"
        ],
        "pitfalls": [
            "Normalized vector (length 1)",
            "Points along curve direction",
            "Per-point, not per-spline"
        ],
        "commonly_used_with": [
            ("Align Euler to Vector", "orient along curve"),
            ("Rotate Instances", "follow curve direction"),
            ("Cross Product", "calculate normal/binormal"),
            ("Curve Normal", "complete frame")
        ],
        "example": "Train on track: Tangent → Align Euler to Vector → Rotate Instances. Arrow particles: tangent as forward direction."
    },
    
    # ==========================================================================
    # CURVE WRITE (additional - some already exist, adding missing ones)
    # ==========================================================================
    
    "GeometryNodeSetSplineType": {
        "display_name": "Set Spline Type",
        "category": "Curve Write",
        "description": "Converts splines between types - Bezier, Poly, NURBS, Catmull-Rom.",
        "common_uses": [
            "Convert Bezier to Poly for simplicity",
            "Add NURBS smoothness",
            "Change curve behavior"
        ],
        "pitfalls": [
            "Types: Catmull-Rom, Poly, Bezier, NURBS",
            "Poly = straight segments between points",
            "Conversion may change shape slightly"
        ],
        "commonly_used_with": [
            ("Curve primitives", "change default type"),
            ("Resample Curve", "after conversion"),
            ("Set Handle Type", "for Bezier curves"),
            ("Set Spline Resolution", "for NURBS")
        ],
        "example": "Sharp corners: Set Spline Type (Poly). Smooth: Set Spline Type (Catmull-Rom). Control: Bezier with handles."
    },
    
    # ==========================================================================
    # GREASE PENCIL OPERATIONS
    # ==========================================================================
    
    "GeometryNodeMergeGreasePencilLayers": {
        "display_name": "Merge Layers",
        "category": "Grease Pencil",
        "description": "Combines multiple Grease Pencil layers into one - flatten layer stack.",
        "common_uses": [
            "Flatten GP layers",
            "Combine strokes",
            "Simplify GP structure"
        ],
        "pitfalls": [
            "Merges all selected layers",
            "Order affects result",
            "Layer attributes combined"
        ],
        "commonly_used_with": [
            ("Curves to Grease Pencil", "create then merge"),
            ("Named Layer Selection", "select layers to merge"),
            ("GP modifiers", "process merged result"),
            ("Set GP Layer", "assign to specific layer")
        ],
        "example": "Flatten artwork: multiple layers → Merge Layers → single layer. Combine procedural strokes from different sources."
    },
    
    # ==========================================================================
    # INPUT CONSTANT NODES
    # ==========================================================================
    
    "GeometryNodeInputCollection": {
        "display_name": "Collection",
        "category": "Input",
        "description": "References a collection of objects - for instancing or iteration.",
        "common_uses": [
            "Source for Collection Info",
            "Instance multiple objects",
            "Object set reference"
        ],
        "pitfalls": [
            "Pick collection from dropdown",
            "Empty collection = no instances",
            "Nested collections supported"
        ],
        "commonly_used_with": [
            ("Collection Info", "get collection geometry"),
            ("Instance on Points", "random from collection"),
            ("Pick Instance", "select specific object"),
            ("Realize Instances", "convert to mesh")
        ],
        "example": "Scatter variations: Collection of tree variants → Collection Info → Instance on Points (Pick Random). Each point gets random tree."
    },
    
    "GeometryNodeInputImage": {
        "display_name": "Image",
        "category": "Input",
        "description": "References an image data-block - for texturing or data input.",
        "common_uses": [
            "Source for Image Texture",
            "Height map reference",
            "Texture data input"
        ],
        "pitfalls": [
            "Pick image from dropdown or load new",
            "Image must be loaded in Blender",
            "Use Image Info for dimensions"
        ],
        "commonly_used_with": [
            ("Image Texture", "sample the image"),
            ("Image Info", "get width/height"),
            ("Sample UV Surface", "UV-based sampling"),
            ("Grid", "create image-sized mesh")
        ],
        "example": "Height map displacement: Image → Image Texture → displacement. Reference texture for procedural effects."
    },
    
    "GeometryNodeInputMaterial": {
        "display_name": "Material",
        "category": "Input",
        "description": "References a material data-block - for assigning to geometry.",
        "common_uses": [
            "Material for Set Material",
            "Material parameter",
            "Conditional material assignment"
        ],
        "pitfalls": [
            "Pick material from dropdown",
            "Material must exist in Blender",
            "Use Set Material to apply"
        ],
        "commonly_used_with": [
            ("Set Material", "assign to faces"),
            ("Replace Material", "swap materials"),
            ("Switch", "conditional material"),
            ("Material Selection", "check assignment")
        ],
        "example": "Assign material: Material → Set Material. Conditional: Switch between Material inputs based on condition."
    },
    
    "FunctionNodeInputObject": {
        "display_name": "Object",
        "category": "Input",
        "description": "References an object data-block - alternative to Object Info input.",
        "common_uses": [
            "Object reference for nodes",
            "Target object parameter",
            "Dynamic object selection"
        ],
        "pitfalls": [
            "Pick object from scene",
            "Object must exist",
            "Use Object Info to get geometry/transform"
        ],
        "commonly_used_with": [
            ("Object Info", "get object's geometry"),
            ("Raycast", "target object"),
            ("Geometry Proximity", "distance to object"),
            ("Sample Nearest Surface", "sample from object")
        ],
        "example": "Target reference: Object → Object Info → use geometry. Raycast target: Object as target input."
    },
    
    "FunctionNodeInputRotation": {
        "display_name": "Rotation",
        "category": "Input",
        "description": "Rotation constant input - Euler angles in radians.",
        "common_uses": [
            "Fixed rotation value",
            "Rotation parameter",
            "Default orientation"
        ],
        "pitfalls": [
            "Values in radians (π = 180°)",
            "Euler XYZ order",
            "Use Euler to Rotation for conversion"
        ],
        "commonly_used_with": [
            ("Rotate Instances", "apply rotation"),
            ("Rotate Rotation", "combine rotations"),
            ("Transform Geometry", "rotate geometry"),
            ("Align Euler to Vector", "alternative input")
        ],
        "example": "90° X rotation: (π/2, 0, 0). Upside down: (π, 0, 0). Combined rotation parameter for node group."
    },
    
    "FunctionNodeInputString": {
        "display_name": "String",
        "category": "Input",
        "description": "Text string constant - for labels, names, or text operations.",
        "common_uses": [
            "Attribute names",
            "Text labels",
            "String parameters"
        ],
        "pitfalls": [
            "Plain text input",
            "Case-sensitive for attribute names",
            "Use Join Strings to combine"
        ],
        "commonly_used_with": [
            ("Named Attribute", "attribute name input"),
            ("Store Named Attribute", "name for stored data"),
            ("String to Curves", "create text geometry"),
            ("Join Strings", "combine strings")
        ],
        "example": "Attribute name: String 'my_color' → Named Attribute. Dynamic text: String → String to Curves."
    },
    
    # ==========================================================================
    # INPUT IMPORT
    # ==========================================================================
    
    "GeometryNodeOpenVDBRead": {
        "display_name": "Open VDB",
        "category": "Input",
        "description": "Imports volume data from OpenVDB file - industry standard volume format.",
        "common_uses": [
            "Import simulation caches",
            "Load volume data",
            "External VDB files"
        ],
        "pitfalls": [
            "Requires valid .vdb file path",
            "Grid names must match",
            "Large files = slow loading"
        ],
        "commonly_used_with": [
            ("Volume to Mesh", "convert to mesh"),
            ("Volume Cube", "alternative generation"),
            ("Sample Volume", "read volume values"),
            ("Set Volume Grid", "modify grids")
        ],
        "example": "Import smoke sim: Open VDB → file path → volume geometry. Access density grid for rendering."
    },
    
    # ==========================================================================
    # INPUT SCENE
    # ==========================================================================
    
    "GeometryNodeInputSceneTime": {
        "display_name": "Scene Time",
        "category": "Input",
        "description": "Outputs current frame and time - for animation and time-based effects.",
        "common_uses": [
            "Animated effects",
            "Time-based procedural",
            "Frame-dependent behavior"
        ],
        "pitfalls": [
            "Seconds: time in seconds",
            "Frame: current frame number",
            "Updates every frame"
        ],
        "commonly_used_with": [
            ("Math", "time calculations"),
            ("Sine/Cosine", "oscillating motion"),
            ("Noise Texture", "animated noise offset"),
            ("Map Range", "time remapping")
        ],
        "example": "Oscillation: sin(Seconds × speed). Frame counter: Frame output. Animated offset: Seconds × velocity → position offset."
    },
    
    # ==========================================================================
    # LAYOUT NODES
    # ==========================================================================
    
    "NodeFrame": {
        "display_name": "Frame",
        "category": "Layout",
        "description": "Visual container for organizing nodes - groups related nodes together.",
        "common_uses": [
            "Organize node tree",
            "Label sections",
            "Visual documentation"
        ],
        "pitfalls": [
            "Purely organizational (no function)",
            "Drag nodes into frame to add",
            "Ctrl+J to add selected nodes to frame"
        ],
        "commonly_used_with": [
            ("Any nodes", "organization"),
            ("Reroute", "cleaner connections"),
            ("Group Input/Output", "mark sections")
        ],
        "example": "Create Frame → drag related nodes inside → label it 'Displacement Setup'. Keeps complex trees organized and readable."
    },
    
    # ==========================================================================
    # MESH OPERATIONS (additional)
    # ==========================================================================
    
    "GeometryNodeEdgePathsToSelection": {
        "display_name": "Edge Paths to Selection",
        "category": "Mesh Operations",
        "description": "Finds shortest edge paths between marked vertices - creates edge selection.",
        "common_uses": [
            "Edge loop selection",
            "Path finding on mesh",
            "Connect distant vertices"
        ],
        "pitfalls": [
            "Start/End Vertices: boolean selection",
            "Finds shortest path along edges",
            "Returns edge selection"
        ],
        "commonly_used_with": [
            ("Compare", "mark start/end vertices"),
            ("Extrude Mesh", "extrude along path"),
            ("Set Shade Smooth", "smooth path edges"),
            ("Separate Geometry", "extract path")
        ],
        "example": "Connect corners: mark two vertices as Start/End → Edge Paths to Selection → edges along shortest path selected."
    },
    
    "GeometryNodeMeshToDensityGrid": {
        "display_name": "Mesh to Density Grid",
        "category": "Mesh Operations",
        "description": "Converts mesh to volume density grid - solid mesh becomes volume.",
        "common_uses": [
            "Mesh to volume conversion",
            "Volume-based effects",
            "Fog/cloud generation"
        ],
        "pitfalls": [
            "Resolution affects quality and memory",
            "Closed mesh recommended",
            "Output is volume grid"
        ],
        "commonly_used_with": [
            ("Volume to Mesh", "convert back"),
            ("Volume Cube", "combine volumes"),
            ("Sample Volume", "read density"),
            ("Set Volume Grid", "modify")
        ],
        "example": "Cloud from mesh: Mesh → Mesh to Density Grid → volume shader. Resolution 64+ for detail."
    },
    
    "GeometryNodeMeshToSDFGrid": {
        "display_name": "Mesh to SDF Grid",
        "category": "Mesh Operations",
        "description": "Converts mesh to Signed Distance Field - stores distance to surface.",
        "common_uses": [
            "Distance-based effects",
            "Volume boolean operations",
            "Collision detection"
        ],
        "pitfalls": [
            "SDF = distance to surface (negative inside)",
            "Higher resolution = more accurate",
            "Can be slow for complex meshes"
        ],
        "commonly_used_with": [
            ("SDF Grid Boolean", "volume booleans"),
            ("Volume to Mesh", "convert back"),
            ("Sample Grid", "read distance values"),
            ("SDF Grid Offset", "expand/shrink")
        ],
        "example": "SDF workflow: Mesh to SDF → SDF operations → Volume to Mesh. Smoother booleans than mesh booleans."
    },
    
    # ==========================================================================
    # MESH READ (additional)
    # ==========================================================================
    
    "GeometryNodeInputMeshEdgesToFaceGroups": {
        "display_name": "Edges to Face Groups",
        "category": "Mesh Read",
        "description": "Creates face groups from boundary edges - regions separated by marked edges.",
        "common_uses": [
            "Region identification",
            "Edge-based segmentation",
            "Face grouping"
        ],
        "pitfalls": [
            "Boundary Edges input: edge selection",
            "Each region gets unique ID",
            "Returns face domain values"
        ],
        "commonly_used_with": [
            ("Edge Angle", "auto boundary detection"),
            ("Material Index", "alternative grouping"),
            ("Random Value", "per-group randomness"),
            ("Split to Instances", "separate groups")
        ],
        "example": "Auto-segment: Edge Angle > 30° as Boundary → Edges to Face Groups → each smooth region gets ID."
    },
    
    "GeometryNodeInputMeshFaceGroupBoundaries": {
        "display_name": "Face Group Boundaries",
        "category": "Mesh Read",
        "description": "Finds edges at face group boundaries - where group IDs differ.",
        "common_uses": [
            "Find region edges",
            "Outline generation",
            "Group visualization"
        ],
        "pitfalls": [
            "Face Group ID input: per-face values",
            "Returns edge selection",
            "Edges where adjacent faces have different IDs"
        ],
        "commonly_used_with": [
            ("Material Index", "material boundaries"),
            ("Mesh Island", "island boundaries"),
            ("Extrude Mesh", "extrude boundaries"),
            ("Set Shade Smooth", "smooth within groups")
        ],
        "example": "Material outlines: Material Index → Face Group Boundaries → mark boundary edges for rendering."
    },
    
    "GeometryNodeInputShadeSmooth": {
        "display_name": "Is Face Smooth",
        "category": "Mesh Read",
        "description": "Reads smooth shading status per face - True if smooth shaded.",
        "common_uses": [
            "Check shading state",
            "Conditional operations",
            "Shading analysis"
        ],
        "pitfalls": [
            "Boolean per face",
            "True = smooth, False = flat",
            "Use Set Shade Smooth to modify"
        ],
        "commonly_used_with": [
            ("Set Shade Smooth", "modify shading"),
            ("Boolean Math", "combine conditions"),
            ("Switch", "conditional based on shading"),
            ("Separate Geometry", "split by shading")
        ],
        "example": "Select flat faces: NOT(Is Face Smooth) = flat shaded faces. Useful for identifying hard-surface vs organic areas."
    },
    
    "GeometryNodeInputEdgeSmooth": {
        "display_name": "Is Edge Smooth",
        "category": "Mesh Read",
        "description": "Reads edge smooth status - affects shading across edge.",
        "common_uses": [
            "Check edge sharpness",
            "Sharp edge detection",
            "Shading control"
        ],
        "pitfalls": [
            "Boolean per edge",
            "False = sharp edge (breaks smoothing)",
            "Different from face smooth"
        ],
        "commonly_used_with": [
            ("Set Shade Smooth", "edge smooth control"),
            ("Split Edges", "split sharp edges"),
            ("Boolean Math", "combine conditions"),
            ("Edge Angle", "auto-detect sharp")
        ],
        "example": "Find sharp edges: NOT(Is Edge Smooth) = marked sharp. Select for bevel or visualization."
    },
    
    # ==========================================================================
    # MESH UV
    # ==========================================================================
    
    "GeometryNodeInputMeshUVTangent": {
        "display_name": "UV Tangent",
        "category": "Mesh Read",
        "description": "Reads tangent vector from UV map - for tangent space calculations.",
        "common_uses": [
            "Normal mapping",
            "Tangent space effects",
            "UV-based orientation"
        ],
        "pitfalls": [
            "Requires UV map",
            "Per-corner output",
            "Tangent follows U direction"
        ],
        "commonly_used_with": [
            ("Normal", "complete TBN frame"),
            ("Cross Product", "calculate bitangent"),
            ("Named Attribute (UVMap)", "specify UV"),
            ("Normal Map", "tangent space normals")
        ],
        "example": "TBN matrix: Tangent (T), cross(Normal, Tangent) (B), Normal (N). For proper normal map application."
    },
    
    # ==========================================================================
    # MESH WRITE (additional)
    # ==========================================================================
    
    "GeometryNodeSetMeshNormal": {
        "display_name": "Set Mesh Normal",
        "category": "Mesh Write",
        "description": "Sets custom normal direction - override automatic normals.",
        "common_uses": [
            "Custom shading normals",
            "Face-weighted normals",
            "Artistic normal control"
        ],
        "pitfalls": [
            "Input should be normalized",
            "Overrides auto-calculated normals",
            "Per-corner or per-vertex"
        ],
        "commonly_used_with": [
            ("Normal", "read existing"),
            ("Vector Math (Normalize)", "ensure unit length"),
            ("Mix", "blend normals"),
            ("Sample Nearest Surface", "transfer normals")
        ],
        "example": "Flat shading: Face Normal → Set Mesh Normal (per corner). Smooth blend: mix normals between surfaces."
    },
    
    # ==========================================================================
    # OUTPUT
    # ==========================================================================
    
    "GeometryNodeEnableOutput": {
        "display_name": "Enable Output",
        "category": "Output",
        "description": "Conditionally enables/disables geometry output - for tool feedback.",
        "common_uses": [
            "Tool conditional output",
            "Debug visualization toggle",
            "Optional geometry"
        ],
        "pitfalls": [
            "Tool context primarily",
            "Enable = False skips output",
            "Used with multiple outputs"
        ],
        "commonly_used_with": [
            ("Group Output", "control which outputs active"),
            ("Switch", "select geometry"),
            ("Boolean", "enable condition"),
            ("Compare", "conditional enable")
        ],
        "example": "Debug toggle: Enable Output (debug viz) only when debug boolean True. Production: disable extra outputs."
    },
    
    # ==========================================================================
    # POINT (additional)
    # ==========================================================================
    
    "GeometryNodeDistributePointsInGrid": {
        "display_name": "Distribute Points in Grid",
        "category": "Point",
        "description": "Creates regular 3D grid of points - uniform point distribution.",
        "common_uses": [
            "Voxel-like point grids",
            "3D array of points",
            "Volume point distribution"
        ],
        "pitfalls": [
            "Spacing: distance between points",
            "Bounds: 3D region to fill",
            "Point count = (size/spacing)³"
        ],
        "commonly_used_with": [
            ("Instance on Points", "3D instance array"),
            ("Volume Cube", "bound to volume"),
            ("Delete Geometry", "remove points outside"),
            ("Points to Vertices", "convert to mesh")
        ],
        "example": "3D grid: Distribute Points in Grid → Instance Cubes = voxel grid. Use bounds to limit region."
    },
    
    "GeometryNodePointsToSDFGrid": {
        "display_name": "Points to SDF Grid",
        "category": "Point",
        "description": "Creates SDF volume from point cloud - spherical influence per point.",
        "common_uses": [
            "Metaball-like effect",
            "Point cloud to volume",
            "Blobby surfaces"
        ],
        "pitfalls": [
            "Radius: point influence radius",
            "Points blend together smoothly",
            "Resolution affects quality"
        ],
        "commonly_used_with": [
            ("Distribute Points", "source points"),
            ("Volume to Mesh", "extract surface"),
            ("Set Point Radius", "vary influence"),
            ("SDF Grid Offset", "adjust surface")
        ],
        "example": "Metaballs: Random points → Points to SDF Grid → Volume to Mesh. Points near each other merge smoothly."
    },
    
    # ==========================================================================
    # SIMULATION (additional)
    # ==========================================================================
    
    "GeometryNodeSimulationOutput": {
        "display_name": "Simulation Output",
        "category": "Simulation",
        "description": "End of Simulation Zone - outputs and feeds back to next frame.",
        "common_uses": [
            "Complete simulation zone",
            "Define simulation outputs",
            "Frame-persistent data"
        ],
        "pitfalls": [
            "Must pair with Simulation Input",
            "Data persists between frames",
            "Add sockets by dragging connections"
        ],
        "commonly_used_with": [
            ("Simulation Input", "always paired"),
            ("Set Position", "update positions"),
            ("Store Named Attribute", "persistent attributes"),
            ("Delete Geometry", "remove elements")
        ],
        "example": "Physics sim: Simulation Input geometry → modify positions → Simulation Output (same geometry socket). State carries to next frame."
    },
    
    # ==========================================================================
    # TEXTURE (additional)
    # ==========================================================================
    
    "ShaderNodeTexGabor": {
        "display_name": "Gabor Texture",
        "category": "Texture",
        "description": "Generates Gabor noise - oriented bands useful for anisotropic patterns.",
        "common_uses": [
            "Wood grain patterns",
            "Brushed metal",
            "Directional textures"
        ],
        "pitfalls": [
            "Direction controls band orientation",
            "Frequency controls band density",
            "Anisotropic = direction-dependent"
        ],
        "commonly_used_with": [
            ("Mapping", "control orientation"),
            ("Color Ramp", "map to colors"),
            ("Bump", "surface detail"),
            ("Mix", "combine with other textures")
        ],
        "example": "Wood grain: Gabor Texture (horizontal direction) → Color Ramp (brown gradient). Brushed metal: fine frequency, tangent direction."
    },
    
    # ==========================================================================
    # UTILITIES - FOR EACH ELEMENT
    # ==========================================================================
    
    "GeometryNodeForEachElementInput": {
        "display_name": "For Each Geometry Element Input",
        "category": "Utilities",
        "description": "Start of For Each Element zone - processes each element individually.",
        "common_uses": [
            "Per-face operations",
            "Per-point processing",
            "Individual element transforms"
        ],
        "pitfalls": [
            "Domain: Point, Edge, Face, Spline, etc.",
            "Each element processed separately",
            "Index available inside zone"
        ],
        "commonly_used_with": [
            ("For Each Element Output", "end zone"),
            ("Element Index", "current element"),
            ("Extrude Mesh", "per-face extrusion"),
            ("Transform Geometry", "per-element transform")
        ],
        "example": "Per-face extrusion: For Each Element (Face) → Extrude → random amount per face. Processes each face independently."
    },
    
    "GeometryNodeForEachElementOutput": {
        "display_name": "For Each Geometry Element Output",
        "category": "Utilities",
        "description": "End of For Each Element zone - collects processed elements.",
        "common_uses": [
            "Complete per-element loop",
            "Gather processed results",
            "Join individually processed elements"
        ],
        "pitfalls": [
            "Must pair with For Each Element Input",
            "Results joined automatically",
            "Can output main geometry + generated geometry"
        ],
        "commonly_used_with": [
            ("For Each Element Input", "always paired"),
            ("Join Geometry", "if combining inside"),
            ("Set Position", "per-element modification"),
            ("Instance on Points", "per-element instancing")
        ],
        "example": "Per-face effect: Input → modify each face → Output. All modified faces rejoin automatically."
    },
    
    # ==========================================================================
    # UTILITIES - REPEAT
    # ==========================================================================
    
    "GeometryNodeRepeatOutput": {
        "display_name": "Repeat Output",
        "category": "Utilities",
        "description": "End of Repeat zone - feeds result back for next iteration.",
        "common_uses": [
            "Complete repeat loop",
            "Iterative refinement",
            "Recursive patterns"
        ],
        "pitfalls": [
            "Must pair with Repeat Input",
            "Output feeds back to Input",
            "Iterations set on Input node"
        ],
        "commonly_used_with": [
            ("Repeat Input", "always paired"),
            ("Subdivide Mesh", "iterative subdivision"),
            ("Extrude Mesh", "recursive extrusion"),
            ("Transform Geometry", "repeated transforms")
        ],
        "example": "Fractal: Repeat Input → Subdivide → displace → Repeat Output. Each iteration adds detail level."
    },
    
    # ==========================================================================
    # UTILITIES - BUNDLE
    # ==========================================================================
    
    "GeometryNodeCombineBundle": {
        "display_name": "Combine Bundle",
        "category": "Utilities",
        "description": "Packs multiple values into single bundle socket - simplifies connections.",
        "common_uses": [
            "Group multiple outputs",
            "Simplify node connections",
            "Pass related data together"
        ],
        "pitfalls": [
            "Bundle = container for multiple values",
            "Add sockets by dragging to node",
            "Types preserved inside bundle"
        ],
        "commonly_used_with": [
            ("Separate Bundle", "unpack values"),
            ("Group Input/Output", "cleaner interfaces"),
            ("Reroute", "single wire for multiple values"),
            ("Switch", "switch entire bundles")
        ],
        "example": "Combine position + color + scale → single bundle wire → Separate Bundle at destination. Cleaner node trees."
    },
    
    "GeometryNodeSeparateBundle": {
        "display_name": "Separate Bundle",
        "category": "Utilities",
        "description": "Unpacks bundle into separate value sockets - inverse of Combine Bundle.",
        "common_uses": [
            "Extract bundled values",
            "Access grouped data",
            "Unpack at destination"
        ],
        "pitfalls": [
            "Outputs match Combine Bundle inputs",
            "Order and types preserved",
            "Missing values = default"
        ],
        "commonly_used_with": [
            ("Combine Bundle", "created bundle"),
            ("Group Input", "receive bundle parameter"),
            ("Switch", "after switching bundles"),
            ("Any node", "use extracted values")
        ],
        "example": "Receive bundle → Separate Bundle → use position for Set Position, color for Set Material, etc."
    },
    
    "GeometryNodeJoinBundle": {
        "display_name": "Join Bundle",
        "category": "Utilities",
        "description": "Merges multiple bundles into one - combines bundle contents.",
        "common_uses": [
            "Merge data streams",
            "Combine bundle collections",
            "Aggregate bundled data"
        ],
        "pitfalls": [
            "Input bundles must have compatible structure",
            "Values with same name merged/overwritten",
            "New bundle contains all values"
        ],
        "commonly_used_with": [
            ("Combine Bundle", "create input bundles"),
            ("Separate Bundle", "extract from result"),
            ("For Each Element", "collect per-element bundles"),
            ("Group Output", "single bundle output")
        ],
        "example": "Join Bundle from multiple processing branches → single bundle containing all computed values."
    },
    
    # ==========================================================================
    # UTILITIES - CLOSURE
    # ==========================================================================
    
    "GeometryNodeClosureInput": {
        "display_name": "Closure Input",
        "category": "Utilities",
        "description": "Input for closure zone - defines captured variables.",
        "common_uses": [
            "Deferred evaluation",
            "Callback-like patterns",
            "Lazy evaluation"
        ],
        "pitfalls": [
            "Closure = packaged computation",
            "Captures values at creation time",
            "Evaluated later with Evaluate Closure"
        ],
        "commonly_used_with": [
            ("Closure Output", "end closure zone"),
            ("Evaluate Closure", "execute the closure"),
            ("Menu Switch", "closure-based selection"),
            ("Index Switch", "closure selection")
        ],
        "example": "Define computation in closure → pass closure as data → Evaluate Closure when needed. Deferred execution pattern."
    },
    
    "GeometryNodeClosureOutput": {
        "display_name": "Closure Output",
        "category": "Utilities",
        "description": "Output for closure zone - completes closure definition.",
        "common_uses": [
            "Complete closure definition",
            "Package computation",
            "Define deferred operation"
        ],
        "pitfalls": [
            "Must pair with Closure Input",
            "Outputs closure data type",
            "Closure executed via Evaluate Closure"
        ],
        "commonly_used_with": [
            ("Closure Input", "always paired"),
            ("Evaluate Closure", "execute result"),
            ("Switch", "select between closures"),
            ("Group Output", "expose closure")
        ],
        "example": "Closure Input → computation nodes → Closure Output = packaged computation. Pass around, evaluate when needed."
    },
    
    "GeometryNodeEvaluateClosure": {
        "display_name": "Evaluate Closure",
        "category": "Utilities",
        "description": "Executes a closure - runs the packaged computation.",
        "common_uses": [
            "Execute deferred computation",
            "Run selected closure",
            "Trigger packaged operation"
        ],
        "pitfalls": [
            "Input: closure from Closure Output",
            "Executes computation defined in closure",
            "Can pass additional inputs"
        ],
        "commonly_used_with": [
            ("Closure Output", "closure source"),
            ("Switch", "select which closure to evaluate"),
            ("For Each Element", "evaluate per element"),
            ("Group Input", "closure as parameter")
        ],
        "example": "User selects operation (closure) → Evaluate Closure runs it. Plugin-like extensibility pattern."
    },
    
    # ==========================================================================
    # UTILITIES - FIELD
    # ==========================================================================
    
    "GeometryNodeFieldMinMax": {
        "display_name": "Field Min & Max",
        "category": "Utilities",
        "description": "Finds minimum and maximum values in a field - range detection.",
        "common_uses": [
            "Find value range",
            "Normalize data",
            "Range-based operations"
        ],
        "pitfalls": [
            "Evaluates entire field",
            "Returns single min and max value",
            "Works on geometry domain"
        ],
        "commonly_used_with": [
            ("Map Range", "normalize using min/max"),
            ("Attribute Statistic", "more statistics"),
            ("Position", "find bounding values"),
            ("Any float field", "range detection")
        ],
        "example": "Auto-normalize: Field Min & Max → Map Range (From Min/Max to 0/1). Height coloring: position Z min/max → gradient."
    },
    
    "GeometryNodeFieldVariance": {
        "display_name": "Field Variance",
        "category": "Utilities",
        "description": "Calculates statistical variance of field values - measures spread.",
        "common_uses": [
            "Measure data spread",
            "Uniformity detection",
            "Statistical analysis"
        ],
        "pitfalls": [
            "Variance = average squared deviation from mean",
            "Higher = more spread out",
            "Zero = all values identical"
        ],
        "commonly_used_with": [
            ("Attribute Statistic", "mean/median/etc"),
            ("Field Min & Max", "range"),
            ("Compare", "threshold variance"),
            ("Math (Square Root)", "standard deviation")
        ],
        "example": "Uniformity check: low variance = consistent values. Quality metric: high variance in normals = rough surface."
    },
    
    # ==========================================================================
    # UTILITIES - MATH (additional)
    # ==========================================================================
    
    "FunctionNodeBitMath": {
        "display_name": "Bit Math",
        "category": "Utilities",
        "description": "Bitwise operations on integers - AND, OR, XOR, NOT, shifts.",
        "common_uses": [
            "Flag manipulation",
            "Binary data processing",
            "Efficient integer math"
        ],
        "pitfalls": [
            "Operations: AND, OR, XOR, NOT, SHIFT",
            "Works on integer bits",
            "Useful for packed data"
        ],
        "commonly_used_with": [
            ("Integer Math", "integer calculations"),
            ("Compare", "bit testing"),
            ("Index", "bit manipulation of indices"),
            ("Float to Integer", "convert first")
        ],
        "example": "Extract flag: value AND mask. Set flag: value OR flag. Toggle: value XOR flag. Check bit: (value AND bit) != 0."
    },
    
    "FunctionNodeIntegerMath": {
        "display_name": "Integer Math",
        "category": "Utilities",
        "description": "Math operations that preserve integer type - no floating point.",
        "common_uses": [
            "Index calculations",
            "Integer division",
            "Modulo operations"
        ],
        "pitfalls": [
            "Results stay as integers",
            "Division truncates (no fractions)",
            "Modulo for wrapping/cycling"
        ],
        "commonly_used_with": [
            ("Index", "index math"),
            ("Math", "float operations when needed"),
            ("Compare", "integer comparison"),
            ("Switch", "integer-based selection")
        ],
        "example": "Grid index: row = index // columns, col = index % columns. Cycle: index % count = wrapping index."
    },
    
    "FunctionNodeHashValue": {
        "display_name": "Hash Value",
        "category": "Utilities",
        "description": "Generates deterministic hash from input - consistent pseudo-random.",
        "common_uses": [
            "Deterministic randomness",
            "ID-based variation",
            "Consistent random per element"
        ],
        "pitfalls": [
            "Same input = same output always",
            "Output appears random but repeatable",
            "Seed changes output pattern"
        ],
        "commonly_used_with": [
            ("Index", "per-element hash"),
            ("ID", "instance-based hash"),
            ("Map Range", "scale hash output"),
            ("Compare", "probability threshold")
        ],
        "example": "Deterministic scatter: Hash(ID + seed) → rotation/scale variation. Same seed = same result every time."
    },
    
    # ==========================================================================
    # UTILITIES - ROTATION (additional)
    # ==========================================================================
    
    "FunctionNodeAlignRotationToVector": {
        "display_name": "Align Rotation to Vector",
        "category": "Utilities",
        "description": "Creates rotation that aligns an axis to a vector direction.",
        "common_uses": [
            "Point objects at targets",
            "Align to normals",
            "Direction-based orientation"
        ],
        "pitfalls": [
            "Axis: which local axis to align (X/Y/Z)",
            "Pivot Axis: secondary alignment constraint",
            "Factor: blend amount (0-1)"
        ],
        "commonly_used_with": [
            ("Normal", "align to surface"),
            ("Curve Tangent", "align along curve"),
            ("Rotate Instances", "apply result"),
            ("Vector Math (Normalize)", "ensure unit direction")
        ],
        "example": "Trees on terrain: Align Z axis to Normal → trees point away from surface. Arrows: align Y to velocity direction."
    },
    
    "FunctionNodeRotationToAxisAngle": {
        "display_name": "Rotation to Axis Angle",
        "category": "Utilities",
        "description": "Converts rotation to axis-angle representation - single axis plus angle.",
        "common_uses": [
            "Extract rotation axis",
            "Get rotation amount",
            "Axis-angle workflows"
        ],
        "pitfalls": [
            "Axis: normalized vector",
            "Angle: rotation amount in radians",
            "Any rotation = axis + angle around it"
        ],
        "commonly_used_with": [
            ("Axis Angle to Rotation", "reverse conversion"),
            ("Vector Math", "process axis"),
            ("Math", "process angle"),
            ("Map Range", "remap angle")
        ],
        "example": "Analyze rotation: Rotation to Axis Angle → use angle for color gradient, axis for secondary alignment."
    },
    
    # ==========================================================================
    # UTILITIES - TEXT (additional)
    # ==========================================================================
    
    "FunctionNodeFormatString": {
        "display_name": "Format String",
        "category": "Utilities",
        "description": "Creates formatted string from template with placeholders.",
        "common_uses": [
            "Dynamic text generation",
            "Number formatting",
            "Template-based strings"
        ],
        "pitfalls": [
            "Use {} as placeholders",
            "Arguments fill placeholders in order",
            "Add inputs by connecting values"
        ],
        "commonly_used_with": [
            ("String to Curves", "display formatted text"),
            ("Value to String", "number conversion"),
            ("Join Strings", "complex formatting"),
            ("Index", "numbered labels")
        ],
        "example": "Label: 'Point {}' with Index = 'Point 0', 'Point 1', etc. Score: 'Score: {}' with value."
    },
    
    "FunctionNodeJoinStrings": {
        "display_name": "Join Strings",
        "category": "Utilities",
        "description": "Concatenates multiple strings with optional delimiter.",
        "common_uses": [
            "Combine text parts",
            "Build file paths",
            "Create compound names"
        ],
        "pitfalls": [
            "Delimiter inserted between strings",
            "Empty delimiter = direct concatenation",
            "Add inputs by connecting strings"
        ],
        "commonly_used_with": [
            ("String", "string inputs"),
            ("Value to String", "include numbers"),
            ("Format String", "formatted parts"),
            ("String to Curves", "display result")
        ],
        "example": "Path: Join('/folder', 'file', '.txt') = '/folder/file/.txt'. CSV: Join with delimiter ','."
    },
    
    "FunctionNodeMatchString": {
        "display_name": "Match String",
        "category": "Utilities",
        "description": "Checks if string matches pattern - returns boolean.",
        "common_uses": [
            "Pattern matching",
            "Name filtering",
            "Conditional text logic"
        ],
        "pitfalls": [
            "Pattern: text to match",
            "Case sensitive by default",
            "Returns True/False"
        ],
        "commonly_used_with": [
            ("Named Attribute", "check attribute names"),
            ("Switch", "conditional on match"),
            ("Boolean Math", "combine conditions"),
            ("String", "pattern input")
        ],
        "example": "Filter by name: Match String ('LOD_*') → select objects starting with 'LOD_'."
    },
    
    "FunctionNodeFindInString": {
        "display_name": "Find in String",
        "category": "Utilities",
        "description": "Finds position of substring within string - returns index.",
        "common_uses": [
            "Locate text within string",
            "Parse string content",
            "Check substring existence"
        ],
        "pitfalls": [
            "Returns -1 if not found",
            "Position: starting index (0-based)",
            "First occurrence only"
        ],
        "commonly_used_with": [
            ("Compare", "check if found (>= 0)"),
            ("Slice String", "extract around position"),
            ("String", "search term"),
            ("Switch", "conditional on found")
        ],
        "example": "Check extension: Find '.obj' in filename. If >= 0, it's an OBJ file."
    },
    
    "FunctionNodeStringToValue": {
        "display_name": "String to Value",
        "category": "Utilities",
        "description": "Converts string containing number to float value.",
        "common_uses": [
            "Parse numeric strings",
            "Read text data as numbers",
            "Convert imported text"
        ],
        "pitfalls": [
            "String must contain valid number",
            "Invalid string = 0",
            "Handles decimals and negatives"
        ],
        "commonly_used_with": [
            ("String", "number as text"),
            ("Import CSV", "parsed values"),
            ("Math", "use converted value"),
            ("Compare", "numeric comparison")
        ],
        "example": "Parse data: '3.14' → 3.14 float. Height from text attribute → numeric height value."
    },
    
    "FunctionNodeSpecialCharacters": {
        "display_name": "Special Characters",
        "category": "Utilities",
        "description": "Outputs special text characters - newline, tab, etc.",
        "common_uses": [
            "Multi-line text",
            "Formatted output",
            "Text layout control"
        ],
        "pitfalls": [
            "Line Break: newline character",
            "Tab: horizontal tab",
            "Use with Join Strings"
        ],
        "commonly_used_with": [
            ("Join Strings", "insert special chars"),
            ("String to Curves", "multi-line text"),
            ("Format String", "formatted output"),
            ("String", "combine with text")
        ],
        "example": "Multi-line label: Join('Line 1', Line Break, 'Line 2') → text on two lines."
    },
    
    # ==========================================================================
    # UTILITIES - VECTOR (additional)
    # ==========================================================================
    
    "GeometryNodeRadialTiling": {
        "display_name": "Radial Tiling",
        "category": "Utilities",
        "description": "Tiles/repeats pattern radially around an axis - circular repetition.",
        "common_uses": [
            "Circular patterns",
            "Radial symmetry",
            "Wheel/gear patterns"
        ],
        "pitfalls": [
            "Count: number of repetitions",
            "Center: axis center point",
            "Modifies UV/position for tiling"
        ],
        "commonly_used_with": [
            ("Texture Coordinate", "radial UV"),
            ("Noise Texture", "tiled noise"),
            ("Instance on Points", "radial instances"),
            ("Math (Modulo)", "manual tiling")
        ],
        "example": "6-fold symmetry: Radial Tiling (count 6) → pattern repeats 6 times around center. Snowflake, flower patterns."
    },
    
    # ==========================================================================
    # VOLUME OPERATIONS
    # ==========================================================================
    
    "GeometryNodeGridToMesh": {
        "display_name": "Grid to Mesh",
        "category": "Volume",
        "description": "Converts volume grid to mesh surface - marching cubes algorithm.",
        "common_uses": [
            "Volume to mesh conversion",
            "Isosurface extraction",
            "SDF visualization"
        ],
        "pitfalls": [
            "Threshold: surface level (0 for SDF)",
            "Adaptivity: mesh simplification (0 = exact)",
            "Resolution affects detail"
        ],
        "commonly_used_with": [
            ("Mesh to SDF Grid", "SDF source"),
            ("Volume Cube", "volume source"),
            ("Smooth Shading", "smooth result"),
            ("Decimate", "reduce polygons")
        ],
        "example": "SDF to mesh: Mesh to SDF → operations → Grid to Mesh (threshold 0). Cloud render: density grid → mesh → shader."
    },
    
    "GeometryNodeSDFGridBoolean": {
        "display_name": "SDF Grid Boolean",
        "category": "Volume",
        "description": "Boolean operations on SDF volumes - union, intersect, subtract.",
        "common_uses": [
            "Volume CSG operations",
            "Smooth booleans",
            "Shape combination"
        ],
        "pitfalls": [
            "Operations: Union, Intersect, Difference",
            "SDF booleans are smoother than mesh",
            "Both inputs must be SDF grids"
        ],
        "commonly_used_with": [
            ("Mesh to SDF Grid", "convert meshes"),
            ("Grid to Mesh", "convert result back"),
            ("SDF Grid Offset", "expand/shrink"),
            ("SDF Grid Fillet", "round edges")
        ],
        "example": "Smooth subtraction: Mesh A → SDF, Mesh B → SDF, Boolean Difference → Grid to Mesh. Smoother than mesh boolean."
    },
    
    "GeometryNodeSDFGridFillet": {
        "display_name": "SDF Grid Fillet",
        "category": "Volume",
        "description": "Rounds edges in SDF volume - smooth transitions.",
        "common_uses": [
            "Round sharp edges",
            "Smooth boolean results",
            "Organic shapes"
        ],
        "pitfalls": [
            "Radius: fillet size",
            "Works best after boolean ops",
            "Larger radius = more rounding"
        ],
        "commonly_used_with": [
            ("SDF Grid Boolean", "before filleting"),
            ("Grid to Mesh", "convert result"),
            ("Mesh to SDF Grid", "source"),
            ("SDF Grid Offset", "combine effects")
        ],
        "example": "Rounded box: Cube → SDF → Fillet (radius 0.1) → Grid to Mesh. Smooth edges without manual modeling."
    },
    
    "GeometryNodeSDFGridLaplacian": {
        "display_name": "SDF Grid Laplacian",
        "category": "Volume",
        "description": "Applies Laplacian smoothing to SDF - smooths surface details.",
        "common_uses": [
            "Smooth SDF surface",
            "Remove noise",
            "Simplify shape"
        ],
        "pitfalls": [
            "Iterations: smoothing passes",
            "More iterations = smoother",
            "Can lose small details"
        ],
        "commonly_used_with": [
            ("Mesh to SDF Grid", "noisy input"),
            ("Grid to Mesh", "convert result"),
            ("SDF Grid Boolean", "smooth boolean results"),
            ("Points to SDF Grid", "smooth point cloud")
        ],
        "example": "Smooth scan data: noisy mesh → SDF → Laplacian smooth → clean mesh. Remove scanning artifacts."
    },
    
    "GeometryNodeSDFGridMean": {
        "display_name": "SDF Grid Mean",
        "category": "Volume",
        "description": "Mean filter on SDF grid - averages neighboring values.",
        "common_uses": [
            "Noise reduction",
            "Blur SDF",
            "Smooth gradients"
        ],
        "pitfalls": [
            "Width: filter kernel size",
            "Larger = more blur",
            "Affects distance values"
        ],
        "commonly_used_with": [
            ("Mesh to SDF Grid", "input"),
            ("Grid to Mesh", "output"),
            ("SDF Grid Boolean", "smooth results"),
            ("Sample Grid", "sample smoothed")
        ],
        "example": "Blur SDF: Mean filter before Grid to Mesh = softer surface transitions."
    },
    
    "GeometryNodeSDFGridMeanCurvature": {
        "display_name": "SDF Grid Mean Curvature",
        "category": "Volume",
        "description": "Curvature-based smoothing on SDF - preserves features better.",
        "common_uses": [
            "Feature-preserving smooth",
            "Curvature flow",
            "Artistic smoothing"
        ],
        "pitfalls": [
            "Preserves sharp features better than Mean",
            "Iterations control amount",
            "Good for organic shapes"
        ],
        "commonly_used_with": [
            ("Mesh to SDF Grid", "input"),
            ("Grid to Mesh", "convert result"),
            ("SDF Grid Boolean", "smooth booleans"),
            ("SDF Grid Laplacian", "alternative")
        ],
        "example": "Smooth while preserving edges: Mean Curvature keeps corners sharper than regular smoothing."
    },
    
    "GeometryNodeSDFGridMedian": {
        "display_name": "SDF Grid Median",
        "category": "Volume",
        "description": "Median filter on SDF grid - removes outliers while preserving edges.",
        "common_uses": [
            "Remove speckle noise",
            "Edge-preserving denoise",
            "Clean scan data"
        ],
        "pitfalls": [
            "Median = middle value (not average)",
            "Good for salt-and-pepper noise",
            "Preserves edges better than mean"
        ],
        "commonly_used_with": [
            ("Points to SDF Grid", "clean point cloud SDF"),
            ("Grid to Mesh", "convert result"),
            ("SDF Grid Mean", "combine filters"),
            ("Mesh to SDF Grid", "noisy input")
        ],
        "example": "Clean scan: noisy SDF → Median filter → outliers removed, edges preserved."
    },
    
    "GeometryNodeSDFGridOffset": {
        "display_name": "SDF Grid Offset",
        "category": "Volume",
        "description": "Expands or shrinks SDF surface - offset distance.",
        "common_uses": [
            "Inflate/deflate shapes",
            "Create shells",
            "Adjust surface position"
        ],
        "pitfalls": [
            "Positive offset = expand outward",
            "Negative offset = shrink inward",
            "Amount in Blender units"
        ],
        "commonly_used_with": [
            ("Mesh to SDF Grid", "input"),
            ("Grid to Mesh", "convert result"),
            ("SDF Grid Boolean", "before/after booleans"),
            ("SDF Grid Fillet", "combine with rounding")
        ],
        "example": "Shell: Original SDF, Offset copy (negative), Boolean Difference = hollow shell. Padding: positive offset around mesh."
    },
    
    "GeometryNodeFieldToGrid": {
        "display_name": "Field to Grid",
        "category": "Volume",
        "description": "Converts field values to volume grid - sample field into voxels.",
        "common_uses": [
            "Bake field to volume",
            "Create custom volume data",
            "Field-based volumes"
        ],
        "pitfalls": [
            "Resolution: voxel density",
            "Position field sampled at voxel centers",
            "Creates density/SDF grid"
        ],
        "commonly_used_with": [
            ("Noise Texture", "noise field to volume"),
            ("Position", "position-based volume"),
            ("Math", "computed field values"),
            ("Volume to Mesh", "visualize")
        ],
        "example": "Noise volume: Noise Texture field → Field to Grid → volume with noise density pattern."
    },
    
    "GeometryNodePruneGrid": {
        "display_name": "Prune Grid",
        "category": "Volume",
        "description": "Removes inactive voxels from grid - optimize volume data.",
        "common_uses": [
            "Optimize volume memory",
            "Clean up sparse grids",
            "Remove empty regions"
        ],
        "pitfalls": [
            "Removes voxels below threshold",
            "Reduces memory usage",
            "May affect boundaries slightly"
        ],
        "commonly_used_with": [
            ("Mesh to SDF Grid", "clean result"),
            ("Volume operations", "after processing"),
            ("Grid to Mesh", "before conversion"),
            ("Points to SDF Grid", "optimize")
        ],
        "example": "Memory optimization: after volume operations → Prune Grid → remove unused voxels."
    },
    
    "GeometryNodeVoxelizeGrid": {
        "display_name": "Voxelize Grid",
        "category": "Volume",
        "description": "Changes grid resolution - resample volume at different voxel size.",
        "common_uses": [
            "Change volume resolution",
            "Upscale/downscale volume",
            "Match grid resolutions"
        ],
        "pitfalls": [
            "Voxel Size: new voxel dimensions",
            "Smaller = more detail, more memory",
            "Resamples existing data"
        ],
        "commonly_used_with": [
            ("Mesh to SDF Grid", "adjust resolution"),
            ("Grid to Mesh", "before conversion"),
            ("SDF Grid Boolean", "match resolutions"),
            ("Volume Cube", "resample")
        ],
        "example": "High-res output: low-res SDF operations → Voxelize (smaller voxels) → Grid to Mesh for detail."
    },
    
    # ==========================================================================
    # VOLUME READ
    # ==========================================================================
    
    "GeometryNodeGetNamedGrid": {
        "display_name": "Get Named Grid",
        "category": "Volume",
        "description": "Retrieves a specific named grid from volume - access volume channels.",
        "common_uses": [
            "Access specific volume data",
            "Get density/velocity/etc grids",
            "Multi-channel volumes"
        ],
        "pitfalls": [
            "Name: grid name (e.g., 'density')",
            "Common names: density, temperature, velocity",
            "Returns single grid"
        ],
        "commonly_used_with": [
            ("Open VDB", "multi-grid VDB files"),
            ("Store Named Grid", "custom grids"),
            ("Sample Grid", "read values"),
            ("Grid to Mesh", "visualize specific grid")
        ],
        "example": "Access smoke density: Get Named Grid 'density' → Sample Grid for values. Simulation channels: temperature, velocity."
    },
    
    "GeometryNodeGridInfo": {
        "display_name": "Grid Info",
        "category": "Volume",
        "description": "Outputs information about a volume grid - dimensions, voxel size.",
        "common_uses": [
            "Get grid dimensions",
            "Query voxel size",
            "Volume analysis"
        ],
        "pitfalls": [
            "Voxel Size: size of each voxel",
            "Bounds: grid bounding box",
            "Class: grid type (fog, SDF, etc.)"
        ],
        "commonly_used_with": [
            ("Volume Cube", "input volume"),
            ("Math", "calculate with dimensions"),
            ("Compare", "check grid properties"),
            ("Grid operations", "resolution matching")
        ],
        "example": "Match resolution: Grid Info → use voxel size for consistent grid operations."
    },
    
    "GeometryNodeVoxelIndex": {
        "display_name": "Voxel Index",
        "category": "Volume",
        "description": "Returns voxel grid coordinates - 3D integer index of voxel.",
        "common_uses": [
            "Voxel addressing",
            "Grid coordinate access",
            "Procedural voxel operations"
        ],
        "pitfalls": [
            "Returns integer XYZ coordinates",
            "Specific to volume context",
            "Use for grid-based calculations"
        ],
        "commonly_used_with": [
            ("Sample Grid Index", "sample at voxel"),
            ("Integer Math", "coordinate math"),
            ("Compare", "select voxels"),
            ("Separate XYZ", "individual coordinates")
        ],
        "example": "Checkerboard volume: (voxel_x + voxel_y + voxel_z) % 2 → alternating pattern in voxels."
    },
    
    # ==========================================================================
    # VOLUME SAMPLE
    # ==========================================================================
    
    "GeometryNodeSampleGrid": {
        "display_name": "Sample Grid",
        "category": "Volume",
        "description": "Reads volume grid value at position - interpolated sampling.",
        "common_uses": [
            "Read volume data",
            "Sample density/SDF values",
            "Volume-driven effects"
        ],
        "pitfalls": [
            "Interpolated: smooth between voxels",
            "Position: sample location",
            "Returns grid value at position"
        ],
        "commonly_used_with": [
            ("Position", "sample at point locations"),
            ("Volume Cube", "source volume"),
            ("Compare", "threshold sampling"),
            ("Set Position", "volume-based displacement")
        ],
        "example": "Volume displacement: Sample Grid (SDF) → use as displacement distance. Density mask: sample density → color/opacity."
    },
    
    "GeometryNodeSampleGridIndex": {
        "display_name": "Sample Grid Index",
        "category": "Volume",
        "description": "Reads volume grid value at voxel index - exact voxel access.",
        "common_uses": [
            "Direct voxel access",
            "Exact grid reading",
            "Integer coordinate sampling"
        ],
        "pitfalls": [
            "No interpolation (exact voxel)",
            "Index: integer XYZ coordinates",
            "Out of bounds = zero/default"
        ],
        "commonly_used_with": [
            ("Voxel Index", "current voxel"),
            ("Integer Math", "coordinate calculation"),
            ("Compare", "voxel conditions"),
            ("Store Named Grid", "modify same location")
        ],
        "example": "Neighbor access: Sample Grid Index at (x+1, y, z) → read adjacent voxel. Exact voxel operations."
    },
    
    "GeometryNodeAdvectGrid": {
        "display_name": "Advect Grid",
        "category": "Volume",
        "description": "Moves grid values along velocity field - flow simulation.",
        "common_uses": [
            "Smoke/fluid movement",
            "Flow simulation",
            "Velocity-based transport"
        ],
        "pitfalls": [
            "Velocity: vector field for flow direction",
            "Time Step: movement amount",
            "Advection = transport by velocity"
        ],
        "commonly_used_with": [
            ("Grid Curl", "curl noise velocity"),
            ("Sample Grid", "velocity source"),
            ("Simulation Zone", "animated advection"),
            ("Volume Cube", "source density")
        ],
        "example": "Smoke flow: density grid + velocity field → Advect Grid → density moves with velocity."
    },
    
    "GeometryNodeGridCurl": {
        "display_name": "Grid Curl",
        "category": "Volume",
        "description": "Calculates curl of vector field - rotational component.",
        "common_uses": [
            "Generate swirling motion",
            "Curl noise velocity",
            "Incompressible flow"
        ],
        "pitfalls": [
            "Curl = rotational tendency",
            "Input: vector grid",
            "Output: curl vector grid"
        ],
        "commonly_used_with": [
            ("Noise Texture", "noise-based curl"),
            ("Advect Grid", "use as velocity"),
            ("Field to Grid", "bake curl field"),
            ("Sample Grid", "read curl values")
        ],
        "example": "Turbulent flow: noise field → Grid Curl → swirling velocity field for advection."
    },
    
    "GeometryNodeGridDivergence": {
        "display_name": "Grid Divergence",
        "category": "Volume",
        "description": "Calculates divergence of vector field - expansion/contraction.",
        "common_uses": [
            "Find sources/sinks",
            "Flow analysis",
            "Incompressibility check"
        ],
        "pitfalls": [
            "Positive = expanding (source)",
            "Negative = contracting (sink)",
            "Zero = incompressible"
        ],
        "commonly_used_with": [
            ("Grid Curl", "related operation"),
            ("Sample Grid", "read divergence"),
            ("Compare", "find sources/sinks"),
            ("Grid Gradient", "other derivatives")
        ],
        "example": "Find sources: Divergence > 0 = fluid expanding outward. Pressure solve: divergence drives correction."
    },
    
    "GeometryNodeGridGradient": {
        "display_name": "Grid Gradient",
        "category": "Volume",
        "description": "Calculates gradient of scalar field - direction of steepest increase.",
        "common_uses": [
            "SDF normal calculation",
            "Flow direction",
            "Height-based direction"
        ],
        "pitfalls": [
            "Gradient points toward higher values",
            "For SDF: gradient = surface normal",
            "Output: vector grid"
        ],
        "commonly_used_with": [
            ("Mesh to SDF Grid", "SDF normals"),
            ("Sample Grid", "read gradient"),
            ("Vector Math (Normalize)", "unit direction"),
            ("Set Normal", "apply as normals")
        ],
        "example": "SDF normals: SDF Grid → Grid Gradient → normalized = surface normal direction."
    },
    
    "GeometryNodeGridLaplacian": {
        "display_name": "Grid Laplacian",
        "category": "Volume",
        "description": "Calculates Laplacian of scalar field - second derivative.",
        "common_uses": [
            "Diffusion simulation",
            "Smoothness measure",
            "Heat equation"
        ],
        "pitfalls": [
            "Laplacian = divergence of gradient",
            "Used for diffusion/heat spread",
            "Positive = local minimum, Negative = local maximum"
        ],
        "commonly_used_with": [
            ("Field to Grid", "scalar input"),
            ("Sample Grid", "read Laplacian"),
            ("Simulation Zone", "diffusion over time"),
            ("Math", "process Laplacian values")
        ],
        "example": "Heat diffusion: Laplacian × diffusion_rate = temperature change. Simulation zone for animation."
    },
    
    # ==========================================================================
    # VOLUME WRITE
    # ==========================================================================
    
    "GeometryNodeStoreNamedGrid": {
        "display_name": "Store Named Grid",
        "category": "Volume",
        "description": "Stores a grid with a name into volume - create/replace grid channels.",
        "common_uses": [
            "Create custom volume channels",
            "Store computed grids",
            "Multi-channel volumes"
        ],
        "pitfalls": [
            "Name: grid identifier",
            "Replaces existing grid with same name",
            "Grid becomes part of volume"
        ],
        "commonly_used_with": [
            ("Get Named Grid", "retrieve stored grid"),
            ("Field to Grid", "create grid to store"),
            ("Volume Cube", "volume to modify"),
            ("Sample Grid", "read back")
        ],
        "example": "Custom channel: computed grid → Store Named Grid 'custom_data' → access later with Get Named Grid."
    },
    
    "GeometryNodeSetGridBackground": {
        "display_name": "Set Grid Background",
        "category": "Volume",
        "description": "Sets default value for empty voxels - background value.",
        "common_uses": [
            "Set default density",
            "SDF background value",
            "Sparse grid defaults"
        ],
        "pitfalls": [
            "Background = value for unstored voxels",
            "SDF typically uses large positive value",
            "Density typically uses 0"
        ],
        "commonly_used_with": [
            ("Mesh to SDF Grid", "set SDF background"),
            ("Volume Cube", "modify background"),
            ("Prune Grid", "affects pruning threshold"),
            ("Grid operations", "ensure consistent background")
        ],
        "example": "SDF convention: Set Grid Background to large value (e.g., 1000) → empty space = far from surface."
    },
    
    "GeometryNodeSetGridTransform": {
        "display_name": "Set Grid Transform",
        "category": "Volume",
        "description": "Sets transformation matrix for volume grid - position, rotation, scale.",
        "common_uses": [
            "Transform volume",
            "Position grid in space",
            "Scale volume"
        ],
        "pitfalls": [
            "Transform: 4×4 transformation matrix",
            "Affects grid-to-world mapping",
            "Changes where voxels appear in space"
        ],
        "commonly_used_with": [
            ("Combine Transform", "create matrix"),
            ("Object Info", "match object transform"),
            ("Volume Cube", "transform volume"),
            ("Grid Info", "read existing transform")
        ],
        "example": "Move volume: Combine Transform (new position) → Set Grid Transform. Volume follows transformation."
    },
    
    # ==========================================================================
    # CURVE WRITE - HANDLE NODES
    # ==========================================================================
    
    "GeometryNodeSetHandlePositions": {
        "display_name": "Set Handle Positions",
        "category": "Curve Write",
        "description": "Sets Bezier handle positions - control point tangents.",
        "common_uses": [
            "Custom handle placement",
            "Curve shape control",
            "Precise tangent control"
        ],
        "pitfalls": [
            "Mode: Left, Right handle",
            "Position: world space coordinates",
            "Only affects Bezier curves"
        ],
        "commonly_used_with": [
            ("Handle Positions", "read existing"),
            ("Vector Math", "calculate positions"),
            ("Position", "offset from point"),
            ("Set Handle Type", "set handle behavior")
        ],
        "example": "Smooth curve: calculate handle positions tangent to curve direction. Sharp corner: handles aligned with adjacent segments."
    },
    
    "GeometryNodeSetHandleType": {
        "display_name": "Set Handle Type",
        "category": "Curve Write",
        "description": "Sets Bezier handle type - Free, Vector, Align, Auto.",
        "common_uses": [
            "Control handle behavior",
            "Sharp vs smooth corners",
            "Curve editing"
        ],
        "pitfalls": [
            "Free: independent handles",
            "Vector: straight to next point",
            "Align: handles stay aligned",
            "Auto: automatic smooth"
        ],
        "commonly_used_with": [
            ("Set Handle Positions", "after setting type"),
            ("Handle Type Selection", "select specific types"),
            ("Bezier Segment", "source curve"),
            ("Set Spline Type", "ensure Bezier")
        ],
        "example": "Sharp corner: Set Handle Type (Vector) at corner points. Smooth: Auto handles. Mixed: different types per point."
    },
    
    # ==========================================================================
    # INSTANCES - BOUNDS (verify/add if missing)
    # ==========================================================================
    
    "GeometryNodeInstanceBounds": {
        "display_name": "Instance Bounds",
        "category": "Instances",
        "description": "Gets bounding box of each instance - min/max corners.",
        "common_uses": [
            "Instance collision detection",
            "Size-based operations",
            "Bounding box analysis"
        ],
        "pitfalls": [
            "Returns Min and Max vectors",
            "Per-instance bounds",
            "In instance local space"
        ],
        "commonly_used_with": [
            ("Instance on Points", "instanced geometry"),
            ("Vector Math (Subtract)", "calculate size"),
            ("Compare", "size filtering"),
            ("Bounding Box", "overall bounds")
        ],
        "example": "Filter by size: Instance Bounds → size = max - min → delete small instances. Collision: check bounds overlap."
    },
    
    # ==========================================================================
    # VALUE INPUT (if not already added)
    # ==========================================================================
    
    "FunctionNodeInputValue": {
        "display_name": "Value",
        "category": "Input",
        "description": "Single float value input - becomes slider in modifier panel.",
        "common_uses": [
            "Numeric parameter",
            "User-adjustable value",
            "Constant float"
        ],
        "pitfalls": [
            "Click to edit value directly",
            "Exposed in modifier panel",
            "Single float output"
        ],
        "commonly_used_with": [
            ("Math", "calculations"),
            ("Map Range", "scale value"),
            ("Compare", "threshold"),
            ("Mix", "blend factor")
        ],
        "example": "Parameter: Value (0.5) → use as blend factor, displacement amount, or any numeric control."
    }
}

# Aliases for nodes that may have different bl_idnames across Blender versions
NODE_ALIASES = {
    # Gizmo nodes - bl_idname uses "Gizmo" before type name
    "GeometryNodeDialGizmo": "GeometryNodeGizmoDial",
    "GeometryNodeLinearGizmo": "GeometryNodeGizmoLinear",
    "GeometryNodeTransformGizmo": "GeometryNodeGizmoTransform",
    # Scene input nodes
    "GeometryNodeInputActiveCamera": "GeometryNodeActiveCamera",
    "GeometryNodeInput3DCursor": "GeometryNodeTool3DCursor",
    # Additional possible aliases
    "GeometryNodeToolSelfObject": "GeometryNodeSelfObject",
    "GeometryNodeInputSelfObject": "GeometryNodeSelfObject",
    "GeometryNodeToolIsViewport": "GeometryNodeIsViewport", 
    "GeometryNodeInputIsViewport": "GeometryNodeIsViewport",
    
    # Mesh UV nodes
    "GeometryNodeUVTangent": "GeometryNodeInputMeshUVTangent",
    
    # Common Input node aliases (Blender often drops "Input" prefix)
    "GeometryNodePosition": "GeometryNodeInputPosition",
    "GeometryNodeNormal": "GeometryNodeInputNormal",
    "GeometryNodeIndex": "GeometryNodeInputIndex",
    "GeometryNodeID": "GeometryNodeInputID",
    "GeometryNodeNamedAttribute": "GeometryNodeInputNamedAttribute",
    "GeometryNodeMaterialIndex": "GeometryNodeInputMaterialIndex",
    "GeometryNodeSelection": "GeometryNodeInputSelection",
    "GeometryNodeRadius": "GeometryNodeInputRadius",
    "GeometryNodeSceneTime": "GeometryNodeInputSceneTime",
    "GeometryNodeCollection": "GeometryNodeInputCollection",
    "GeometryNodeImage": "GeometryNodeInputImage",
    "GeometryNodeMaterial": "GeometryNodeInputMaterial",
    "GeometryNodeTangent": "GeometryNodeInputTangent",
    "GeometryNodeShadeSmooth": "GeometryNodeInputShadeSmooth",
    "GeometryNodeEdgeSmooth": "GeometryNodeInputEdgeSmooth",
    
    # Mesh read nodes (Blender may drop "InputMesh" or just "Input")
    "GeometryNodeEdgeAngle": "GeometryNodeInputMeshEdgeAngle",
    "GeometryNodeMeshEdgeAngle": "GeometryNodeInputMeshEdgeAngle",
    "GeometryNodeEdgeNeighbors": "GeometryNodeInputMeshEdgeNeighbors",
    "GeometryNodeMeshEdgeNeighbors": "GeometryNodeInputMeshEdgeNeighbors",
    "GeometryNodeEdgeVertices": "GeometryNodeInputMeshEdgeVertices",
    "GeometryNodeMeshEdgeVertices": "GeometryNodeInputMeshEdgeVertices",
    "GeometryNodeFaceArea": "GeometryNodeInputMeshFaceArea",
    "GeometryNodeMeshFaceArea": "GeometryNodeInputMeshFaceArea",
    "GeometryNodeFaceNeighbors": "GeometryNodeInputMeshFaceNeighbors",
    "GeometryNodeMeshFaceNeighbors": "GeometryNodeInputMeshFaceNeighbors",
    "GeometryNodeFaceIsPlanar": "GeometryNodeInputMeshFaceIsPlanar",
    "GeometryNodeMeshFaceIsPlanar": "GeometryNodeInputMeshFaceIsPlanar",
    "GeometryNodeMeshIsland": "GeometryNodeInputMeshIsland",
    "GeometryNodeIsland": "GeometryNodeInputMeshIsland",
    "GeometryNodeVertexNeighbors": "GeometryNodeInputMeshVertexNeighbors",
    "GeometryNodeMeshVertexNeighbors": "GeometryNodeInputMeshVertexNeighbors",
    "GeometryNodeShortestEdgePaths": "GeometryNodeInputShortestEdgePaths",
    "GeometryNodeEdgesToFaceGroups": "GeometryNodeInputMeshEdgesToFaceGroups",
    "GeometryNodeMeshEdgesToFaceGroups": "GeometryNodeInputMeshEdgesToFaceGroups",
    "GeometryNodeFaceGroupBoundaries": "GeometryNodeInputMeshFaceGroupBoundaries",
    "GeometryNodeMeshFaceGroupBoundaries": "GeometryNodeInputMeshFaceGroupBoundaries",
    "GeometryNodeMeshUVTangent": "GeometryNodeInputMeshUVTangent",
    
    # Curve read nodes
    "GeometryNodeCurveTangent": "GeometryNodeInputCurveTangent",
    "GeometryNodeCurveTilt": "GeometryNodeInputCurveTilt",
    "GeometryNodeSplineResolution": "GeometryNodeInputSplineResolution",
    "GeometryNodeSplineCyclic": "GeometryNodeInputSplineCyclic",
    "GeometryNodeCurveHandlePositions": "GeometryNodeInputCurveHandlePositions",
    
    # Instance nodes
    "GeometryNodeInstanceRotation": "GeometryNodeInputInstanceRotation",
    "GeometryNodeInstanceScale": "GeometryNodeInputInstanceScale",
    
    # Function/Input nodes
    "FunctionNodeInt": "FunctionNodeInputInt",
    "FunctionNodeVector": "FunctionNodeInputVector",
    "FunctionNodeBool": "FunctionNodeInputBool",
    "FunctionNodeFloat": "FunctionNodeInputFloat",
    "FunctionNodeColor": "FunctionNodeInputColor",
    "FunctionNodeObject": "FunctionNodeInputObject",
    "FunctionNodeRotation": "FunctionNodeInputRotation",
    "FunctionNodeString": "FunctionNodeInputString",
    "FunctionNodeValue": "FunctionNodeInputValue",
    
    # Mouse/Tool nodes
    "GeometryNodeMousePosition": "GeometryNodeInputMousePosition",
    "GeometryNodeNamedLayerSelection": "GeometryNodeInputNamedLayerSelection",
}


def get_node_info(node_type):
    """Get info for a node type, returns None if not found."""
    # First try direct lookup
    if node_type in NODE_DATABASE:
        return NODE_DATABASE[node_type]
    # Then try alias lookup
    if node_type in NODE_ALIASES:
        return NODE_DATABASE.get(NODE_ALIASES[node_type], None)
    # Try reverse alias (in case the database has the alias as key)
    for alias, target in NODE_ALIASES.items():
        if target == node_type and alias in NODE_DATABASE:
            return NODE_DATABASE[alias]
    return None


def get_all_node_types():
    """Get list of all supported node types."""
    return list(NODE_DATABASE.keys())


def get_nodes_by_category(category):
    """Get all nodes in a specific category."""
    return {k: v for k, v in NODE_DATABASE.items() if v.get("category") == category}


def get_all_categories():
    """Get list of all unique categories."""
    return list(set(v.get("category", "Other") for v in NODE_DATABASE.values()))
