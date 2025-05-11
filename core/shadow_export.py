import zipfile
import os
from datetime import datetime

def export_all_to_zip():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_name = f"shadowfox_export_{now}.zip"

    with zipfile.ZipFile(export_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # PDF izveštaji
        for root, _, files in os.walk("reports"):
            for f in files:
                full_path = os.path.join(root, f)
                zipf.write(full_path, arcname=os.path.relpath(full_path, start="."))

        # HackerOne exporti
        for root, _, files in os.walk("exports/hackerone"):
            for f in files:
                full_path = os.path.join(root, f)
                zipf.write(full_path, arcname=os.path.relpath(full_path, start="."))

        # Log fajl
        if os.path.exists("results_log.json"):
            zipf.write("results_log.json")

    print(f"[✓] ShadowFox export završen: {export_name}")
