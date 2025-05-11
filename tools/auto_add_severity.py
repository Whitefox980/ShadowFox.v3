import os

POC_DIR = "poc_scripts"
SEVERITY_FUNC = "\nfrom utils.log_utils import classify_severity"

def update_file_with_severity(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

    modified = False
    new_lines = []
    for line in lines:
        if "log_to_sheet(" in line and "classify_severity" not in "".join(lines):
            indent = line[:len(line) - len(line.lstrip())]
            new_lines.append(f"{indent}severity = classify_severity({line.split('(')[1].split(',')[1].strip().rstrip(')')})\n")
            line = line.replace("log_to_sheet(", "log_to_sheet(").rstrip() + " + f' | Severity: {{severity}}')\n"
            modified = True
        new_lines.append(line)

    if modified:
        if SEVERITY_FUNC not in "".join(lines):
            for i, line in enumerate(new_lines):
                if line.startswith("from utils.log_utils import log_to_sheet"):
                    new_lines[i] = line.rstrip() + ", classify_severity\n"
                    break
            else:
                new_lines.insert(0, SEVERITY_FUNC + "\n")
        with open(filepath, "w") as f:
            f.writelines(new_lines)
        print(f"[+] Updated: {filepath}")
    else:
        print(f"[-] Skipped (no change): {filepath}")

for file in os.listdir(POC_DIR):
    if file.endswith(".py"):
        update_file_with_severity(os.path.join(POC_DIR, file))
