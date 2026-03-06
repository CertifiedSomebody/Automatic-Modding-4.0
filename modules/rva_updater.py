import re
import shutil


def parse_dump_file(dump_path):
    """
    Parse dump.cs and return dictionary:
    (class_name, method_name) -> RVA
    """

    rva_map = {}
    current_class = None

    with open(dump_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        line = lines[i]

        # Detect class name
        class_match = re.search(r'class\s+(\w+)', line)
        if class_match:
            current_class = class_match.group(1)

        # Detect RVA
        rva_match = re.search(r'RVA:\s*(0x[0-9A-Fa-f]+)', line)
        if rva_match and i + 1 < len(lines):

            rva = rva_match.group(1)
            method_line = lines[i + 1]

            name_match = re.search(r'(\w+)\(', method_line)

            if name_match and current_class:
                method = name_match.group(1)

                key = (current_class.lower(), method.lower())
                rva_map[key] = rva

    return rva_map


def update_main_cpp(main_path, rva_map, backup=True):
    """
    Update HOOK RVAs in main.cpp
    Returns: (updated_count, missing_count)
    """

    if backup:
        backup_path = main_path + ".bak"
        shutil.copy(main_path, backup_path)

    with open(main_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    updated = 0
    missing = 0

    current_class = None
    current_method = None

    for i, line in enumerate(lines):

        # Detect comment like: // ClassName::MethodName()
        comment_match = re.search(r'//\s*(\w+)::(\w+)', line)
        if comment_match:
            current_class = comment_match.group(1)
            current_method = comment_match.group(2)

        # Update HOOK line
        if "HOOK(" in line and current_class and current_method:

            key = (current_class.lower(), current_method.lower())

            if key in rva_map:
                new_rva = rva_map[key]

                lines[i] = re.sub(r'0x[0-9A-Fa-f]+', new_rva, line)
                updated += 1
            else:
                missing += 1

            # reset so wrong comment isn't reused
            current_class = None
            current_method = None

    with open(main_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return updated, missing