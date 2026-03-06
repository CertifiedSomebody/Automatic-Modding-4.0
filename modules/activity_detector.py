import os
import xml.etree.ElementTree as ET


# -------------------------------------------------
# Resolve activity name properly
# -------------------------------------------------
def resolve_activity_name(name, package_name):

    if not name:
        return None

    if name.startswith("."):
        return package_name + name

    if "." not in name:
        return package_name + "." + name

    return name


# -------------------------------------------------
# Detect launcher activity
# -------------------------------------------------
def get_launcher_activity(apk_folder):

    manifest_path = os.path.join(apk_folder, "AndroidManifest.xml")

    if not os.path.exists(manifest_path):
        raise Exception("AndroidManifest.xml not found")

    try:
        tree = ET.parse(manifest_path)
        root = tree.getroot()
    except Exception as e:
        raise Exception("Failed to parse AndroidManifest.xml: " + str(e))

    namespace = "{http://schemas.android.com/apk/res/android}"

    package_name = root.attrib.get("package", "")

    # safer application detection
    app = None
    for element in root.iter():
        if element.tag.endswith("application"):
            app = element
            break

    if app is None:
        raise Exception("Application tag not found in manifest")

    # check activity and activity-alias
    for tag in ["activity", "activity-alias"]:

        for activity in app.findall(tag):

            name = activity.attrib.get(namespace + "name")

            if not name:
                continue

            for intent in activity.findall("intent-filter"):

                has_main = False
                has_launcher = False

                for action in intent.findall("action"):
                    if action.attrib.get(namespace + "name") == "android.intent.action.MAIN":
                        has_main = True

                for category in intent.findall("category"):
                    if category.attrib.get(namespace + "name") == "android.intent.category.LAUNCHER":
                        has_launcher = True

                if has_main and has_launcher:

                    # resolve alias target activity
                    if tag == "activity-alias":
                        target = activity.attrib.get(namespace + "targetActivity")
                        if target:
                            name = target

                    name = resolve_activity_name(name, package_name)

                    if name:
                        return name

    raise Exception("Launcher activity not found in manifest")


# -------------------------------------------------
# Convert activity name to smali file path
# -------------------------------------------------
def activity_to_smali_path(apk_folder, activity_name):

    if not activity_name:
        raise Exception("Invalid activity name")

    activity_path = activity_name.replace(".", "/") + ".smali"

    smali_folders = []

    for folder in os.listdir(apk_folder):
        if folder.startswith("smali"):
            smali_folders.append(folder)

    if not smali_folders:
        raise Exception("No smali folders found in APK")

    for folder in smali_folders:

        full_path = os.path.join(apk_folder, folder, activity_path)

        if os.path.exists(full_path):
            return full_path

    raise Exception(
        f"Activity smali file not found: {activity_path}"
    )