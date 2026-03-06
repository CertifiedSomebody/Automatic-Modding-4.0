import os
import shutil
import re


# -------------------------------------------------
# Find rainbow asset inside app-debug
# -------------------------------------------------
def find_asset(app_debug_folder):

    for root, dirs, files in os.walk(app_debug_folder):
        for file in files:
            if file.lower() == "rainbow.png":
                return os.path.join(root, file)

    raise Exception("rainbow.png not found inside app-debug folder")


# -------------------------------------------------
# Copy rainbow.png asset
# -------------------------------------------------
def copy_asset(apk_folder, asset_path):

    if not os.path.exists(asset_path):
        raise Exception("Asset file not found: " + asset_path)

    dest_assets = os.path.join(apk_folder, "assets")
    os.makedirs(dest_assets, exist_ok=True)

    dest_file = os.path.join(dest_assets, os.path.basename(asset_path))

    shutil.copy2(asset_path, dest_file)

    return dest_file


# -------------------------------------------------
# Detect lib folder inside app-debug
# -------------------------------------------------
def find_lib_root(app_debug_folder):

    for root, dirs, files in os.walk(app_debug_folder):
        if os.path.basename(root) == "lib":
            return root

    raise Exception("lib folder not found inside app-debug")


# -------------------------------------------------
# Detect architecture and copy correct .so
# -------------------------------------------------
def copy_so(apk_folder, lib_source_root):

    apk_lib_folder = os.path.join(apk_folder, "lib")

    if not os.path.exists(apk_lib_folder):
        raise Exception("lib folder not found inside decompiled APK")

    copied_arch = None

    for arch in os.listdir(apk_lib_folder):

        dest_arch = os.path.join(apk_lib_folder, arch)
        source_arch = os.path.join(lib_source_root, arch)

        if not os.path.isdir(dest_arch):
            continue

        if not os.path.isdir(source_arch):
            continue

        for file in os.listdir(source_arch):

            if not file.endswith(".so"):
                continue

            src_file = os.path.join(source_arch, file)
            dst_file = os.path.join(dest_arch, file)

            shutil.copy2(src_file, dst_file)

        copied_arch = arch

    if not copied_arch:
        raise Exception("No matching ABI found between app-debug libs and APK")

    return copied_arch


# -------------------------------------------------
# Find smali root inside app-debug
# -------------------------------------------------
def find_smali_root(app_debug_folder):

    for root, dirs, files in os.walk(app_debug_folder):
        if os.path.basename(root).startswith("smali"):
            return os.path.dirname(root)

    raise Exception("smali folder not found inside app-debug")


# -------------------------------------------------
# Find next smali_classesX folder
# -------------------------------------------------
def get_next_smali_folder(apk_folder):

    max_index = 1

    for name in os.listdir(apk_folder):

        if name == "smali":
            max_index = max(max_index, 1)

        match = re.match(r"smali_classes(\d+)", name)

        if match:
            num = int(match.group(1))
            max_index = max(max_index, num)

    next_folder = f"smali_classes{max_index + 1}"
    next_path = os.path.join(apk_folder, next_folder)

    os.makedirs(next_path, exist_ok=True)

    return next_path


# -------------------------------------------------
# Copy smali menu files
# -------------------------------------------------
def copy_smali(apk_folder, smali_root):

    dest_folder = get_next_smali_folder(apk_folder)

    copied_any = False

    for folder in os.listdir(smali_root):

        if not folder.startswith("smali"):
            continue

        source_com = os.path.join(smali_root, folder, "com")

        if not os.path.exists(source_com):
            continue

        dest_com = os.path.join(dest_folder, "com")

        shutil.copytree(source_com, dest_com, dirs_exist_ok=True)

        copied_any = True

    if not copied_any:
        raise Exception("No 'com' folders found in smali source")

    return dest_folder


# -------------------------------------------------
# Main Injector Function
# -------------------------------------------------
def inject_assets(apk_folder, app_debug_folder):

    if not os.path.exists(apk_folder):
        raise Exception("APK folder not found")

    if not os.path.exists(app_debug_folder):
        raise Exception("app-debug folder not found")

    # Auto detect components
    asset_path = find_asset(app_debug_folder)
    lib_root = find_lib_root(app_debug_folder)
    smali_root = find_smali_root(app_debug_folder)

    # Perform injections
    asset_result = copy_asset(apk_folder, asset_path)

    arch_used = copy_so(apk_folder, lib_root)

    smali_dest = copy_smali(apk_folder, smali_root)

    return {
        "asset_copied_to": asset_result,
        "lib_arch_used": arch_used,
        "smali_destination": smali_dest
    }