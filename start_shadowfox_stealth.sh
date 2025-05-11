#!/data/data/com.termux/files/usr/bin/bash

LOGFILE="$HOME/ShadowFox2/logs/stealth_boot.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo -e "\n[$DATE] === Pokretanje ShadowFox u stealth režimu ===" >> $LOGFILE

# 1. Pokreni Proton VPN (CLI verzija, ili zameni sa wg-quick up)
echo "[*] Povezivanje na VPN..." | tee -a $LOGFILE
protonvpn-cli c --fastest --sc >> $LOGFILE 2>&1

sleep 3

# 2. Proveri IP adresu
VPN_IP=$(curl -s https://ipinfo.io/ip)
echo "[*] Detektovana IP adresa: $VPN_IP" | tee -a $LOGFILE

# 3. Provera: da li IP pripada Proton-u
ISP=$(curl -s https://ipinfo.io/org)

if [[ $ISP == *"Proton"* || $ISP == *"M247"* || $ISP == *"Datacamp"* ]]; then
    echo "[+] VPN potvrđen ($ISP), pokrećem sistem..." | tee -a $LOGFILE
    cd ~/ShadowFox2
    python3 runner.py | tee -a $LOGFILE
else
    echo "[!] VPN NIJE AKTIVAN! ISP: $ISP" | tee -a $LOGFILE
    echo "[!] STOPIRANO — ShadowFox neće startovati bez zaštite!" | tee -a $LOGFILE
fi
