# Geo Nodes Guide

A Blender addon that shows instant documentation when you hover over Geometry Nodes.

![Blender](https://img.shields.io/badge/Blender-5.0+-orange)
![License](https://img.shields.io/github/license/addonyte/geo-nodes-guide)
![Nodes](https://img.shields.io/badge/Nodes%20Documented-332-green)
![Contributors](https://img.shields.io/github/contributors/addonyte/geo-nodes-guide)
![Open Source](https://img.shields.io/badge/Open%20Source-GPL--3.0--or--later-green)


## What It Does

Hover over any Geometry Node and get a tooltip with:
- **Description** - What the node does
- **Common Uses** - Practical applications
- **Pitfalls** - Mistakes to avoid (radians vs degrees, etc.)
- **Works Well With** - Nodes that pair nicely
- **Example** - Real workflow snippet

No more tab-switching to look up documentation.

## Installation

### Option 1: Download from Releases
1. Download the latest `.zip` from [Releases](../../releases)
2. In Blender: `Edit → Preferences → Add-ons → Install`
3. Select the downloaded zip
4. Enable "Geo Nodes Guide"

### Option 2: Clone the Repository
```bash
git clone https://github.com/addonyte/geo-nodes-guide.git
```
Copy the `geo_nodes_guide` folder to your Blender addons directory.

## Usage

1. Open any Geometry Nodes editor
2. Find the **Geo Nodes Guide** tab in the sidebar (press `N` if hidden)
3. Click **Hover Help Active**
4. Hover over any node to see documentation
5. Press `ESC` to dismiss tooltip

## Requirements

- Blender 5.0 or newer

## Contributing

Contributions are welcome! Here's how you can help:

### 🌍 Translations
We'd love help translating the node documentation to other languages. If you're interested:
1. Open an issue saying which language you'd like to add
2. Fork the repo
3. Add translations to the documentation data files (see database.py for current structure)
4. Submit a pull request

### 📝 Improve Documentation
Found a node description that could be clearer? Have a better example? PRs welcome!

### 🐛 Bug Reports
Open an issue with:
- Blender version
- Steps to reproduce
- Error message (if any)

### 💡 Feature Requests
Open an issue describing what you'd like to see.

## Project Structure

```
geo_nodes_guide/
├── __init__.py              # Main addon code
├── database.py              # Node documentation (332 nodes)
├── blender_manifest.toml    # Blender extension manifest
├── LICENSE                  # GPL-3.0-or-later
└── README.md                # This file
```

## License

GPL-3.0-or-later - see [LICENSE](LICENSE) for details.

You’re free to use, modify, and distribute this addon under the terms of the GPL-3.0-or-later license. Any distributed modifications must remain open source under the same license.

## Support

- **Issues**: [GitHub Issues](../../issues)
- **Gumroad**: [https://addonyte.gumroad.com/l/geometrynodesguide]

## Credits

Created by **Addonyte**

Thanks to all contributors!
