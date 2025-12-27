# Geo Nodes Guide

A Blender addon that shows instant documentation when you hover over Geometry Nodes.

![Blender](https://img.shields.io/badge/Blender-5.0+-orange)
![License](https://img.shields.io/badge/License-MIT-blue)
![Nodes](https://img.shields.io/badge/Nodes%20Documented-332-green)

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

- Blender 5.0

## Contributing

Contributions are welcome! Here's how you can help:

### 🌍 Translations
We'd love help translating the node documentation to other languages. If you're interested:
1. Open an issue saying which language you'd like to add
2. Fork the repo
3. Add translations to `database.py`
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
├── LICENSE                  # MIT License
└── README.md                # This file
```

## License

MIT License - see [LICENSE](LICENSE) for details.

You're free to use, modify, and distribute this addon. Just keep the copyright notice.

## Support

- **Issues**: [GitHub Issues](../../issues)
- **Gumroad**: https://addonyte.gumroad.com/l/geometrynodesguide

## Credits

Created by **Addonyte**

Thanks to all contributors!
