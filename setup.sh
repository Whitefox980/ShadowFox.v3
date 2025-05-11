#!/bin/bash

echo "[*] Pokrećem ShadowFox setup..."

# .env check
if [ ! -f .env ]; then
    echo "OPENAI_API_KEY=your-key-here" > .env
    echo "[+] Kreiran .env template (unesi svoj OpenAI ključ)"
else
    echo "[✓] .env već postoji"
fi

# logs folder
if [ ! -d logs ]; then
    mkdir logs
    echo "[+] Kreiran logs/ folder"
fi

# reports folder
if [ ! -d reports ]; then
    mkdir reports
    echo "[+] Kreiran reports/ folder"
fi

# .gitignore check
if [ ! -f .gitignore ]; then
    echo "[!] .gitignore ne postoji – preporuka da ga odmah dodaš!"
else
    echo "[✓] .gitignore postoji"
fi

chmod 700 logs reports
echo "[✓] Permisije podešene (logs/ i reports/)"

echo "[✓] ShadowFox spreman za operacije."
