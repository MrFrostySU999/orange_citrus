import os
import sys
import shutil
import subprocess
import requests
from config import ORANGE, RED, GREEN, CYAN, YELLOW, BLUE, WHITE, RESET

class VulnEngine:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.install_path = os.path.expanduser("~/orange_tools")
        self.global_target = "None Assigned"
        os.makedirs(self.install_path, exist_ok=True)
        
        self.vendor_maps = {
            "subfinder": "projectdiscovery/subfinder",
            "nuclei": "projectdiscovery/nuclei",
            "amass": "owasp-amass/amass",
            "wfuzz": "xmendez/wfuzz",
            "gau": "lc/gau",
            "recon-ng": "lanmaster53/recon-ng",
            "theharvester": "laramies/theHarvester",
            "sherlock": "sherlock-project/sherlock",
            "spiderfoot": "smicallef/spiderfoot",
            "dirsearch": "maurosoria/dirsearch",
            "gobuster": "OJ/gobuster",
            "nikto": "sullo/nikto",
            "sqlmap": "sqlmapproject/sqlmap",
            "wpscan": "wpscanteam/wpscan",
            "sublist3r": "aboul3la/Sublist3r",
            "cowpatty": "joswr1ght/cowpatty"
        }

    def set_global_target(self):
        print(f"\n{CYAN}=== TARGET CONF ==={RESET}")
        print(f"Target: {GREEN}{self.global_target}{RESET}")
        tgt = input("Enter target: ").strip()
        if tgt:
            self.global_target = tgt
            print(f"[+] Set: {self.global_target}")
        input("\n[Press Enter]")

    def auto_install_python_dependencies(self, tool_dir):
        req = os.path.join(tool_dir, "requirements.txt")
        if os.path.exists(req):
            print(f"[*] Syncing pip packages...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req, "--break-system-packages"])

    def get_tool_dependencies(self, tool_bin):
        dep_map = {
            "nmap": {"sys": ["nmap"], "pip": []},
            "nikto": {"sys": ["perl"], "pip": []},
            "recon-ng": {"sys": ["git"], "pip": ["mechanize", "dnspython", "beautifulsoup4", "pyyaml"]},
            "sublist3r": {"sys": ["git"], "pip": ["requests", "dnspython", "argparse"]},
            "amass": {"sys": ["git"], "pip": []},
            "cowpatty": {"sys": ["git", "make", "gcc", "libpcap-dev"], "pip": []},
            "sqlmap": {"sys": ["python3"], "pip": []},
            "wpscan": {"sys": ["ruby"], "pip": []}
        }
        return dep_map.get(tool_bin.lower(), {"sys": [], "pip": []})

    def auto_resolve_dependencies(self, tool_name, tool_bin):
        deps = self.get_tool_dependencies(tool_bin)
        print(f"\n[*] Auditing: {tool_name.upper()}")
        
        missing_sys = []
        for pkg in deps["sys"]:
            is_bin = shutil.which(pkg) is not None
            is_lib = subprocess.run(f"dpkg -s {pkg}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
            if not is_bin and not is_lib:
                missing_sys.append(pkg)

        if missing_sys:
            print(f"[!] Missing packages: {missing_sys}")
            print("[*] Unlocking system configurations...")
            subprocess.run("dpkg --purge --force-all exim4-config exim4-base exim4-daemon-light bsd-mailx", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run("apt-get autoremove -y && dpkg --configure -a", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["apt-get", "update", "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for pkg in missing_sys:
                print(f"[*] Installing system package: {pkg}")
                cmd = f"DEBIAN_FRONTEND=noninteractive apt-get install -y -o Dpkg::Options::=--force-confdef {pkg}"
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if deps["pip"]:
            for lib in deps["pip"]:
                check_name = "yaml" if lib == "pyyaml" else lib
                try:
                    __import__(check_name)
                except ImportError:
                    print(f"[*] Installing pip lib: {lib}")
                    subprocess.run([sys.executable, "-m", "pip", "install", lib, "--break-system-packages"])
        print(f"{GREEN}[+] Dependencies verified.{RESET}")

    def scan_tools(self):
        tools_list = [
            {"name": "Nmap", "bin": "nmap", "cat": "Network"},
            {"name": "Nikto", "bin": "nikto", "cat": "Web"},
            {"name": "Recon-ng", "bin": "recon-ng", "cat": "OSINT"},
            {"name": "Sublist3r", "bin": "sublist3r", "cat": "Web"},
            {"name": "Amass", "bin": "amass", "cat": "Network"},
            {"name": "Nuclei", "bin": "nuclei", "cat": "Web"},
            {"name": "Subfinder", "bin": "subfinder", "cat": "OSINT"},
            {"name": "Sqlmap", "bin": "sqlmap", "cat": "Web"},
            {"name": "Chkrootkit", "bin": "chkrootkit", "cat": "Audit"},
            {"name": "Lynis", "bin": "lynis", "cat": "Audit"},
            {"name": "Cowpatty", "bin": "cowpatty", "cat": "WiFi"}
        ]
        while True:
            print(f"\n{CYAN}=== EXPANSION PANEL ==={RESET}")
            for idx, tool in enumerate(tools_list, 1):
                exe = tool["bin"]
                local_path = os.path.join(self.install_path, exe, exe)
                compiled_bin = os.path.join(self.install_path, exe, exe + "_bin")
                is_installed = shutil.which(exe) is not None or os.path.exists(local_path) or os.path.exists(compiled_bin)
                status = f"{GREEN}Installed{RESET}" if is_installed else f"{RED}Missing{RESET}"
                print(f" [{idx}] {tool['name']:<12} | {status}")
            print(f"{CYAN}========================{RESET}")
            t_choice = input(f"\n{YELLOW}Select Tool # (0 to Exit): {RESET}").strip()
            if t_choice == "0": break
            if t_choice.isdigit() and 1 <= int(t_choice) <= len(tools_list):
                self.manage_tool(tools_list[int(t_choice) - 1])
            else:
                print(f"{RED}[-] Invalid select.{RESET}")
        return True

    def manage_tool(self, tool):
        name = tool["name"]
        exe = tool["bin"]
        while True:
            local_path = os.path.join(self.install_path, exe, exe)
            compiled_bin = os.path.join(self.install_path, exe, exe + "_bin")
            is_installed = shutil.which(exe) is not None or os.path.exists(local_path) or os.path.exists(compiled_bin)
            status = f"{GREEN}Installed{RESET}" if is_installed else f"{RED}Missing{RESET}"
            
            print(f"\n{CYAN}[*] {name.upper()} HUB ({status}){RESET}")
            print(f" [{GREEN}1{RESET}] Download / Install Tool")
            print(f" [{GREEN}2{RESET}] Launch Active Scan Instance")
            print(f" [{GREEN}3{RESET}] Uninstall / Delete Tool")
            print(f" [{GREEN}0{RESET}] Back to Index Matrix")
            act = input(f"{YELLOW}Action #: {RESET}").strip()
            if act == "0": break
            elif act == "1":
                self.auto_resolve_dependencies(name, exe)
                if is_installed:
                    print(f"{GREEN}[+] Already installed.{RESET}")
                else:
                    repo_slug = self.vendor_maps.get(exe, f"secops-tools/{exe}")
                    dest = os.path.join(self.install_path, exe)
                    if os.path.exists(dest): shutil.rmtree(dest)
                    
                    # --- FIXED STATIC STRING URL REALIGNMENT ---
                    scrub = str(repo_slug).replace("https://", "").replace("http://", "").replace("://", "")
                    scrub = scrub.replace("://github.com", "").replace("github.com", "").strip("/")
                    
                    target_url = "https://://github.com" + str(scrub) + ".git"
                    print(f"[*] Pre-Scan Interceptor: URL layout verified clean.")
                    print(f"[*] Cloning: '{target_url}'")
                    
                    proc_status = subprocess.run(["git", "clone", target_url, dest], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
                    if proc_status == 0:
                        self.auto_install_python_dependencies(dest)
                        if os.path.exists(os.path.join(dest, "Makefile")):
                            print("[*] Makefile found. Compiling...")
                            subprocess.run(["make"], cwd=dest, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            for root, dirs, files in os.walk(dest):
                                if exe in files:
                                    shutil.copy(os.path.join(root, exe), compiled_bin)
                                    break
                    else:
                        print("[*] Git download failed. Trying apt-get fallback...")
                        cmd = f"DEBIAN_FRONTEND=noninteractive apt-get install -y -o Dpkg::Options::=--force-confdef {exe}"
                        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                input("\n[Press Enter]")
            elif act == "2":
                self.auto_resolve_dependencies(name, exe)
                if not is_installed:
                    print(f"{RED}[!] Error: Run Option 1 first.{RESET}")
                elif self.global_target == "None Assigned" and tool.get("cat") not in ["Audit", "Defense", "WiFi"]:
                    print(f"{RED}[!] Error: Target is empty. Use option 5.{RESET}")
                else:
                    args = f"-F {self.global_target} --unprivileged" if exe == "nmap" else f"-h {self.global_target}"
                    if exe == "sublist3r": args = f"-d {self.global_target}"
                    run_cmd = exe if shutil.which(exe) else (compiled_bin if os.path.exists(compiled_bin) else f"python3 {local_path}")
                    print(f"{YELLOW}[Running]: {run_cmd} {args}{RESET}\n")
                    subprocess.run(f"{run_cmd} {args}", shell=True)
                input("\n[Press Enter]")
            elif act == "3":
                dest = os.path.join(self.install_path, exe)
                if os.path.exists(dest):
                    print(f"\n{YELLOW}[*] Purging files...{RESET}")
                    try: shutil.rmtree(dest)
                    except: pass
                if os.path.exists(compiled_bin):
                    try: os.remove(compiled_bin)
                    except: pass
                if shutil.which(exe):
                    print(f"\n{YELLOW}[*] Purging global package...{RESET}")
                    subprocess.run(["DEBIAN_FRONTEND=noninteractive apt-get remove -y " + exe], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    subprocess.run([sys.executable + " -m pip uninstall -y " + exe + " --break-system-packages"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"{GREEN}[+] Uninstalled.{RESET}")
                input("\n[Press Enter]")

    def fetch_live_vulnerabilities(self):
        print(f"\n{CYAN}=== LIVE LOOKUP ==={RESET}")
        kw = input(f"{YELLOW}Keyword: {RESET}").strip()
        if not kw:
            print(f"{RED}[-] Keyword req.{RESET}")
            return True
        print(f"[*] Querying indices: {kw}...")
        url = f"https://circl.lu{kw}"
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                res_list = data.get('results', data) if isinstance(data, dict) else data
                if not res_list:
                    print(f"{YELLOW}[*] No threats found.{RESET}")
                    return True
                print(f"\n{ORANGE}Latest Live Threats Matches:{RESET}")
                print(f"{BLUE}------------------------------{RESET}")
                for item in res_list[:10]:
                    cve_id = item.get('id', 'Unknown CVE')
                    summary = item.get('summary', 'No desc.')
                    score = item.get('cvss', 'N/A')
                    print(f" {GREEN}• {cve_id}{RESET} [CVSS: {YELLOW}{score}{RESET}]")
                    print(f"   {WHITE}{summary[:80]}...{RESET}\n")
                print(f"{BLUE}------------------------------{RESET}")
            else:
                print(f"{RED}[-] HTTP Error: {res.status_code}{RESET}")
        except Exception as e:
            print(f"{RED}[!] Remote Fault: {e}{RESET}")
        return True

    def run_category_menu(self):
        return self.scan_tools()
