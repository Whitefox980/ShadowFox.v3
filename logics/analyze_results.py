import os

results_dir = "results"
summary = []

if not os.path.exists(results_dir):
    print(f"[!] Folder '{results_dir}' ne postoji.")
    exit(1)

for fname in os.listdir(results_dir):
    fpath = os.path.join(results_dir, fname)
    if fname.endswith(".txt") and os.path.isfile(fpath):
        with open(fpath, "r") as f:
            content = f.read().strip()
            lines = content.splitlines()
            summary.append({
                "file": fname,
                "lines": len(lines),
                "chars": len(content),
                "pocetni_red": lines[0] if lines else "(prazan)"
            })

if summary:
    print("=== Analiza rezultata ===")
    for s in summary:
        print(f"\n[Fajl: {s['file']}]")
        print(f" - Linija: {s['lines']}")
        print(f" - Karaktera: {s['chars']}")
        print(f" - Prvi red: {s['pocetni_red']}")
else:
    print("Nema rezultata za analizu.")
