# 🚀 LunarBit Modpack Updater

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Modrinth](https://img.shields.io/badge/Modrinth-API%20v2-00AF5C.svg)](https://docs.modrinth.com/)
[![GUI](https://img.shields.io/badge/GUI-Available-brightgreen.svg)](#-gui-mode)

A powerful tool that automatically updates Minecraft modpacks using the Modrinth API, with intelligent modloader compatibility and client/server .mrpack generation. Now featuring a beautiful GUI with LunarBit theming!

## ✨ Features

### 🎨 **Beautiful GUI Interface**
- Modern dark theme with LunarBit styling
- Intuitive configuration panel with all options
- Real-time output monitoring with colored logs
- One-click updates with progress tracking
- Cross-platform compatibility (Windows, macOS, Linux)

### 🔄 **Intelligent Mod Updates**
- Automatically checks for mod updates using Modrinth API v2
- Respects Minecraft version compatibility (including sub-version matching like 1.21.x)
- Smart modloader filtering with Quilt ↔ Fabric backward compatibility
- Supports Fabric, Quilt, Forge, and NeoForge modloaders
- Safe backup and replacement of existing mod files

### 📦 **Client/Server .mrpack Generation**
- Generate separate client and server modpack files
- Automatic server compatibility filtering using Modrinth API
- Proper environment tags (`client`/`server` required/unsupported)
- Support for overrides folder (configs, resource packs, etc.)
- Follows official Modrinth modpack specification

### 📊 **Comprehensive Reporting**
- Color-coded terminal output for easy status tracking
- Detailed changelog generation in Markdown format
- Update summary with counts of updated, up-to-date, and failed mods
- Export all mods to local `mods/` directory

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Internet connection for Modrinth API access

### Installation

1. Clone the repository:
```bash
git clone https://github.com/LunarBit-dev/Modrinth-Auto-Updater.git
cd Modrinth-Auto-Updater
```

2. **Quick Setup** (recommended):
```bash
# Linux/macOS
chmod +x setup.sh && ./setup.sh

# Windows
setup.bat
```

**Or manually:**
```bash
pip install -r requirements.txt
```

## 🎨 GUI Mode

Launch the beautiful GUI interface with enhanced LunarBit theming:

### Quick Launch
```bash
# Universal launcher (automatically chooses best mode)
python3 launcher.py

# Explicit GUI launch
python3 launcher.py --gui

# Platform-specific launchers
./run_gui.sh        # Linux/macOS
run_gui.bat         # Windows
python3 run_gui.py  # Direct Python
```

### Enhanced Features
- 🎨 **Stunning Design** - Modern dark theme with LunarBit colors and enhanced typography
- � **Smart File Selection** - Choose between folder or .mrpack file with visual dialog
- � **Real-time Status** - Live path validation and detailed progress tracking
- ⚙️ **Rich Configuration** - Enhanced options panel with descriptions and validation
- 🚀 **One-Click Updates** - Streamlined workflow with intelligent status updates
- 📋 **Beautiful Output** - Enhanced terminal output with better fonts and spacing

![Enhanced GUI](docs/gui-screenshot.png)

## 💻 Command Line Usage

### Universal Launcher
```bash
# Auto-detect best mode (GUI if available, CLI otherwise)
python3 launcher.py

# Force CLI mode with arguments
python3 launcher.py --cli --modpack-dir path/to/modpack --client

# Auto-detect CLI mode (when CLI arguments are provided)
python3 launcher.py --modpack-dir path/to/modpack --server
```

### Direct CLI Usage

### Basic Usage

```bash
# Update mods and export to local mods/ folder
python3 update_modpack.py --modpack-dir path/to/modpack

# Generate client .mrpack file
python3 update_modpack.py --modpack-dir path/to/modpack --client

# Generate server .mrpack file (with server compatibility filtering)
python3 update_modpack.py --modpack-dir path/to/modpack --server

# Generate both client and server .mrpack files
python3 update_modpack.py --modpack-dir path/to/modpack --client --server
```

## 📖 Detailed Usage

### GUI Examples

#### Quick Update with GUI
1. Launch GUI: `./run_gui.sh` (Linux/macOS) or `run_gui.bat` (Windows)
2. Click "Browse" and select your modpack folder
3. Enable "Generate client .mrpack" if desired
4. Click "🚀 Update Modpack"

#### Server Pack Generation
1. Open the GUI and select your modpack
2. Check "📱 Generate client .mrpack" and "🖥️ Generate server .mrpack"
3. Set custom overrides folder if needed
4. Start the update and monitor progress in real-time

### Command Line Options

```
usage: update_modpack.py [-h] --modpack-dir MODPACK_DIR [--client] [--server] 
                        [--overrides-folder OVERRIDES_FOLDER]

options:
  -h, --help                    Show this help message and exit
  --modpack-dir MODPACK_DIR     Path to modpack directory or .mrpack file
  --client                      Generate client .mrpack file
  --server                      Generate server .mrpack file  
  --overrides-folder FOLDER     Name of overrides folder (default: overrides)
```

### Command Line Examples

#### Example 1: Basic Update
usage: update_modpack.py [-h] --modpack-dir MODPACK_DIR [--client] [--server]
                         [--overrides-folder OVERRIDES_FOLDER]

options:
  --modpack-dir MODPACK_DIR     Path to modpack folder or .mrpack file
  --client                      Generate client .mrpack file
  --server                      Generate server .mrpack file  
  --overrides-folder FOLDER     Custom overrides folder (default: overrides)
```

### Input Formats

The script accepts:
- **Modpack folders** containing `modrinth.index.json` or `index.json`
- **`.mrpack` files** (automatically extracted)

### Modloader Compatibility

| Modpack Type | Accepts Mods For |
|--------------|------------------|
| Fabric | Fabric only |
| Quilt | Quilt + Fabric (backward compatibility) |
| Forge | Forge only |
| NeoForge | NeoForge only |

### Server Filtering

When generating server .mrpack files, the script:
1. Queries each mod's `server_side` compatibility via Modrinth API
2. Includes only mods marked as `"required"` or `"optional"` for servers
3. Excludes client-only mods (e.g., Sodium, OptiFine)
4. Reports skipped mods in the output

## 🔧 Examples

### Example 1: Basic Update
```bash
python3 update_modpack.py --modpack-dir "./MyModpack/"
```
**Result**: Updates all mods, exports to `mods/`, generates changelog

### Example 2: Client Distribution
```bash
python3 update_modpack.py --modpack-dir "./MyModpack.mrpack" --client
```
**Result**: Creates `MyModpack.mrpack` optimized for client installation

### Example 3: Server Deployment
```bash
python3 update_modpack.py --modpack-dir "./MyModpack/" --server
```
**Result**: Creates `MyModpack-server.mrpack` with only server-compatible mods

### Example 4: Full Distribution
```bash
python3 update_modpack.py --modpack-dir "./MyModpack/" --client --server --overrides-folder config
```
**Result**: Creates both client and server .mrpack files with custom config folder

## 📄 Output Files

### Generated Files
- `mods/` - Directory containing all updated mod files
- `{modpack-name}_changelog.md` - Detailed update changelog
- `{modpack-name}.mrpack` - Client modpack (if `--client`)
- `{modpack-name}-server.mrpack` - Server modpack (if `--server`)

### Changelog Format
```markdown
# Modpack Update Changelog - 2025-07-21

## 🔄 Updated Mods (2)
- **Sodium**: `mc1.21.4-0.6.0` → `mc1.21.6-0.6.13`
- **Fabric API**: `0.104.0+1.21` → `0.129.0+1.21.8`

## ✅ Up-to-date Mods (15)
- JEI: `19.22.4.118`
- REI: `16.0.744`
...
```

## 🛠️ Development

### Project Structure
```
modrinth-modpack-updater/
├── update_modpack.py          # Main script
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore rules
└── examples/                # Example modpacks and configs
```

### Code Features
- **Type hints** for better code maintainability
- **Error handling** with detailed logging
- **Modular design** with separate functions for each feature
- **API rate limiting** respect for Modrinth API
- **Cross-platform** compatibility (Windows, macOS, Linux)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📋 Roadmap

- [ ] Support for CurseForge modpacks
- [ ] GUI interface
- [ ] Batch processing for multiple modpacks
- [ ] Mod dependency resolution
- [ ] Custom update channels (alpha, beta, release)
- [ ] Integration with mod hosting platforms

## 🐛 Known Issues

- Some mods may not have proper server compatibility tags on Modrinth
- Very large modpacks (500+ mods) may take longer to process
- Rate limiting may cause slower updates for modpacks with many mods

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/LunarBit-dev/Modrinth-Auto-Updater/issues)
- **Discussions**: [GitHub Discussions](https://github.com/LunarBit-dev/Modrinth-Auto-Updater/discussions)
- **Discord**: [LunarBit Discord](https://discord.gg/lunarbit)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Modrinth](https://modrinth.com/) for providing an excellent API
- [Minecraft](https://minecraft.net/) community for the amazing modding ecosystem
- All contributors and users of this tool

## ⭐ Star History

If this tool helped you, please consider giving it a star on GitHub!

---

**Made with ❤️ by [LunarBit](https://github.com/LunarBit-dev) for the Minecraft modding community**
