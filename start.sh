#!/bin/bash

echo "=== BugHunt START ==="
timestamp=$(date +%Y%m%d_%H%M%S)
log_file="logs/log_$timestamp.txt"

# 1. Očisti stare rezultate (po želji)
echo "[*] Čistim /results i /logs..." | tee -a "$log_file"
rm -f results/* logs/* reports/*

# 2. Pokreni runner.py (glavni engine)
echo "[*] Pokrećem runner.py..." | tee -a "$log_file"
python3 runner.py | tee -a "$log_file"

# 3. Analiza i generisanje izveštaja (ako postoji skripta)
if [ -f logics/generate_report.py ]; then
  echo "[*] Generišem izveštaj..." | tee -a "$log_file"
  python3 logics/generate_report.py | tee -a "$log_file"
fi

echo "=== Završeno: $timestamp ===" | tee -a "$log_file"
