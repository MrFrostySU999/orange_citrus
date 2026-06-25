#!/bin/bash
# 1. Back up old config if it exists
mkdir -p /etc
cp /etc/resolv.conf /etc/resolv.conf.bak 2>/dev/null || true

# 2. Inject stable public DNS addresses directly into your system network file
echo "nameserver 8.8.8.8" > /etc/resolv.conf
echo "nameserver 8.8.4.4" >> /etc/resolv.conf

# 3. Test the connection immediately using a standard ping lookup
echo "[*] Testing network resolution..."
if getent ahosts raw.githubusercontent.com > /dev/null; then
    echo -e "\033[1;32m[+] Internet connection restored successfully!\033[0m"
else
    echo -e "\033[1;31m[-] Still offline. Please double-check that your phone's Wi-Fi or mobile data is turned on.\033[0m"
fi
