import os
import re

INJECT_LINE = "\n    invoke-static {p0}, Lcom/android/support/Main;->Start(Landroid/content/Context;)V\n"


# -------------------------------------------------
# Inject mod menu call inside onCreate
# -------------------------------------------------
def inject_oncreate(smali_file):

    if not os.path.exists(smali_file):
        raise Exception("Smali file not found")

    with open(smali_file, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    # Prevent duplicate injection
    for line in lines:
        if "Lcom/android/support/Main;->Start" in line:
            print("Mod menu already injected")
            return True

    new_lines = []
    inside_oncreate = False
    injected = False

    for line in lines:

        stripped = line.strip()
        new_lines.append(line)

        # Detect start of onCreate
        if stripped.startswith(".method") and "onCreate(Landroid/os/Bundle;)V" in stripped:
            inside_oncreate = True
            continue

        if inside_oncreate:

            # Inject AFTER invoke-super onCreate call
            if "invoke-super" in stripped and "onCreate" in stripped:

                new_lines.append(INJECT_LINE)
                injected = True
                inside_oncreate = False
                continue

        # Stop scanning if method ends
        if inside_oncreate and stripped.startswith(".end method"):
            inside_oncreate = False

    if not injected:
        raise Exception("invoke-super onCreate call not found, injection failed")

    with open(smali_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print("Mod menu injected successfully")

    return True