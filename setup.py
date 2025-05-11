import os

# Kreiraj dodatne foldere i šablone ako su potrebni
os.makedirs("reports", exist_ok=True)
os.makedirs("targets", exist_ok=True)
os.makedirs("ai_templates/generated", exist_ok=True)

# Kreiraj početne fajlove
with open("reports/.gitkeep", "w") as f:
    f.write("")

with open("targets/targets.txt", "w") as f:
    f.write("# Add target URLs/domains here\n")

with open("ai_templates/generated/README.md", "w") as f:
    f.write("# Auto-generated AI Templates\n")

# Ažuriraj README
with open("README.md", "a") as f:
    f.write("\n\n## New Additions\n- `reports/`: output reports\n- `targets/`: target list\n- `ai_templates/generated/`: dynamic templates")

"Direktorijumi i fajlovi za proširenje su dodati."
