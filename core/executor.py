import subprocess
import os
from tools_config import TOOLS
from logics.ai_tools import suggest_exploit, suggest_fix, classify_severity
from logics.generate_pdf import save_ai_report_to_pdf
from core.logger import log_result

def run_tool(script_name, target_url):
    try:
        result = subprocess.run(
            ["python3", f"poc_scripts/{script_name}", target_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=60
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "[!] Alat je istekao (timeout)"
    except Exception as e:
        return f"[!] Greška prilikom pokretanja: {str(e)}"

def get_targets(min_priority="Low"):
    priorities_order = {"Low": 1, "Medium": 2, "High": 3}
    min_level = priorities_order.get(min_priority.capitalize(), 1)
    targets = []

    try:
        with open("targets/targets.txt") as f:
            for line in f:
                parts = [p.strip() for p in line.strip().split("|")]
                if len(parts) >= 2:
                    url = parts[0]
                    priority = parts[1].capitalize()
                    comment = parts[2] if len(parts) > 2 else ""
                    if priorities_order.get(priority, 0) >= min_level:
                        targets.append({"url": url, "priority": priority, "comment": comment})
    except FileNotFoundError:
        print("[!] targets.txt nije pronađen.")
    return targets

def run_all():
    min_priority = input("Minimalni prioritet za skeniranje (Low/Medium/High): ").strip()
    targets = get_targets(min_priority)
    if not targets:
        print("[!] Nema meta za testiranje.")
        return

    for target_data in targets:
        target = target_data["url"]
        print(f"\n=== META: {target} | {target_data['priority']} - {target_data['comment']} ===")

        for tool_id, script in TOOLS.items():
            print(f"[*] {tool_id} ...")
            output = run_tool(script, target)
            print(output)

            do_ai = input("AI analiza? [y/n]: ").lower()
            severity = "unknown"
            if do_ai == "y":
                exploit = suggest_exploit(output)
                fix = suggest_fix(output)
                severity = classify_severity(output)

                print("\n>>> AI Eksploatacija:\n", exploit)
                print("\n>>> AI Preporuka:\n", fix)
                print("\n>>> Ozbiljnost:", severity)

                if input("Sačuvaj kao PDF? [y/n]: ").lower() == "y":
                    combined = f"{tool_id.upper()} na {target}\n\n[OUTPUT]\n{output}\n\n[EXPLOIT]\n{exploit}\n\n[FIX]\n{fix}\n\n[SEVERITY]: {severity}"
                    save_ai_report_to_pdf(combined, site=target)

            log_result(target, tool_id, output, status="done", severity=severity)
            print("-" * 50)

def run_all_headless():
    targets = get_targets("Low")
    if not targets:
        print("[!] Nema meta.")
        return

    for target_data in targets:
        target = target_data["url"]
        for tool_id, script in TOOLS.items():
            output = run_tool(script, target)
            exploit = suggest_exploit(output)
            fix = suggest_fix(output)
            severity = classify_severity(output)

            combined = f"{tool_id.upper()} na {target}\n\n[OUTPUT]\n{output}\n\n[EXPLOIT]\n{exploit}\n\n[FIX]\n{fix}\n\n[SEVERITY]: {severity}"
            save_ai_report_to_pdf(combined, site=target)
            log_result(target, tool_id, output, status="done", severity=severity)

    print("[✓] Headless završeno.")

def run_selected():
    targets = get_targets()
    if not targets:
        print("[!] Nema meta.")
        return

    print("Dostupni alati:")
    keys = list(TOOLS.keys())
    for i, tool in enumerate(keys):
        print(f"[{i+1}] {tool}")
    selection = input("Unesi brojeve alata (npr. 1,3): ")
    indices = [int(x.strip()) - 1 for x in selection.split(",")]

    for target_data in targets:
        target = target_data["url"]
        print(f"\n=== META: {target} ===")

        for i in indices:
            tool_id = keys[i]
            script = TOOLS[tool_id]
            output = run_tool(script, target)
            print(output)

            do_ai = input("AI analiza? [y/n]: ").lower()
            severity = "unknown"
            if do_ai == "y":
                exploit = suggest_exploit(output)
                fix = suggest_fix(output)
                severity = classify_severity(output)

                print("\n>>> AI Eksploatacija:\n", exploit)
                print("\n>>> AI Preporuka:\n", fix)
                print("\n>>> Ozbiljnost:", severity)

                if input("PDF? [y/n]: ").lower() == "y":
                    combined = f"{tool_id.upper()} na {target}\n\n[OUTPUT]\n{output}\n\n[EXPLOIT]\n{exploit}\n\n[FIX]\n{fix}\n\n[SEVERITY]: {severity}"
                    save_ai_report_to_pdf(combined, site=target)
                from core.tagger import get_tags
                tags = get_tags(tool_id, output)
                log_result(target, tool_id, output, status="done", severity=severity, tags=tags)
                log_result(target, tool_id, output, status="done", severity=severity)
            print("-" * 50)
