# Example Modpacks

This directory contains example modpack configurations for testing and demonstration purposes.

## Files

### `example-fabric-modpack.json`
A sample Fabric modpack configuration with popular performance and utility mods.

### `example-quilt-modpack.json`
A sample Quilt modpack that demonstrates Quilt's backward compatibility with Fabric mods.

### `example-forge-modpack.json`
A sample Forge modpack with magic and technology mods.

## Usage

These examples can be used to test the modpack updater:

```bash
# Test with the Fabric example
python3 ../update_modpack.py --modpack-dir ./fabric-example --client --server

# Test with the Quilt example
python3 ../update_modpack.py --modpack-dir ./quilt-example --client
```

## Creating Your Own

To create your own modpack configuration:

1. Create a folder with your modpack name
2. Add a `modrinth.index.json` file following the Modrinth modpack format
3. Optionally add an `overrides/` folder with configs and resource packs
4. Run the updater script on your folder
