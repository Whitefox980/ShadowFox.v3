#!/bin/bash

echo "[*] Kreiram osnovnu strukturu za ShadowFox..."

# Kreiranje foldera ako ne postoje
mkdir -p core logics poc_scripts utils reports logs data

# Kreiranje osnovnih fajlova
touch core/__init__.py
touch core/executor.py
touch core/shadow_operator.py
touch core/shadow_radar.py
touch core/shadow_mapper.py
touch core/shadow_stats.py
touch core/shadow_tactic_ai.py
touch core/shadow_pdf_export.py
touch core/shadow_payloads.py
touch core/shadow_control.py
touch core/shadow_log_center.py

touch logics/ai_tools.py
touch logics/fuzz_ai_trigger.py
touch logics/white_shadow_advisor.py
touch logics/black_shadow_advisor.py

touch utils/__init__.py
touch utils/log_to_text.py

# Dummy fajl za konfiguraciju i ključ
touch config.json

# Log folder i primer
touch logs/startup.log

# POC folder i primer skripti
touch poc_scripts/targets.txt
touch poc_scripts/sql_injection.py
touch poc_scripts/xss_scanner.py
touch poc_scripts/ssrf_checker.py

# Starter skripte
touch runner.py
touch start_shadowfox_vpn.sh

echo "[✓] ShadowFox struktura spremna!"
