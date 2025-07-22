#!/usr/bin/env python3
"""
Modrinth Modpack Updater

- Reads a Modrinth modpack (folder or .mrpack)
- Checks for mod updates via Modrinth API
- Downloads and replaces updated mods, backing up old versions
- Outputs a Markdown changelog and color-coded terminal summary

Author: Lunarbit
"""
import os
import sys
import json
import argparse
import requests
import shutil
import zipfile
import tempfile
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Tuple
from urllib.request import urlopen

# Terminal color codes
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

MODRINTH_API = "https://api.modrinth.com/v2"

# -------------------- Argument Parsing --------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Update a Modrinth modpack's mods to latest compatible versions.")
    parser.add_argument('--modpack-dir', required=True, help='Path to modpack folder or .mrpack file')
    parser.add_argument('--client', action='store_true', help='Generate client .mrpack file')
    parser.add_argument('--server', action='store_true', help='Generate server .mrpack file')
    parser.add_argument('--overrides-folder', default='overrides', help='Folder containing config/resource files to include (default: overrides)')
    return parser.parse_args()

# -------------------- Modpack Loading --------------------
def extract_mrpack(mrpack_path: str) -> str:
    temp_dir = tempfile.mkdtemp(prefix="modrinth_modpack_")
    with zipfile.ZipFile(mrpack_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    return temp_dir

def find_index_json(modpack_dir: str) -> str:
    # Try both possible filenames for Modrinth modpack index
    for filename in ['modrinth.index.json', 'index.json']:
        index_path = os.path.join(modpack_dir, filename)
        if os.path.exists(index_path):
            return index_path
    
    # If not found in root, search recursively
    for filename in ['modrinth.index.json', 'index.json']:
        for root, _, files in os.walk(modpack_dir):
            if filename in files:
                return os.path.join(root, filename)
    
    raise FileNotFoundError(f'modrinth.index.json or index.json not found in modpack directory: {modpack_dir}')

def extract_project_id_from_url(download_url: str) -> str | None:
    """Extract project ID from Modrinth download URL"""
    # URL format: https://cdn.modrinth.com/data/{project_id}/versions/{version_id}/{filename}
    try:
        parts = download_url.split('/')
        if 'cdn.modrinth.com' in download_url and 'data' in parts:
            data_index = parts.index('data')
            if data_index + 1 < len(parts):
                return parts[data_index + 1]
    except Exception:
        pass
    return None

def get_version_info_by_hash(sha1_hash: str) -> Dict[str, Any] | None:
    """Get version info from Modrinth using file hash"""
    url = f"{MODRINTH_API}/version_file/{sha1_hash}"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return None
def get_project_info(slug: str) -> Dict[str, Any] | None:
    url = f"{MODRINTH_API}/project/{slug}"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    return None

def get_latest_version(slug: str, mc_version: str, loaders: List[str], current_version: str, current_version_info: Dict[str, Any] | None = None) -> Tuple[Dict[str, Any] | None, bool]:
    url = f"{MODRINTH_API}/project/{slug}/version"
    params = {
        "game_versions": mc_version,
        "loaders": loaders
    }
    try:
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            return None, False
        versions = resp.json()
        if not versions:
            return None, False
            
        # Get compatible loaders for this modpack
        compatible_loaders = get_compatible_loaders(loaders)
        
        # Sort by date_published descending (newest first)
        versions.sort(key=lambda v: v.get('date_published', ''), reverse=True)
        
        # Filter versions to only compatible ones
        compatible_versions = []
        for v in versions:
            if is_version_compatible(v, mc_version, compatible_loaders):
                compatible_versions.append(v)
        
        if not compatible_versions:
            return None, False
            
        # For Quilt modpacks, prefer Quilt versions over Fabric when available
        is_quilt_modpack = any('quilt' in loader.lower() for loader in loaders)
        if is_quilt_modpack:
            quilt_versions = [v for v in compatible_versions if 'quilt' in [l.lower() for l in v.get('loaders', [])]]
            fabric_versions = [v for v in compatible_versions if 'fabric' in [l.lower() for l in v.get('loaders', [])] and 'quilt' not in [l.lower() for l in v.get('loaders', [])]]
            
            # Check if current mod is Fabric and we have a Quilt alternative
            current_is_fabric_only = (current_version_info and 
                                    'fabric' in [l.lower() for l in current_version_info.get('loaders', [])] and 
                                    'quilt' not in [l.lower() for l in current_version_info.get('loaders', [])])
            
            if current_is_fabric_only and quilt_versions:
                # Look for a Quilt version of the same version number
                quilt_same_version = next((v for v in quilt_versions if v['version_number'] == current_version), None)
                if quilt_same_version:
                    print(f"    Found Quilt version of same release: {quilt_same_version['version_number']}")
                    return quilt_same_version, True
            
            # Use Quilt versions if they're as recent as the latest overall version
            if quilt_versions and quilt_versions[0]['date_published'] >= compatible_versions[0]['date_published']:
                versions_to_check = quilt_versions
            else:
                versions_to_check = compatible_versions
        else:
            versions_to_check = compatible_versions
            
        # If current_version is empty, return the latest compatible version
        if not current_version:
            return versions_to_check[0], True
            
        # Find the current version in the compatible list to get its position
        current_version_index = None
        for i, v in enumerate(versions_to_check):
            if v['version_number'] == current_version:
                current_version_index = i
                break
                
        # If current version is found and there are versions before it (newer), return the first one
        if current_version_index is not None and current_version_index > 0:
            newer_version = versions_to_check[0]
            return newer_version, True
        elif current_version_index == 0:
            # Current version is already the latest compatible
            return versions_to_check[0], False
        else:
            # Current version not found in compatible versions, return latest
            return versions_to_check[0] if versions_to_check else None, bool(versions_to_check)
    except Exception:
        return None, False

def download_file(url: str, dest: str) -> bool:
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(dest, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except Exception:
        return False

# -------------------- Mod Updating Logic --------------------
def backup_and_replace_mod(mods_dir: str, old_filename: str, new_jar_path: str):
    old_path = os.path.join(mods_dir, old_filename)
    backup_dir = os.path.join(mods_dir, 'old_mods')
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"{os.path.splitext(old_filename)[0]}_{timestamp}.jar"
    backup_path = os.path.join(backup_dir, backup_name)
    shutil.move(old_path, backup_path)
    shutil.move(new_jar_path, os.path.join(mods_dir, os.path.basename(new_jar_path)))

# -------------------- Changelog Output --------------------
def write_changelog(changelog_path: str, updated: List[Dict], uptodate: List[Dict], missing: List[Dict], errors: List[str]):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(f"# Modpack Update Changelog\n\n")
        f.write(f"**Update Time:** {now}\n\n")
        if updated:
            f.write("## ✅ Updated Mods\n")
            for mod in updated:
                f.write(f"- **{mod['name']}** ({mod['slug']}) {mod['old_version']} → {mod['new_version']}\n")
            f.write("\n")
        if uptodate:
            f.write("## 🟡 Already Up-to-date\n")
            for mod in uptodate:
                f.write(f"- **{mod['name']}** ({mod['slug']}) {mod['version']}\n")
            f.write("\n")
        if missing:
            f.write("## ❌ Missing/Unavailable Mods\n")
            for mod in missing:
                f.write(f"- **{mod['slug']}** (not found on Modrinth)\n")
            f.write("\n")
        if errors:
            f.write("## ⚠️ Errors\n")
            for err in errors:
                f.write(f"- {err}\n")
            f.write("\n")

def get_compatible_loaders(modpack_loaders: List[str]) -> set:
    """
    Get compatible mod loaders based on the modpack's loader.
    Quilt is backward compatible with Fabric.
    Other loaders are strict.
    """
    compatible = set()
    
    for loader in modpack_loaders:
        if 'quilt' in loader.lower():
            # Quilt can use both Quilt and Fabric mods
            compatible.update(['quilt', 'fabric'])
        elif 'fabric' in loader.lower():
            # Fabric only uses Fabric mods
            compatible.add('fabric')
        elif 'forge' in loader.lower():
            # Forge only uses Forge mods
            compatible.add('forge')
        elif 'neoforge' in loader.lower():
            # NeoForge only uses NeoForge mods
            compatible.add('neoforge')
        else:
            # For any other loader, use exact match
            compatible.add(loader.lower())
    
    return compatible

def is_version_compatible(mod_version: Dict[str, Any], target_mc_version: str, compatible_loaders: set) -> bool:
    """
    Check if a mod version is compatible with the target Minecraft version and modloaders.
    """
    # Check Minecraft version compatibility
    version_mc_versions = mod_version.get('game_versions', [])
    is_mc_compatible = any(
        is_minecraft_version_compatible(target_mc_version, v_mc_version) 
        for v_mc_version in version_mc_versions
    )
    
    if not is_mc_compatible:
        return False
    
    # Check modloader compatibility
    version_loaders = set(loader.lower() for loader in mod_version.get('loaders', []))
    has_compatible_loader = bool(version_loaders.intersection(compatible_loaders))
    
    return has_compatible_loader
def is_minecraft_version_compatible(target_version: str, available_version: str) -> bool:
    """
    Check if a Minecraft version is compatible with the target version.
    For example, 1.21.5 mods should work in 1.21.7 modpacks (same major.minor version).
    """
    try:
        # Parse versions like "1.21.7" -> [1, 21, 7]
        target_parts = [int(x) for x in target_version.split('.')]
        available_parts = [int(x) for x in available_version.split('.')]
        
        # Must have at least major.minor version
        if len(target_parts) < 2 or len(available_parts) < 2:
            return target_version == available_version
        
        # Same major.minor version is considered compatible
        # e.g., 1.21.5 is compatible with 1.21.7
        if target_parts[0] == available_parts[0] and target_parts[1] == available_parts[1]:
            return True
            
        # Exact match is always compatible
        return target_version == available_version
        
    except (ValueError, IndexError):
        # If we can't parse versions, fall back to exact match
        return target_version == available_version

# -------------------- Modrinth API Helpers --------------------

def check_server_compatibility(project_slug: str) -> str:
    """
    Check if a mod supports server-side usage.
    Returns: "required", "optional", "unsupported"
    """
    try:
        url = f"{MODRINTH_API}/project/{project_slug}"
        resp = requests.get(url)
        if resp.status_code == 200:
            project_data = resp.json()
            return project_data.get('server_side', 'unsupported')
    except Exception as e:
        print(f"{Colors.YELLOW}⚠️  Warning: Could not check server compatibility for {project_slug}: {e}{Colors.RESET}")
    return 'unsupported'

def generate_mrpack(modpack_name: str, version_id: str, mc_version: str, modloader: str, mod_list: List[Dict], 
                   mode: str = "client", overrides_folder: str = "overrides", output_file: str | None = None):
    """
    Generate a .mrpack file using mod metadata and overrides.
    
    Args:
        mode: "client" or "server" - determines env settings and mod filtering
        mod_list: list of dicts, each with:
          - filename (str): mod filename like 'sodium-fabric.jar'
          - url (str): direct Modrinth download URL
          - sha1 (str): file hash (optional, will be calculated if not given)
          - project_slug (str): Modrinth project slug for server compatibility check
          - env (dict): original env settings (optional)
    """
    if output_file is None:
        suffix = "-server" if mode == "server" else ""
        output_file = f"{modpack_name.replace(' ', '_')}{suffix}.mrpack"
    
    print(f"{Colors.GREEN}📦 Generating {mode} .mrpack file: {output_file}{Colors.RESET}")
    
    index = {
        "formatVersion": 1,
        "game": "minecraft",
        "versionId": version_id,
        "name": f"{modpack_name}{' (Server)' if mode == 'server' else ''}",
        "summary": f"{modpack_name} {mode} modpack auto-generated by mod updater",
        "dependencies": {
            "minecraft": mc_version,
            f"{modloader}-loader": "latest"
        },
        "files": []
    }

    # Filter and process mods based on mode
    included_mods = 0
    skipped_mods = 0
    
    for mod in mod_list:
        # For server mode, check server compatibility
        if mode == "server":
            project_slug = mod.get('project_slug')
            if project_slug:
                server_side = check_server_compatibility(project_slug)
                if server_side == 'unsupported':
                    print(f"{Colors.YELLOW}⏭️  Skipping {mod['filename']} (server unsupported){Colors.RESET}")
                    skipped_mods += 1
                    continue
        
        path = f"mods/{mod['filename']}"
        local_file = os.path.join("mods", mod["filename"])
        sha1 = mod.get("sha1")

        # Calculate hash if not provided and file exists
        if not sha1 and os.path.exists(local_file):
            with open(local_file, "rb") as f:
                sha1 = hashlib.sha1(f.read()).hexdigest()
        elif not sha1:
            print(f"{Colors.YELLOW}⚠️  Warning: No hash available for {mod['filename']}{Colors.RESET}")
            continue

        # Set environment based on mode
        if mode == "client":
            env = {"client": "required", "server": "unsupported"}
        else:  # server mode
            env = {"client": "unsupported", "server": "required"}

        index["files"].append({
            "path": path,
            "downloads": [mod["url"]],
            "hashes": {"sha1": sha1},
            "env": env
        })
        included_mods += 1

    # Create temporary directory for .mrpack contents
    temp_mrpack_dir = "temp_mrpack"
    os.makedirs(temp_mrpack_dir, exist_ok=True)
    
    try:
        # Write modrinth.index.json
        with open(os.path.join(temp_mrpack_dir, "modrinth.index.json"), "w") as f:
            json.dump(index, f, indent=2)

        # Copy overrides folder (if it exists)
        if os.path.exists(overrides_folder):
            shutil.copytree(overrides_folder, os.path.join(temp_mrpack_dir, "overrides"), dirs_exist_ok=True)
            print(f"{Colors.GREEN}📁 Copied overrides folder{Colors.RESET}")

        # Copy optional files if they exist
        optional_files = ["icon.png", "README.md"]
        for optional_file in optional_files:
            if os.path.exists(optional_file):
                shutil.copy2(optional_file, temp_mrpack_dir)
                print(f"{Colors.GREEN}📄 Added {optional_file}{Colors.RESET}")

        # Create .mrpack zip
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(temp_mrpack_dir):
                for file in files:
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, temp_mrpack_dir)
                    z.write(abs_path, rel_path)

        print(f"{Colors.GREEN}✅ {mode.capitalize()} .mrpack created: {output_file}{Colors.RESET}")
        print(f"{Colors.GREEN}📊 Contains {included_mods} mods{Colors.RESET}")
        if skipped_mods > 0:
            print(f"{Colors.YELLOW}⏭️  Skipped {skipped_mods} server-incompatible mods{Colors.RESET}")
        
    finally:
        # Cleanup temp directory
        if os.path.exists(temp_mrpack_dir):
            shutil.rmtree(temp_mrpack_dir)

# -------------------- Main Logic --------------------
def main():
    args = parse_args()
    modpack_path = os.path.expanduser(args.modpack_dir)  # Expand ~ to full path
    temp_dir = None
    
    if modpack_path.endswith('.mrpack'):
        print(f"Extracting .mrpack file: {modpack_path}")
        temp_dir = extract_mrpack(modpack_path)
        modpack_dir = temp_dir
        print(f"Extracted to: {modpack_dir}")
        
        # Debug: List contents of extracted directory
        print("Contents of extracted directory:")
        for item in os.listdir(modpack_dir):
            item_path = os.path.join(modpack_dir, item)
            if os.path.isdir(item_path):
                print(f"  📁 {item}/")
            else:
                print(f"  📄 {item}")
    else:
        modpack_dir = modpack_path
    
    try:
        index_path = find_index_json(modpack_dir)
        print(f"Found index.json at: {index_path}")
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
    except Exception as e:
        print(f"{Colors.RED}Error loading index.json: {e}{Colors.RESET}")
        if temp_dir:
            shutil.rmtree(temp_dir)
        sys.exit(1)

    mc_version = index.get('dependencies', {}).get('minecraft')
    loaders = [k for k in index.get('dependencies', {}) if k != 'minecraft']
    mods = index.get('files', [])
    modpack_name = index.get('name', 'modpack').replace(' ', '_').replace('[', '').replace(']', '')
    
    # Handle mods directory - create in the current working directory
    mods_dir = os.path.join(os.getcwd(), 'mods')
    if not os.path.isdir(mods_dir):
        print(f"Creating mods/ directory at: {mods_dir}")
        os.makedirs(mods_dir, exist_ok=True)

    print(f"Minecraft version: {mc_version}")
    print(f"Mod loaders: {', '.join(loaders)}")
    print(f"Found {len(mods)} mods to check")
    print(f"Mods will be exported to: {mods_dir}")
    print("=" * 50)

    updated, uptodate, missing, errors = [], [], [], []
    mod_list_for_mrpack = []  # Collect mod data for .mrpack generation

    for mod in mods:
        filename = mod.get('path', '').split('/')[-1] if mod.get('path') else ''
        downloads = mod.get('downloads', [])
        sha1_hash = mod.get('hashes', {}).get('sha1')
        
        if not downloads and not sha1_hash:
            errors.append(f"No download URL or hash for mod: {filename}")
            continue
        
        print(f"Checking {filename}...")
        
        # Try to get project ID from download URL first
        project_id = None
        if downloads:
            project_id = extract_project_id_from_url(downloads[0])
        
        # If that fails, try to get version info by hash
        version_info = None
        if sha1_hash:
            version_info = get_version_info_by_hash(sha1_hash)
            if version_info:
                project_id = version_info.get('project_id')
        
        if not project_id:
            errors.append(f"Could not determine project ID for mod: {filename}")
            print(f"{Colors.RED}❌ {filename}: Could not determine project ID{Colors.RESET}")
            continue
            
        # Get project info
        project = get_project_info(project_id)
        if not project:
            missing.append({'slug': project_id})
            print(f"{Colors.RED}❌ {filename}: Project not found on Modrinth{Colors.RESET}")
            continue
            
        name = project.get('title', project_id)
        current_version = version_info.get('version_number', 'unknown') if version_info else 'unknown'
        
        # Check if mod file exists locally
        mod_file_path = os.path.join(mods_dir, filename) if filename else None
        mod_exists_locally = mod_file_path and os.path.exists(mod_file_path)
        
        latest, is_newer = get_latest_version(project_id, mc_version, loaders, current_version, version_info)
        
        if latest and is_newer:
            # Download new file
            primary_file = next((f for f in latest['files'] if f['primary']), latest['files'][0])
            url = primary_file['url']
            new_jar = os.path.join(tempfile.gettempdir(), primary_file['filename'])
            
            if download_file(url, new_jar):
                try:
                    if mod_exists_locally:
                        # Update existing mod
                        backup_and_replace_mod(mods_dir, filename, new_jar)
                    else:
                        # Download new mod
                        final_path = os.path.join(mods_dir, primary_file['filename'])
                        shutil.move(new_jar, final_path)
                        
                    updated.append({
                        'name': name,
                        'slug': project_id,
                        'old_version': current_version,
                        'new_version': latest['version_number'],
                        'changelog': latest.get('changelog', '').strip()
                    })
                    
                    # Add mod data for .mrpack generation
                    mod_list_for_mrpack.append({
                        'filename': primary_file['filename'],
                        'url': url,
                        'sha1': primary_file.get('hashes', {}).get('sha1'),
                        'project_slug': project_id,
                        'env': mod.get('env', {"client": "required", "server": "optional"})
                    })
                    
                    print(f"{Colors.GREEN}✅ {name}: Updated {current_version} → {latest['version_number']}{Colors.RESET}")
                except Exception as e:
                    errors.append(f"Failed to update {project_id}: {e}")
                    print(f"{Colors.RED}❌ {name}: Failed to update ({e}){Colors.RESET}")
            else:
                errors.append(f"Failed to download new version for {project_id}")
                print(f"{Colors.RED}❌ {name}: Failed to download new version{Colors.RESET}")
                
        elif latest and not is_newer:
            # Download current version if not exists locally
            if not mod_exists_locally:
                # Use the original download URL from the modpack
                download_url = downloads[0] if downloads else latest['files'][0]['url']
                download_filename = filename or latest['files'][0]['filename']
                new_jar = os.path.join(tempfile.gettempdir(), download_filename)
                
                if download_file(download_url, new_jar):
                    final_path = os.path.join(mods_dir, download_filename)
                    shutil.move(new_jar, final_path)
                    print(f"{Colors.YELLOW}📥 {name}: Downloaded current version {current_version}{Colors.RESET}")
                else:
                    errors.append(f"Failed to download current version for {project_id}")
                    print(f"{Colors.RED}❌ {name}: Failed to download current version{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}🟡 {name}: Already up-to-date (file exists){Colors.RESET}")
                    
            uptodate.append({'name': name, 'slug': project_id, 'version': current_version})
            
            # Add mod data for .mrpack generation (use current version info)
            if latest:
                primary_file = next((f for f in latest['files'] if f['primary']), latest['files'][0])
                mod_list_for_mrpack.append({
                    'filename': filename or primary_file['filename'],
                    'url': downloads[0] if downloads else primary_file['url'],
                    'sha1': sha1_hash or primary_file.get('hashes', {}).get('sha1'),
                    'project_slug': project_id,
                    'env': mod.get('env', {"client": "required", "server": "optional"})
                })
            
        elif not latest:
            # Couldn't find any version for this mod
            missing.append({'slug': project_id})
            print(f"{Colors.RED}❌ {name}: No compatible versions found{Colors.RESET}")
        else:
            errors.append(f"Unknown error for {project_id}")
            print(f"{Colors.RED}❌ {name}: Unknown error{Colors.RESET}")

    # Use modpack name for changelog
    changelog_path = os.path.join("/Users/lexicodes/Lunarbit-Modrinth-Autoupdater", f'{modpack_name}_changelog.md')
    write_changelog(changelog_path, updated, uptodate, missing, errors)
    print(f"\nChangelog written to {changelog_path}")
    
    # Generate .mrpack files if requested
    if (args.client or args.server) and mod_list_for_mrpack:
        print(f"\n{Colors.GREEN}Generating .mrpack files...{Colors.RESET}")
        
        # Extract version info for .mrpack
        version_id = index.get('versionId', f"v{datetime.now().strftime('%Y.%m.%d')}")
        modloader = loaders[0].replace('-loader', '') if loaders else 'fabric'
        
        if args.client:
            print(f"\n{Colors.GREEN}📱 Generating client modpack...{Colors.RESET}")
            generate_mrpack(
                modpack_name=modpack_name,
                version_id=version_id,
                mc_version=mc_version,
                modloader=modloader,
                mod_list=mod_list_for_mrpack,
                mode="client",
                overrides_folder=args.overrides_folder
            )
        
        if args.server:
            print(f"\n{Colors.GREEN}🖥️  Generating server modpack...{Colors.RESET}")
            generate_mrpack(
                modpack_name=modpack_name,
                version_id=version_id,
                mc_version=mc_version,
                modloader=modloader,
                mod_list=mod_list_for_mrpack,
                mode="server",
                overrides_folder=args.overrides_folder
            )
    elif args.client or args.server:
        print(f"{Colors.YELLOW}⚠️  No mods found for .mrpack generation{Colors.RESET}")
    
    # Print summary
    print(f"\n{Colors.GREEN}Summary:{Colors.RESET}")
    print(f"{Colors.GREEN}✅ Updated: {len(updated)}{Colors.RESET}")
    print(f"{Colors.YELLOW}🟡 Up-to-date: {len(uptodate)}{Colors.RESET}")
    print(f"{Colors.RED}❌ Missing/Failed: {len(missing) + len(errors)}{Colors.RESET}")
    print(f"\n{Colors.GREEN}Mods exported to: {mods_dir}{Colors.RESET}")
    
    if temp_dir:
        shutil.rmtree(temp_dir)

if __name__ == '__main__':
    main()
