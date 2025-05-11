import os
import json
import csv
from datetime import datetime

def generate_markdown_report(results, out_dir="reports"):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(out_dir, f"report_{timestamp}.md")

    with open(file_path, "w") as f:
        f.write(f"# ShadowFox Report – {timestamp}\n\n")
        for result in results:
            f.write(f"## Test: {result['tool']}\n")
            f.write(f"**Target:** {result['target']}\n")
            f.write(f"**Status:** {result['status']}\n\n")
            f.write("```\n")
            f.write(result['output'])
            f.write("\n```\n\n")

    print(f"[+] Markdown izveštaj: {file_path}")
    return file_path

def generate_json_report(results, out_dir="reports"):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(out_dir, f"report_{timestamp}.json")

    with open(file_path, "w") as f:
        json.dump(results, f, indent=4)

    print(f"[+] JSON izveštaj: {file_path}")
    return file_path

def generate_csv_report(results, out_dir="reports"):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(out_dir, f"report_{timestamp}.csv")

    with open(file_path, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["tool", "target", "status", "output"])
        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print(f"[+] CSV izveštaj: {file_path}")
    return file_path
