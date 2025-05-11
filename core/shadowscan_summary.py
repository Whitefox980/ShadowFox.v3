import os
from collections import Counter
import PyPDF2
import re

VULN_KEYWORDS = [
    "xss", "sql", "sqli", "ssrf", "csrf", "rce", "idor",
    "bypass", "token", "admin", "auth", "leak"
]

def scan_pdf_keywords():
    counter = Counter()

    for fname in os.listdir("reports"):
        if not fname.endswith(".pdf"):
            continue
        try:
            with open(os.path.join("reports", fname), "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""

                for word in VULN_KEYWORDS:
                    if re.search(rf"\b{word}\b", text, re.IGNORECASE):
                        counter[word] += 1
        except:
            continue

    if not counter:
        print("[x] Nema pronađenih termina u PDF izveštajima.")
        return

    print("\n[✓] ShadowScan Rezime iz AI izveštaja:\n")
    for word, count in counter.most_common():
        print(f"{word.upper():10} : {count} puta")
