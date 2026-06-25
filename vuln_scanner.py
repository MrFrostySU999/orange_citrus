import os
import sys
import time
import requests
import json
import shutil
import subprocess

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
            3: "Subdomain Brute-Forcing",
            4: "CMS & WordPress Auditing",
            5: "Port Scanning & Network Discovery"
        }

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
        print(f"{RED}[!] Error logged! Details dumped into buglist.json for analysis.{RESET}")

    def view_buglist(self):
        if not os.path.exists(self.bug_file):
            print(f"{GREEN}[+] Zero errors detected. buglist.json is clean!{RESET}"); return
        try:
            with open(self.bug_file, 'r') as f: bugs = json.load(f)
            print(f"\n{RED}=== CRITICAL BUG WATCHLIST ({len(bugs)} logs) ==={RESET}")
            for index, bug in enumerate(bugs, 1):
                print(f" [{index}] Time: {bug['timestamp']} | Tool Target: {bug['tool']}")
                print(f"     Exception Summary: {bug['error']}")
                print(f"{CYAN}------------------------------------------------------{RESET}")
        except Exception as e: print(f"[-] Unable to decode bug records: {e}")
        input(f"\nPress [Enter] to resume...")

    def get_tool_meta(self, choice):
        meta = {
            1: {"name": "Recon-ng", "path": "lanmaster53/recon-ng.git", "dir": "recon-ng", "size": "4.2 MB", "exec": "recon-ng"},
            2: {"name": "Nikto", "path": "sullo/nikto.git", "dir": "nikto", "size": "15.8 MB", "exec": "nikto.pl"},
            3: {"name": "Sublist3r", "path": "aboul3la/Sublist3r.git", "dir": "Sublist3r", "size": "1.1 MB", "exec": "sublist3r.py"},
            4: {"name": "WPScan", "path": "wpscanteam/wpscan.git", "dir": "wpscan", "size": "22.4 MB", "exec": "wpscan"},
            5: {"name": "Nmap", "path": "nmap/nmap.git", "dir": "nmap", "size": "84.1 MB", "exec": "nmap"}
        }
        return meta.get(choice, None)

    def get_online_tool_feed(self):
        return {
            1: {"name": "theHarvester", "path": "laramies/theHarvester.git", "dir": "theHarvester", "size": "2.1 MB", "cat_id": 1, "func": "Gathers OSINT data from public sources.", "exec": "theHarvester.py"},
            2: {"name": "Sqlmap", "path": "sqlmapproject/sqlmap.git", "dir": "sqlmap", "size": "28.5 MB", "cat_id": 2, "func": "Automates SQL injection auditing.", "exec": "sqlmap.py"},
            3: {"name": "Amass", "path": "owasp-amass/amass.git", "dir": "amass", "size": "44.2 MB", "cat_id": 3, "func": "In-depth asset discovery mapping.", "exec": "amass"},
            4: {"name": "Dirsearch", "path": "maurosoria/dirsearch.git", "dir": "dirsearch", "size": "11.4 MB", "cat_id": 2, "func": "Brute forces web server directories.", "exec": "dirsearch.py"},
            5: {"name": "Sherlock", "path": "sherlock-project/sherlock.git", "dir": "sherlock", "size": "0.9 MB", "cat_id": 1, "func": "Hunts profiles by username.", "exec": "sherlock.py"}
        }

    def get_free_space(self):
        try:
            total, used, free = shutil.disk_usage(os.path.expanduser("~"))
            return f"{free / (1024 ** 3):.2f} GB"
        except Exception: return "UNKNOWN"

    def scan_and_list_online_tools(self):
        feed = self.get_online_tool_feed()
        while True:
            print(f"\n{ORANGE}============================================={RESET}")
            print(f"{ORANGE}      ONLINE PENTEST UTILITY CATALOGUE       {RESET}")
            print(f"{ORANGE}============================================={RESET}")
            for key, tool in feed.items():
                cat_name = self.categories.get(tool["cat_id"], "General")
                dest_dir = os.path.join(self.install_path, tool["dir"])
                status = f"{GREEN}[Installed]{RESET}" if os.path.exists(dest_dir) else f"{RED}[Not Installed]{RESET}"
                print(f" [{key}] {tool['name'].ljust(15)} Size: {tool['size'].ljust(8)} Status: {status}")
                print(f"     Target Layer: {cat_name}")
            print(f" [0] Return to Matrix Menu")
            print(f"{ORANGE}============================================={RESET}")
            choice = input(f"{ORANGE}Select utility index: {RESET}").strip()
            if choice == "0" or choice == "": break
            try:
                sel = int(choice)
                if sel in feed: self.manage_online_tool(feed[sel])
            except ValueError: pass

    def manage_online_tool(self, tool):
        dest_dir = os.path.join(self.install_path, tool["dir"])
        free_space = self.get_free_space()
        while True:
            print(f"\n{CYAN}--- Management Matrix: {tool['name']} ---{RESET}")
            print(f" [Spec]: {tool['func']}")
            print(f" [Size]: {tool['size']}  |  [Free Space]: {free_space}")
            print(f"{CYAN}---------------------------------------------{RESET}")
            print(f" [1] Download / Route Tool")
            print(f" [2] Purge Tool Files")
            print(f" [0] Cancel and Back")
            sub_choice = input(f"\n{ORANGE}Option #: {RESET}").strip()
            if sub_choice == "1":
                if os.path.exists(dest_dir): os.system(f"git -C {dest_dir} pull")
                else: os.system(f"git clone git@github.com:{tool['path']} {dest_dir}")
                break
            elif sub_choice == "2":
                if os.path.exists(dest_dir): os.system(f"rm -rf {dest_dir}")
                break
            elif sub_choice == "0": break

    def launch_tool_interface(self):
        while True:
            installed_apps = []
            for i in range(1, 6):
                t = self.get_tool_meta(i)
                if os.path.exists(os.path.join(self.install_path, t["dir"])):
                    installed_apps.append({"name": t["name"], "dir": os.path.join(self.install_path, t["dir"]), "exec": t["exec"]})
            for key, t in self.get_online_tool_feed().items():
                if os.path.exists(os.path.join(self.install_path, t["dir"])):
                    installed_apps.append({"name": t["name"] + " [Expansion]", "dir": os.path.join(self.install_path, t["dir"]), "exec": t["exec"]})
            
            print(f"\n{GREEN}============================================={RESET}")
            print(f"{GREEN}       ACTIVE APPLICATION LAUNCH TERMINAL     {RESET}")
            print(f"{GREEN}============================================={RESET}")
            if not installed_apps: print(f" [!] No tools installed."); input("\nPress [Enter] to return..."); break
            for index, app in enumerate(installed_apps, 1): print(f" [{index}] Launch: {app['name']}")
            print(f" [0] Exit Launcher")
            print(f"{GREEN}============================================={RESET}")
            choice = input(f"{ORANGE}Select app index to run: {RESET}").strip()
            if choice == "0" or choice == "": break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(installed_apps):
                    target = installed_apps[idx]
                    req_path = os.path.join(target['dir'], "requirements.txt")
                    if os.path.exists(req_path):
                        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=target['dir'])
                    found_path = None
                    for root, dirs, files in os.walk(target["dir"]):
                        if target["exec"] in files:
                            found_path = os.path.relpath(os.path.join(root, target["exec"]), target["dir"]); break
                        elif "__main__.py" in files and target["exec"].replace(".py", "") in root.lower():
                            found_path = os.path.relpath(os.path.join(root, "__main__.py"), target["dir"]); break
                    if found_path:
                        if found_path.endswith(".py"): run_cmd = [sys.executable, found_path, "--help"]
                        elif found_path.endswith(".pl"): run_cmd = ["perl", found_path, "-Help"]
                        else: run_cmd = ["bash", found_path, "--help"]
                    else: run_cmd = [sys.executable, "-m", target["exec"].replace(".py", ""), "--help"]
                    try:
                        print(f"{ORANGE}[Running]: {' '.join(run_cmd)}{RESET}\n")
                        subprocess.run(run_cmd, cwd=target['dir'], check=True)
                        input(f"\n{GREEN}Press [Enter] to exit...{RESET}")
                    except Exception as failure: self.log_bug(target["name"], failure); input("\nPress [Enter]...")
            except ValueError: pass

    def calculate_metrics(self, cve_id):
        num_seed = sum(int(c) for c in cve_id if c.isdigit())
        return f"{(num_seed % 15) + 2.4:.1f} KB", f"exploit_framework --cve {cve_id}"

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
            print(f" [0] Back to Main Menu")
            print(f"{ORANGE}============================================={RESET}")
            choice = input(f"{ORANGE}Select index to inspect: {RESET}").strip()
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
            tool = self.get_tool_meta(i)
            status = f"{GREEN}[Installed]{RESET}" if os.path.exists(os.path.join(self.install_path, tool["dir"])) else f"{RED}[Not Installed]{RESET}"
            print(f" [{i}] {tool['name'].ljust(35)} {status}")
        print(f" [0] Back to Main Menu\n{ORANGE}============================================={RESET}")

    def manage_tool(self, choice):
        tool = self.get_tool_meta(choice)
        if not tool: return
        target_dir = os.path.join(self.install_path, tool["dir"])
        free_space = self.get_free_space()
        while True:
            print(f"\n{CYAN}--- Management Matrix: {tool['name']} ---{RESET}")
            print(f" [Size]: {tool['size']}  |  [Free Space]: {free_space}")
            print(f"{CYAN}---------------------------------------------{RESET}")
            print(f" [1] Install / Sync Tool")
            print(f" [2] Uninstall Tool")
            print(f" [3] Search Live Sites for Vulnerabilities")
            print(f" [0] Back to Listing")
            sub_choice = input(f"\n{ORANGE}Select option: {RESET}").strip()
            if sub_choice == "1":
                if os.path.exists(target_dir): os.system(f"git -C {target_dir} pull")
                else: os.system(f"git clone git@github.com:{tool['path']} {target_dir}")
                break
            elif sub_choice == "2":
                os.system(f"rm -rf {target_dir}")
                break
            elif sub_choice == "3":
                keyword = input(f"\n{ORANGE}Enter keyword to query: {RESET}").strip()
                if keyword: self.fetch_live_vulnerabilities(keyword)
                break
            elif sub_choice == "0": break
