#!/data/data/com.termux/files/usr/bin/bash
echo "[+] Pinging target..."
ping -c 3 example.com > reports/ping_result.txt
echo "[+] Done."
