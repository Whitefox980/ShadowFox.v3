#!/data/data/com.termux/files/usr/bin/bash

echo
echo "=== SHADOWFOX VPN MODE ACTIVATION ==="
echo

echo "[*] Dobavljam trenutnu IP adresu..."
IP=$(curl -s --noproxy "*" https://1.1.1.1/cdn-cgi/trace | grep ip= | cut -d= -f2)
echo "[*] IP: $IP"

# Provera da li je lokalna adresa
if [[ "$IP" == 10.* || "$IP" == 192.168.* || "$IP" == 127.* || -z "$IP" ]]; then
  echo "[!] VPN NIJE aktivan ili IP nije zaštićen!"
  echo "[!] STOPIRANO — pokreni ProtonVPN i pokušaj ponovo."
  exit 1
else
  echo "[✓] VPN aktivan! Pokrećem ShadowFox..."
  python3 runner.py
fi
