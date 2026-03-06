import os
import xml.etree.ElementTree as ET

ANDROID_NS = "http://schemas.android.com/apk/res/android"
NS = "{%s}" % ANDROID_NS

ET.register_namespace("android", ANDROID_NS)


# -------------------------------------------------
# Remove unwanted entries
# -------------------------------------------------
def remove_unwanted(root, application):

    removed = {
        "check_license": False,
        "license_activity": False,
        "license_provider": False
    }

    # remove CHECK_LICENSE permission
    for perm in list(root.findall("uses-permission")):
        if perm.attrib.get(NS + "name") == "com.android.vending.CHECK_LICENSE":
            root.remove(perm)
            removed["check_license"] = True

    # remove license activity
    for act in list(application.findall("activity")):
        name = act.attrib.get(NS + "name", "")
        if "pairip.licensecheck.LicenseActivity" in name:
            application.remove(act)
            removed["license_activity"] = True

    # remove license provider
    for prov in list(application.findall("provider")):
        name = prov.attrib.get(NS + "name", "")
        if "pairip.licensecheck.LicenseContentProvider" in name:
            application.remove(prov)
            removed["license_provider"] = True

    return removed


# -------------------------------------------------
# Insert SYSTEM_ALERT_WINDOW after INTERNET
# -------------------------------------------------
def add_overlay_permission(root):

    overlay = "android.permission.SYSTEM_ALERT_WINDOW"

    # remove existing duplicates
    for perm in list(root.findall("uses-permission")):
        if perm.attrib.get(NS + "name") == overlay:
            root.remove(perm)

    new_perm = ET.Element("uses-permission")
    new_perm.set(NS + "name", overlay)

    perms = root.findall("uses-permission")

    for perm in perms:
        if perm.attrib.get(NS + "name") == "android.permission.INTERNET":
            index = list(root).index(perm)
            root.insert(index + 1, new_perm)
            return True

    # fallback if INTERNET not found
    root.insert(0, new_perm)
    return True


# -------------------------------------------------
# Add launcher service
# -------------------------------------------------
def add_launcher_service(application):

    for service in application.findall("service"):
        if service.attrib.get(NS + "name") == "com.android.support.Launcher":
            return False

    service = ET.Element("service")

    service.set(NS + "name", "com.android.support.Launcher")
    service.set(NS + "enabled", "true")
    service.set(NS + "exported", "false")
    service.set(NS + "stopWithTask", "true")

    application.append(service)

    return True


# -------------------------------------------------
# Main manifest modifier
# -------------------------------------------------
def modify_manifest(apk_folder):

    manifest_path = os.path.join(apk_folder, "AndroidManifest.xml")

    if not os.path.exists(manifest_path):
        raise Exception("AndroidManifest.xml not found")

    tree = ET.parse(manifest_path)
    root = tree.getroot()

    application = root.find("application")

    if application is None:
        raise Exception("Application tag not found")

    removed = remove_unwanted(root, application)

    perm_added = add_overlay_permission(root)

    service_added = add_launcher_service(application)

    # Pretty format XML (fixes same-line issues)
    ET.indent(tree, space="    ")

    tree.write(
        manifest_path,
        encoding="utf-8",
        xml_declaration=True
    )

    return {
        "permission_added": perm_added,
        "service_added": service_added,
        "removed": removed
    }