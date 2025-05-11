import os
import json
import PyPDF2
import re

def extract_examples_from_pdfs(output_file="ai_dataset.jsonl"):
    dataset = []
    for fname in os.listdir("reports"):
        if not fname.endswith(".pdf"):
            continue
        try:
            with open(os.path.join("reports", fname), "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""

                match = re.search(r"Payload: (.+?)\nURL: (.+?)\n", text)
                exploit = re.search(r"EXPLOIT\n(.+?)\n\n", text, re.DOTALL)
                fix = re.search(r"FIX\n(.+?)\n\n", text, re.DOTALL)
                severity = re.search(r"SEVERITY: (.+?)\n", text)

                if match and exploit and fix:
                    prompt = f"Analyze the following input:\nURL: {match.group(2)}\nPayload: {match.group(1)}\n\nWhat is the vulnerability and how to exploit it?"
                    completion = f"{exploit.group(1).strip()}\n\nFix: {fix.group(1).strip()}\nSeverity: {severity.group(1).strip() if severity else 'Unknown'}"
                    dataset.append({"prompt": prompt, "completion": completion})
        except:
            continue

    with open(output_file, "w", encoding="utf-8") as out:
        for entry in dataset:
            out.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"[✓] Dataset kreiran: {output_file} ({len(dataset)} primera)")
