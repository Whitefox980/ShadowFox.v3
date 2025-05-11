#!/bin/bash

echo "================================="
echo "  SHADOWFOX: RECON + FUZZ START"
echo "================================="

echo "[*] Pokrećem RECON fazu..."
python3 main.py --recon

echo "[*] Pokrećem FUZZ fazu..."
python3 main.py --fuzz

PDF_PATH="reports/shadow_summary.pdf"

if [ -f "$PDF_PATH" ]; then
    echo "[✓] PDF generisan: $PDF_PATH"

    # Ako si u Termuxu
    if command -v termux-open >/dev/null 2>&1; then
        termux-open "$PDF_PATH"
    # Ako si na Linux desktopu
    elif command -v xdg-open >/dev/null 2>&1; then
        xdg-open "$PDF_PATH"
    fi
else
    echo "[!] PDF nije generisan."
fi

echo "================================="
echo "  ShadowFox ALL završen."
echo "================================="
