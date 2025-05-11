#!/bin/bash

echo "============================="
echo "  SHADOWFOX FUZZ STARTUJE..."
echo "============================="

# (opcionalno) Očisti prethodni log
# echo "[*] Čistim stare logove i PDF..."
# rm -f logs/*.txt reports/*.pdf

# Pokreni main
python3 main.py --fuzz

echo "============================="
echo "   ShadowFox Fuzz ZAVRŠEN"
echo "   PDF: reports/shadow_summary.pdf"
echo "============================="
