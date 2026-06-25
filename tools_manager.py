import os, shutil, subprocess
from config import RED, GREEN, YELLOW, BLUE, CYAN, WHITE, RESET, DATABASE

def check_installed(pkg):
    return shutil.which(pkg) is not None or os.path.exists(f"/usr/bin/{pkg}")

def fix_package_locks():
    broken = ["sudo", "tcpdump", "openssh-client", "openssh-server", "rpcbind", "nfs-common", "systemd", "dbus", "dbus-daemon", "dbus-system-bus-common"]
    for pkg in broken:
        postinst = f"/var/lib/dpkg/info/${pkg}.postinst"
        if os.path.exists(postinst):
            try:
                with open(postinst, 'w') as f: f.write("#!/bin/sh\nexit 0")
            except: pass
    subprocess.run(["dpkg", "--configure", "-a"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_tool_management(tool_data):
    while True:
        os.system('clear')
        is_inst = check_installed(tool_data['pkg'])
        status_text = f"{RED}Installed" if is_inst else f"{GREEN}Not Installed"
        toggle_action = f"{RED}1) Uninstall {tool_data['name']}" if is_inst else f"{GREEN}1) Install {tool_data['name']}"

        print(f"{CYAN}=====================================================${RESET}")
        print(f"{WHITE} 🍊 ORANGE MANAGED INTERFACE: {tool_data['name']}{RESET}")
        print(f"{CYAN}=====================================================${RESET}")
        print(f"{YELLOW}Description:{RESET}\n {tool_data['desc']}\n")
        print(f"{YELLOW}Syntax Profile:{RESET}\n {WHITE}{tool_data['syntax']}{RESET}\n")
        print(f"{YELLOW}Size on Disk:{RESET} {WHITE}{tool_data['size']}{RESET}")
        print(f"{YELLOW}Status:{RESET} {status_text}{RESET}")
        print(f"{CYAN}=====================================================${RESET}")
        print(f" {toggle_action}{RESET}\n {WHITE}2) Return Back{RESET}")
        print(f"{CYAN}=====================================================${RESET}")
        
        choice = input("Action selection [1-2]: ").strip()
        if choice == "1":
            fix_package_locks()
            if is_inst:
                print(f"\n{YELLOW}[*] Purging {tool_data['name']}...{RESET}")
                subprocess.run(["apt-get", "remove", "--purge", "-y", tool_data['pkg']])
                subprocess.run(["apt-get", "autoremove", "-y"])
            else:
                print(f"\n{YELLOW}[*] Downloading {tool_data['name']}...{RESET}")
                subprocess.run(["apt-get", "install", "-y", tool_data['pkg']])
            input(f"\n{GREEN}[+] Operations complete. Press Enter...{RESET}")
        elif choice == "2": break

def run_category_menu(cat_id):
    cat_data = DATABASE[cat_id]
    while True:
        os.system('clear')
        print(f"{cat_data['color']}=====================================================${RESET}")
        print(f"{WHITE} 📁 SUITE: {cat_data['title'].upper()}{RESET}")
        print(f"{WHITE} (Red = Installed | Green = Available)${RESET}")
        print(f"{cat_data['color']}=====================================================${RESET}")
        
        for idx, t_key in enumerate(cat_data['tools'], 1):
            t_data = cat_data['tools'][t_key]
            color = RED if check_installed(t_data['pkg']) else GREEN
            print(f" {color}{idx}) {t_data['name']} [{t_data['size']}]{RESET}")
            
        print(f" {RED}{len(cat_data['tools'])+1}) <- Return to Main Dashboard{RESET}")
        print(f"{cat_data['color']}=====================================================${RESET}")
        
        choice = input("Select a tool token: ").strip()
        if choice in cat_data['tools']:
            run_tool_management(cat_data['tools'][choice])
        elif choice == str(len(cat_data['tools']) + 1): break
