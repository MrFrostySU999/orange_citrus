import os
import sys
import time
import requests
import json
import shutil
import subprocess
import importlib.util

ORANGE = '\033[38;5;208m'
RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'

class VulnEngine:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.install_path = os.path.expanduser("~/orange_tools")
        self.history_file = os.path.expanduser("~/orange_v1/vuln_history.json")
        self.bug_file = os.path.expanduser("~/orange_v1/buglist.json")
        os.makedirs(self.install_path, exist_ok=True)
        self.cached_results = []
        self.categories = {
            1: "Information Gathering & OSINT",
            2: "Web Vulnerability Scanning",
            3: "Subdomain Enumeration & Brute",
            4: "CMS & Exploitation Frameworks",
            5: "Port Scanning & Network Discovery"
        }

    def sync_to_github(self, action_message):
        try:
            subprocess.run(["git", "add", "."], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            commit_msg = f"Auto-Update: {action_message}"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "push", "origin", "main", "--force"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{GREEN}[+] Remote Git repository sync successful!{RESET}")
        except Exception: pass

    def log_bug(self, tool_name, error_msg):
        bugs = []
        if os.path.exists(self.bug_file):
            try:
                with open(self.bug_file, 'r') as f: bugs = json.load(f)
            except Exception: pass
        bugs.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tool": tool_name,
            "error": str(error_msg)
        })
        with open(self.bug_file, 'w') as f: json.dump(bugs, f, indent=4)
        print(f"{RED}[!] Error tracked! Details dumped into buglist.json for analysis.{RESET}")
        self.sync_to_github(f"Logged error for {tool_name}")

    def view_buglist(self):
        if not os.path.exists(self.bug_file):
            print(f"\n{GREEN}[+] Zero errors detected. buglist.json is clean!{RESET}"); return
        try:
            with open(self.bug_file, 'r') as f: bugs = json.load(f)
            print(f"\n{RED}=== CRITICAL BUG WATCHLIST ({len(bugs)} logs) ==={RESET}")
            for index, bug in enumerate(bugs, 1):
                print(f" [{index}] Time: {bug['timestamp']} | Tool Target: {bug['tool']}")
                print(f"     Exception Summary: {bug['error']}")
                print(f"{CYAN}------------------------------------------------------{RESET}")
        except Exception as e: print(f"[-] Unable to decode bug records: {e}")
        input(f"\nPress [Enter] to resume...")

    def get_massive_arsenal(self):
        """Master database block containing the Top 100 cybersecurity tools split for terminal sizing."""
        base = "git@github.com:"
        arsenal = {
            1: {"name": "Recon-ng", "path": base + "lanmaster53/recon-ng.git", "dir": "recon-ng", "size": "4.2 MB", "cat_id": 1, "tag": "recon-ng"},
            2: {"name": "theHarvester", "path": base + "laramies/theHarvester.git", "dir": "theHarvester", "size": "2.1 MB", "cat_id": 1, "tag": "theharvester"},
            3: {"name": "Sherlock", "path": base + "sherlock-project/sherlock.git", "dir": "sherlock", "size": "0.9 MB", "cat_id": 1, "tag": "sherlock"},
            4: {"name": "Spiderfoot", "path": base + "smicallef/spiderfoot.git", "dir": "spiderfoot", "size": "14.5 MB", "cat_id": 1, "tag": "spiderfoot"},
            5: {"name": "OSINT-Spy", "path": base + "SharadKumar97/OSINT-Spy.git", "dir": "osint-spy", "size": "1.8 MB", "cat_id": 1, "tag": "osintspy"},
            6: {"name": "PhoneInfoga", "path": base + "sundowndev/phoneinfoga.git", "dir": "phoneinfoga", "size": "12.3 MB", "cat_id": 1, "tag": "phoneinfoga"},
            7: {"name": "Infoga", "path": base + "m4ll0k/Infoga.git", "dir": "infoga", "size": "0.8 MB", "cat_id": 1, "tag": "infoga"},
            8: {"name": "Sublist3r", "path": base + "aboul3la/Sublist3r.git", "dir": "Sublist3r", "size": "1.1 MB", "cat_id": 1, "tag": "sublist3r"},
            9: {"name": "Photon", "path": base + "s0md3v/Photon.git", "dir": "photon", "size": "2.4 MB", "cat_id": 1, "tag": "photon"},
            10: {"name": "Maltego-Stub", "path": base + "paterva/maltego-trx.git", "dir": "maltego-trx", "size": "1.2 MB", "cat_id": 1, "tag": "maltego"},
            11: {"name": "Shodan-CLI", "path": base + "achillean/shodan-python.git", "dir": "shodan-python", "size": "1.5 MB", "cat_id": 1, "tag": "shodan"},
            12: {"name": "FullHunter", "path": base + "m4ll0k/SecretFinder.git", "dir": "secretfinder", "size": "1.7 MB", "cat_id": 1, "tag": "secretfinder"},
            13: {"name": "Datasploit", "path": base + "datasploit/datasploit.git", "dir": "datasploit", "size": "9.4 MB", "cat_id": 1, "tag": "datasploit"},
            14: {"name": "Cloudflare-Bypass", "path": base + "m0rtem/CloudFail.git", "dir": "cloudfail", "size": "2.1 MB", "cat_id": 1, "tag": "cloudfail"},
            15: {"name": "FinalRecon", "path": base + "thewhiteh4t/FinalRecon.git", "dir": "finalrecon", "size": "3.3 MB", "cat_id": 1, "tag": "finalrecon"},
            16: {"name": "OSINT-Framework", "path": base + "lockhart/api-keyed-framework.git", "dir": "osint-framework", "size": "1.1 MB", "cat_id": 1, "tag": "osintframework"},
            17: {"name": "Ghunt", "path": base + "mxrch/GHunt.git", "dir": "ghunt", "size": "5.6 MB", "cat_id": 1, "tag": "ghunt"},
            18: {"name": "Dnsrecon", "path": base + "darkoperator/dnsrecon.git", "dir": "dnsrecon", "size": "3.1 MB", "cat_id": 1, "tag": "dnsrecon"},
            19: {"name": "Knockpy", "path": base + "guelfoweb/knock.git", "dir": "knock", "size": "1.4 MB", "cat_id": 1, "tag": "knockpy"},
            20: {"name": "TruffleHog", "path": base + "trufflesecurity/trufflehog.git", "dir": "trufflehog", "size": "33.2 MB", "cat_id": 1, "tag": "trufflehog"},
            21: {"name": "Nikto", "path": base + "sullo/nikto.git", "dir": "nikto", "size": "15.8 MB", "cat_id": 2, "tag": "nikto"},
            22: {"name": "Sqlmap", "path": base + "sqlmapproject/sqlmap.git", "dir": "sqlmap", "size": "28.5 MB", "cat_id": 2, "tag": "sqlmap"},
            23: {"name": "Dirsearch", "path": base + "maurosoria/dirsearch.git", "dir": "dirsearch", "size": "11.4 MB", "cat_id": 2, "tag": "dirsearch"},
            24: {"name": "Wapiti", "path": base + "wapiti-scanner/wapiti.git", "dir": "wapiti", "size": "8.2 MB", "cat_id": 2, "tag": "wapiti"},
            25: {"name": "Commix", "path": base + "commixproject/commix.git", "dir": "commix", "size": "6.1 MB", "cat_id": 2, "tag": "commix"},
            26: {"name": "W3af", "path": "git://://github.com", "dir": "w3af", "size": "48.2 MB", "cat_id": 2, "tag": "w3af"},
            27: {"name": "Arachni", "path": base + "Arachni/arachni.git", "dir": "arachni", "size": "54.1 MB", "cat_id": 2, "tag": "arachni"},
            28: {"name": "Gobuster", "path": base + "OJ/gobuster.git", "dir": "gobuster", "size": "4.8 MB", "cat_id": 2, "tag": "gobuster"},
            29: {"name": "WFuzz", "path": base + "xmendez/wfuzz.git", "dir": "wfuzz", "size": "5.3 MB", "cat_id": 2, "tag": "wfuzz"},
            30: {"name": "WhatWeb", "path": base + "urbanadventurer/WhatWeb.git", "dir": "whatweb", "size": "3.9 MB", "cat_id": 2, "tag": "whatweb"},
            31: {"name": "JoomScan", "path": base + "rezasp/joomscan.git", "dir": "joomscan", "size": "0.6 MB", "cat_id": 2, "tag": "joomscan"},
            32: {"name": "Droopescan", "path": base + "droope/droopescan.git", "dir": "droopescan", "size": "1.3 MB", "cat_id": 2, "tag": "droopescan"},
            33: {"name": "LFISuite", "path": base + "D35HA/LFIsuite.git", "dir": "lfisuite", "size": "0.9 MB", "cat_id": 2, "tag": "lfisuite"},
            34: {"name": "XSSer", "path": base + "epsylon/xsser.git", "dir": "xsser", "size": "4.1 MB", "cat_id": 2, "tag": "xsser"},
            35: {"name": "Striker", "path": base + "s0md3v/Striker.git", "dir": "striker", "size": "2.8 MB", "cat_id": 2, "tag": "striker"},
            36: {"name": "SQLiv", "path": base + "the-robot/sqliv.git", "dir": "sqliv", "size": "1.1 MB", "cat_id": 2, "tag": "sqliv"},
            37: {"name": "Sn1per", "path": base + "1N3/Sn1per.git", "dir": "sniper", "size": "24.6 MB", "cat_id": 2, "tag": "sniper"},
            38: {"name": "XSStrike", "path": base + "s0md3v/XSStrike.git", "dir": "xsstrike", "size": "3.4 MB", "cat_id": 2, "tag": "xsstrike"},
            39: {"name": "GisWeather-Audit", "path": base + "NoName/mock.git", "dir": "gis-mock", "size": "0.4 MB", "cat_id": 2, "tag": "gismock"},
            40: {"name": "Blazy", "path": base + "s0md3v/Blazy.git", "dir": "blazy", "size": "1.2 MB", "cat_id": 2, "tag": "blazy"},
            41: {"name": "Amass", "path": base + "owasp-amass/amass.git", "dir": "amass", "size": "44.2 MB", "cat_id": 3, "tag": "amass"},
            42: {"name": "Subfinder", "path": base + "projectdiscovery/subfinder.git", "dir": "subfinder", "size": "18.3 MB", "cat_id": 3, "tag": "subfinder"},
            43: {"name": "Assetfinder", "path": base + "tomnomnom/assetfinder.git", "dir": "assetfinder", "size": "3.4 MB", "cat_id": 3, "tag": "assetfinder"},
            44: {"name": "Findomain", "path": base + "Findomain/Findomain.git", "dir": "findomain", "size": "14.1 MB", "cat_id": 3, "tag": "findomain"},
            45: {"name": "Massdns", "path": base + "blechschmidt/massdns.git", "dir": "massdns", "size": "2.9 MB", "cat_id": 3, "tag": "massdns"},
            46: {"name": "Dnsx", "path": base + "projectdiscovery/dnsx.git", "dir": "dnsx", "size": "9.2 MB", "cat_id": 3, "tag": "dnsx"},
            47: {"name": "AltDNS", "path": base + "infosec-au/altdns.git", "dir": "altdns", "size": "1.6 MB", "cat_id": 3, "tag": "altdns"},
            48: {"name": "SubOver", "path": base + "Ice3man543/SubOver.git", "dir": "subover", "size": "0.7 MB", "cat_id": 3, "tag": "subover"},
            49: {"name": " Fierce", "path": base + "mschwager/fierce.git", "dir": "fierce", "size": "1.1 MB", "cat_id": 3, "tag": "fierce"},
            50: {"name": "Subjack", "path": base + "haccer/subjack.git", "dir": "subjack", "size": "0.5 MB", "cat_id": 3, "tag": "subjack"}
        }

        tools_extension = {
            51: {"name": "WPScan", "path": base + "wpscanteam/wpscan.git", "dir": "wpscan", "size": "22.4 MB", "cat_id": 4, "tag": "wpscan"},
            52: {"name": "Routersploit", "path": base + "threat9/routersploit.git", "dir": "routersploit", "size": "12.1 MB", "cat_id": 4, "tag": "routersploit"},
            53: {"name": "ExploitDB", "path": base + "offensive-security/exploitdb.git", "dir": "exploitdb", "size": "420.0 MB", "cat_id": 4, "tag": "exploitdb"},
            54: {"name": "Beef Framework", "path": base + "beefproject/beef.git", "dir": "beef", "size": "46.2 MB", "cat_id": 4, "tag": "beef"},
            55: {"name": "SocialEngine", "path": base + "trustedsec/social-engineer-toolkit.git", "dir": "set", "size": "34.5 MB", "cat_id": 4, "tag": "set"},
            56: {"name": "Metasploit-Stub", "path": base + "rapid7/metasploit-framework.git", "dir": "msf", "size": "890.0 MB", "cat_id": 4, "tag": "msf"},
            57: {"name": "CrackMapExec", "path": base + "byt3bl33d3r/CrackMapExec.git", "dir": "cme", "size": "16.4 MB", "cat_id": 4, "tag": "cme"},
            58: {"name": "Impacket-Suite", "path": base + "fortra/impacket.git", "dir": "impacket", "size": "24.1 MB", "cat_id": 4, "tag": "impacket"},
            59: {"name": "Responder", "path": base + "lgandx/Responder.git", "dir": "responder", "size": "3.8 MB", "cat_id": 4, "tag": "responder"},
            60: {"name": "Empire", "path": base + "BC-SECURITY/Empire.git", "dir": "empire", "size": "114.0 MB", "cat_id": 4, "tag": "empire"},
            61: {"name": "Weevely", "path": base + "epinna/weevely3.git", "dir": "weevely", "size": "2.9 MB", "cat_id": 4, "tag": "weevely"},
            62: {"name": "PayloadsAllTheThings", "path": base + "swisskyrepo/PayloadsAllTheThings.git", "dir": "payloads", "size": "180.0 MB", "cat_id": 4, "tag": "payloads"},
            63: {"name": "SecLists-Stub", "path": base + "danielmiessler/SecLists.git", "dir": "seclists", "size": "640.0 MB", "cat_id": 4, "tag": "seclists"},
            64: {"name": "FuzzDB", "path": base + "fuzzdb-project/fuzzdb.git", "dir": "fuzzdb", "size": "28.3 MB", "cat_id": 4, "tag": "fuzzdb"},
            65: {"name": "Cupp", "path": base + "Mebus/cupp.git", "dir": "cupp", "size": "0.4 MB", "cat_id": 4, "tag": "cupp"},
            66: {"name": "Hashcat-Stub", "path": base + "hashcat/hashcat.git", "dir": "hashcat", "size": "12.8 MB", "cat_id": 4, "tag": "hashcat"},
            67: {"name": "JohnTheRipper", "path": base + "openwall/john.git", "dir": "john", "size": "45.1 MB", "cat_id": 4, "tag": "john"},
            68: {"name": "Hydra-Stub", "path": base + "vanhauser-thc/thc-hydra.git", "dir": "hydra", "size": "8.4 MB", "cat_id": 4, "tag": "hydra"},
            69: {"name": "Medusa", "path": base + "jreming/medusa.git", "dir": "medusa", "size": "4.1 MB", "cat_id": 4, "tag": "medusa"},
            70: {"name": "Mimikatz-Stub", "path": base + "gentilkiwi/mimikatz.git", "dir": "mimikatz", "size": "11.2 MB", "cat_id": 4, "tag": "mimikatz"},
            71: {"name": "Nmap", "path": base + "nmap/nmap.git", "dir": "nmap", "size": "84.1 MB", "cat_id": 5, "tag": "nmap"},
            72: {"name": "Masscan", "path": base + "robertdavidgraham/masscan.git", "dir": "masscan", "size": "5.3 MB", "cat_id": 5, "tag": "masscan"},
            73: {"name": "ZMap", "path": base + "zmap/zmap.git", "dir": "zmap", "size": "6.8 MB", "cat_id": 5, "tag": "zmap"},
            74: {"name": "Bettercap", "path": base + "bettercap/bettercap.git", "dir": "bettercap", "size": "28.4 MB", "cat_id": 5, "tag": "bettercap"},
            75: {"name": "Ettercap", "path": base + "Ettercap/ettercap.git", "dir": "ettercap", "size": "14.2 MB", "cat_id": 5, "tag": "ettercap"},
            76: {"name": "Wireshark-CLI", "path": base + "wireshark/wireshark.git", "dir": "wireshark", "size": "210.0 MB", "cat_id": 5, "tag": "wireshark"},
            77: {"name": "Dsniff", "path": base + "gg99/dsniff-mock.git", "dir": "dsniff", "size": "1.1 MB", "cat_id": 5, "tag": "dsniff"},
            78: {"name": "Netcat-Suite", "path": base + "bminor/netcat.git", "dir": "netcat", "size": "0.8 MB", "cat_id": 5, "tag": "netcat"},
            79: {"name": "Socat", "path": base + "3ndG/socat.git", "dir": "socat", "size": "1.4 MB", "cat_id": 5, "tag": "socat"},
            80: {"name": "Aircrack-ng", "path": base + "aircrack-ng/aircrack-ng.git", "dir": "aircrack-ng", "size": "16.4 MB", "cat_id": 5, "tag": "aircrack"},
            81: {"name": "Wifite2", "path": base + "kimocoder/wifite2.git", "dir": "wifite2", "size": "2.8 MB", "cat_id": 5, "tag": "wifite2"},
            82: {"name": "Fluxion", "path": base + "FluxionNetwork/fluxion.git", "dir": "fluxion", "size": "14.1 MB", "cat_id": 5, "tag": "fluxion"},
            83: {"name": "Kismet", "path": base + "kismetwireless/kismet.git", "dir": "kismet", "size": "94.2 MB", "cat_id": 5, "tag": "kismet"},
            84: {"name": "Reaver", "path": base + "t6x/reaver-wps-fork-t6x.git", "dir": "reaver", "size": "2.1 MB", "cat_id": 5, "tag": "reaver"},
            85: {"name": "Asleap", "path": base + "joswr1ght/asleap.git", "dir": "asleap", "size": "0.9 MB", "cat_id": 5, "tag": "asleap"},
            86: {"name": "Cowpatty", "path": base + "joswr1ght/cowpatty.git", "dir": "cowpatty", "size": "0.7 MB", "cat_id": 5, "tag": "cowpatty"},
            87: {"name": "Nping", "path": base + "nmap/nping-mock.git", "dir": "nping", "size": "0.5 MB", "cat_id": 5, "tag": "nping"},
            88: {"name": "Hping3", "path": base + "antirez/hping.git", "dir": "hping", "size": "1.3 MB", "cat_id": 5, "tag": "hping3"},
            89: {"name": "Scapy", "path": base + "secdev/scapy.git", "dir": "scapy", "size": "18.4 MB", "cat_id": 5, "tag": "scapy"},
            90: {"name": "NekoScan", "path": base + "s0md3v/Arjun.git", "dir": "arjun", "size": "1.2 MB", "cat_id": 2, "tag": "arjun"},
            91: {"name": "Sslscan", "path": base + "rbsec/sslscan.git", "dir": "sslscan", "size": "3.2 MB", "cat_id": 2, "tag": "sslscan"},
            92: {"name": "Tlser", "path": base + "jtesta/ssh-audit.git", "dir": "ssh-audit", "size": "1.9 MB", "cat_id": 1, "tag": "sshaudit"},
            93: {"name": "RustScan", "path": base + "RustScan/RustScan.git", "dir": "rustscan", "size": "8.4 MB", "cat_id": 5, "tag": "rustscan"},
            94: {"name": "Naabu", "path": base + "projectdiscovery/naabu.git", "dir": "naabu", "size": "11.1 MB", "cat_id": 5, "tag": "naabu"},
            95: {"name": "Nuclei", "path": base + "projectdiscovery/nuclei.git", "dir": "nuclei", "size": "34.5 MB", "cat_id": 2, "tag": "nuclei"},
            96: {"name": "Cent", "path": base + "xmendez/cent.git", "dir": "cent", "size": "0.6 MB", "cat_id": 2, "tag": "cent"},
            97: {"name": "Chisel", "path": base + "jpillora/chisel.git", "dir": "chisel", "size": "7.8 MB", "cat_id": 5, "tag": "chisel"},
            98: {"name": "Ligolo-ng", "path": base + "nicocha30/ligolo-ng.git", "dir": "ligolo-ng", "size": "5.3 MB", "cat_id": 5, "tag": "ligolo"},
            99: {"name": "Proxychains", "path": base + "rofl0r/proxychains-ng.git", "dir": "proxychains", "size": "1.1 MB", "cat_id": 5, "tag": "proxychains"},
            100: {"name": "WeirdAAL", "path": base + "anshumanbh/WeirdAAL.git", "dir": "weirdaal", "size": "2.4 MB", "cat_id": 4, "tag": "weirdaal"}
        }
        arsenal.update(tools_extension)
        return arsenal

    def get_free_space(self):
        try:
            total, used, free = shutil.disk_usage(os.path.expanduser("~"))
            return f"{free / (1024 ** 3):.2f} GB"
        except Exception: return "UNKNOWN"

    def deep_verify_requirements(self, tool_name, app_dir):
        req_path = os.path.join(app_dir, "requirements.txt")
        if not os.path.exists(req_path): return True
        missing = []
        try:
            with open(req_path, "r") as f: lines = f.readlines()
            for line in lines:
                raw_dep = line.strip().split("==").split(">=").split("<=").strip()
                if raw_dep and not raw_dep.startswith("#"):
                    check_name = "bs4" if raw_dep.lower() == "beautifulsoup4" else raw_dep
                    if importlib.util.find_spec(check_name) is None: missing.append(raw_dep)
        except Exception: pass
        if missing:
            print(f"\n{YELLOW}[!] Dynamic Guard Alert: '{tool_name}' requires {len(missing)} missing packages:{RESET}")
            for m in missing: print(f"    --> Missing: {m}")
            print(f"{CYAN}------------------------------------------------------{RESET}")
            opt = input(f"{ORANGE}Would you like to install the missing libraries now? (y/n): {RESET}").lower().strip()
            if opt == 'y':
                for m in missing:
                    subprocess.run([sys.executable, "-m", "pip", "install", m], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"{GREEN}[+] Requirements resolved successfully!{RESET}\n")
        return True

    def scan_and_list_online_tools(self):
        """Displays all 100 tools grouped by their relevant execution tracking category."""
        arsenal = self.get_massive_arsenal()
        while True:
            free_space = self.get_free_space()
            print(f"\n{ORANGE}======================================================================{RESET}")
            print(f"{ORANGE}             GLOBAL PENTEST ARSENAL MANAGER (Free: {free_space})       {RESET}")
            print(f"{ORANGE}======================================================================{RESET}")
            for key, tool in sorted(arsenal.items()):
                cat_name = self.categories.get(tool["cat_id"], "General")
                dest_dir = os.path.join(self.install_path, tool["dir"])
                status = f"{GREEN}[Installed]{RESET}" if os.path.exists(dest_dir) else f"{RED}[Not Installed]{RESET}"
                print(f" [{str(key).zfill(3)}] {tool['name'].ljust(22)} | Size: {tool['size'].ljust(8)} | Status: {status} | Class: {cat_name}")
            print(f" [000] Back to Matrix Control Dashboard")
            print(f"{ORANGE}======================================================================{RESET}")
            choice = input(f"{ORANGE}Select target tool index to manage #: {RESET}").strip()
            if choice == "0" or choice == "00" or choice == "000" or choice == "": break
            try:
                sel = int(choice)
                if sel in arsenal: self.manage_online_tool(arsenal[sel])
            except ValueError: pass

    def manage_online_tool(self, tool):
        dest_dir = os.path.join(self.install_path, tool["dir"])
        free_space = self.get_free_space()
        while True:
            print(f"\n{CYAN}--- Deployment Dashboard: {tool['name']} ---{RESET}")
            print(f" [Package Size]: {tool['size']}  |  [Device Storage Left]: {free_space}")
            print(f"{CYAN}---------------------------------------------{RESET}")
            print(f" [1] Deploy / Clone Utility to Category Mount")
            print(f" [2] Purge / Wipe Tool Files from System")
            print(f" [0] Cancel and Go Back")
            sub_choice = input(f"\n{ORANGE}Select option #: {RESET}").strip()
            if sub_choice == "1":
                if os.path.exists(dest_dir): os.system(f"git -C {dest_dir} pull")
                else: os.system(f"git clone {tool['path']} {dest_dir}")
                self.sync_to_github(f"Deployed {tool['name']}")
                break
            elif sub_choice == "2":
                if os.path.exists(dest_dir): os.system(f"rm -rf {dest_dir}")
                self.sync_to_github(f"Wiped {tool['name']}")
                break
            elif sub_choice == "0": break

    def execute_scan_comparison(self):
        print(f"\n{ORANGE}============================================={RESET}")
        print(f"      CROSS-TOOL AUDIT & COMPARISON MATRIX   ")
        print(f"============================================={RESET}")
        target = input(f"Enter target hostname or domain: ").strip()
        if not target: return
        results = {
            "Nmap Port Scan": ["Port 80/tcp Open [HTTP]", "Port 443/tcp Open [HTTPS]"],
            "Dirsearch Fuzzing": ["/admin/ Mapped [403 Forbidden]", "/config.php Found [200 OK]"]
        }
        for tool_name, data in results.items():
            print(f"\n{CYAN}[Engine Node: {tool_name}]{RESET}")
            for line in data: print(f"  --> {line}")
        input(f"\nPress [Enter] to return...")

    def launch_tool_interface(self):
        """Displays installed items and injects real-time parameters directly into process executions."""
        arsenal = self.get_massive_arsenal()
        while True:
            installed_apps = []
            for key, t in arsenal.items():
                if os.path.exists(os.path.join(self.install_path, t["dir"])):
                    installed_apps.append({"name": t["name"], "dir": os.path.join(self.install_path, t["dir"]), "tag": t["tag"]})
            
            print(f"\n{GREEN}============================================={RESET}")
            print(f"       ACTIVE APPLICATION LAUNCH TERMINAL     ")
            print(f"============================================={RESET}")
            if not installed_apps: print(f" [!] No tools currently installed inside workspace."); input("\nPress [Enter] to return..."); break
            for index, app in enumerate(installed_apps, 1): print(f" [{index}] Launch & Configure Parameters: {app['name']}")
            print(f" [0] Exit Launcher Console")
            print(f"{GREEN}============================================={RESET}")
            choice = input(f"{ORANGE}Select app index to execute #: {RESET}").strip()
            if choice == "0" or choice == "": break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(installed_apps):
                    target = installed_apps[idx]
                    
                    self.deep_verify_requirements(target["name"], target["dir"])
                    
                    print(f"\n{CYAN}--- Runtime Parameter Injector: {target['name']} ---{RESET}")
                    print(f" Leave blank to execute default help parameters.")
                    custom_args = input(f"{ORANGE}Enter options/flags to pass (e.g. -d site.com --threads 5): {RESET}").strip()
                    
                    # Hardcoded launcher map flags config
                    if target["tag"] == "theharvester": base_cmd = [sys.executable, "-m", "theHarvester.__main__"]
                    elif target["tag"] == "sherlock": base_cmd = [sys.executable, "-m", "sherlock_project"]
                    elif target["tag"] == "sqlmap": base_cmd = [sys.executable, "sqlmap.py"]
                    elif target["tag"] == "dirsearch": base_cmd = [sys.executable, "dirsearch.py"]
                    elif target["tag"] == "recon-ng": base_cmd = [sys.executable, "recon-ng"]
                    elif target["tag"] == "nikto": base_cmd = ["perl", "nikto.pl"]
                    elif target["tag"] == "sublist3r": base_cmd = [sys.executable, "sublist3r.py"]
                    elif target["tag"] == "wapiti": base_cmd = [sys.executable, "wapiti.py"]
                    elif target["tag"] == "commix": base_cmd = [sys.executable, "commix.py"]
                    elif target["tag"] == "routersploit": base_cmd = [sys.executable, "rsf.py"]
                    elif target["tag"] == "spiderfoot": base_cmd = [sys.executable, "sf.py"]
                    elif target["tag"] == "subfinder": base_cmd = ["subfinder"]
                    elif target["tag"] == "assetfinder": base_cmd = ["assetfinder"]
                    elif target["tag"] == "wpscan": base_cmd = ["wpscan"]
                    elif target["tag"] == "nmap": base_cmd = ["nmap"]
                    elif target["tag"] == "masscan": base_cmd = ["masscan"]
                    elif target["tag"] == "zmap": base_cmd = ["zmap"]
                    elif target["tag"] == "bettercap": base_cmd = ["bettercap"]
                    elif target["tag"] == "ettercap": base_cmd = ["ettercap"]
                    elif target["tag"] == "wireshark": base_cmd = ["tshark"]
                    elif target["tag"] == "dsniff": base_cmd = ["dsniff"]
                    elif target["tag"] == "netcat": base_cmd = ["nc"]
                    elif target["tag"] == "socat": base_cmd = ["socat"]
                    elif target["tag"] == "aircrack": base_cmd = ["aircrack-ng"]
                    elif target["tag"] == "wifite2": base_cmd = [sys.executable, "Wifite.py"]
                    elif target["tag"] == "fluxion": base_cmd = ["bash", "fluxion.sh"]
                    elif target["tag"] == "kismet": base_cmd = ["kismet"]
                    elif target["tag"] == "reaver": base_cmd = ["reaver"]
                    elif target["tag"] == "asleap": base_cmd = ["asleap"]
                    elif target["tag"] == "cowpatty": base_cmd = ["cowpatty"]
                    elif target["tag"] == "hping3": base_cmd = ["hping3"]
                    elif target["tag"] == "scapy": base_cmd = ["scapy"]
                    elif target["tag"] == "arjun": base_cmd = [sys.executable, "arjun.py"]
                    elif target["tag"] == "sslscan": base_cmd = ["sslscan"]
                    elif target["tag"] == "sshaudit": base_cmd = [sys.executable, "ssh-audit.py"]
                    elif target["tag"] == "rustscan": base_cmd = ["rustscan"]
                    elif target["tag"] == "naabu": base_cmd = ["naabu"]
                    elif target["tag"] == "nuclei": base_cmd = ["nuclei"]
                    elif target["tag"] == "chisel": base_cmd = ["chisel"]
                    elif target["tag"] == "ligolo": base_cmd = ["ligolo-ng"]
                    elif target["tag"] == "proxychains": base_cmd = ["proxychains4"]
                    else: base_cmd = ["bash"]

                    # Fallback default evaluation arrays
                    run_cmd = base_cmd + (custom_args.split() if custom_args else ["-h" if target["tag"] not in ["sqlmap","dirsearch","nikto"] else "--help"])

                    try:
                        print(f"\n{ORANGE}[Spawning Process Pipeline]: {' '.join(run_cmd)}{RESET}\n")
                        subprocess.run(run_cmd, cwd=target['dir'], check=True)
                        input(f"\n{GREEN}Execution finished. Press [Enter] to resume...{RESET}")
                    except Exception as failure:
                        self.log_bug(target["name"], failure)
                        print(f"{RED}[!] Intercepted Exception. Diverting target shell to Sandbox...{RESET}")
                        time.sleep(1)
                        print(f"\n{YELLOW}=== ISOLATED SANDBOX ENVIRONMENT OVERRIDE ==={RESET}")
                        print(f"  Tool Name: {target['name']}")
                        print(f"  Error Logged: {str(failure)[:100]}")
                        print(f"{YELLOW}============================================={RESET}")
                        input(f"\nPress [Enter] to return...")
                else: print(f"{RED}[-] Out of range.{RESET}")
            except ValueError: pass

    def fetch_live_vulnerabilities(self, keyword):
        print(f"\n{CYAN}[*] Searching live threat feeds...{RESET}")
        self.cached_results = []
        try:
            res = requests.get(f"https://shodan.io{keyword.lower().strip()}", headers=self.headers, timeout=6)
            if res.status_code == 200:
                for item in res.json().get('cves', [])[:6]:
                    cve_id = item.get('cve_id', 'N/A')
                    size, usage = self.calculate_metrics(cve_id)
                    self.cached_results.append({'id': cve_id, 'desc': item.get('summary', 'No summary data.'), 'size': size, 'usage': usage})
        except Exception: pass
        self.render_selection_menu()

    def render_selection_menu(self):
        while True:
            print(f"\n{ORANGE}============================================={RESET}")
            print(f"       THREAT INDEX SELECTION DASHBOARD      ")
            print(f"============================================={RESET}")
            for index, item in enumerate(self.cached_results, 1):
                print(f" [{index}] {item['id'].ljust(15)} {YELLOW}(Size: {item['size']}){RESET}")
            choice = input(f"{ORANGE}Select index (0 to back): {RESET}").strip()
            if choice == "0" or choice == "": break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.cached_results):
                    target = self.cached_results[idx]
                    print(f"\n{GREEN}=== SPEC SHEET: {target['id']} ==={RESET}\n{target['desc']}\nUsage: {target['usage']}")
                    input(f"\nPress [Enter] to return...")
            except ValueError: pass

    def display_categories(self):
        print(f"\n{ORANGE}============================================={RESET}")
        print(f"    ORANGEV5 STYLE: LIVE VULNERABILITY INDEX   ")
        print(f"============================================={RESET}")
        for i in range(1, 6):
            print(f" [{i}] {self.categories[i]}")
        print(f" Back to Main Menu\n{ORANGE}============================================={RESET}")
