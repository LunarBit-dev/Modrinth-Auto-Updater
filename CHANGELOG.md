# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-07-21

### Added
- Initial release of Modrinth Modpack Updater
- Intelligent mod update system with Modrinth API v2 integration
- Smart modloader compatibility (Fabric, Quilt, Forge, NeoForge)
- Quilt backward compatibility with Fabric mods
- Client/server .mrpack generation with proper filtering
- Server compatibility checking via Modrinth API
- Comprehensive changelog generation in Markdown format
- Color-coded terminal output for better UX
- Safe backup and replacement of mod files
- Sub-version Minecraft compatibility (1.21.x matching)
- Support for overrides folder inclusion
- Automatic cleanup of temporary files

### Features
- `--client` flag for generating client-optimized .mrpack files
- `--server` flag for generating server-optimized .mrpack files with compatibility filtering
- `--overrides-folder` option for custom config directories
- Proper .mrpack format compliance with Modrinth specification
- Modular code design for easy maintenance and extension

### Compatibility
- Python 3.8+ support
- Cross-platform compatibility (Windows, macOS, Linux)
- Support for both .mrpack files and modpack folders
- Works with modrinth.index.json and index.json formats
