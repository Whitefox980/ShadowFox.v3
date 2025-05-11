#!/data/data/com.termux/files/usr/bin/bash

echo "========================================"
echo "   SHADOWFOX STEALTH MODE ACTIVATION"
echo "========================================"

# 1. Proveri da li je Tor već aktivan
TOR_STATUS=$(ps aux | grep -v grep | grep tor)

if [ -z "$TOR_STATUS" ]; then
    echo "[*] Tor nije aktivan. Pokrećem..."
    tor & sleep 5
else
    echo "[✓] Tor je već aktivan."
fi

# 2. Postavi proxy promenljive
export ALL_PROXY=socks5://127.0.0.1:9050
echo "[*] Proxy setovan na socks5://127.0.0.1:9050"

# 3. Provera IP adrese kroz Tor mrežu
echo "[*] Proveravam Tor IP..."
RESULT=$(curl -s --socks5 127.0.0.1:9050 https://check.torproject.org)

if [[ $RESULT == *"Congratulations"* ]]; then
    echo "[✓] TOR RADI — IP je maskiran."
    echo "[+] Pokrećem ShadowFox..."
    cd ~/ShadowFox2
    python3 runner.py
else
    echo "[!] NISI na Tor mreži! STOPIRAM ShadowFox radi zaštite."
fi
