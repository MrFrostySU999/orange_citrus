import sys
from vuln_scanner import VulnEngine, ORANGE, RESET, CYAN, RED, GREEN

def main_menu():
    engine = VulnEngine()
    while True:
        print(f"\n{ORANGE}============================================={RESET}")
        print(f"{ORANGE}        ORANGE_CITRUS v5 CONTROL MATRIX       {RESET}")
        print(f"{ORANGE}============================================={RESET}")
        print(f" [1] Core Vulnerability Categories Manager")
        print(f" [2] Scan & Download Expansion Pentest Tools")
        print(f" [3] Direct Internet Live Exploit Lookup")
        print(f" [4] LAUNCH INSTALLED TOOLS TERMINAL")
        print(f" [5] VIEW INTERCEPTED ERROR LOGS (BUGLIST)")
        print(f" [0] Terminate Session")
        print(f"{ORANGE}============================================={RESET}")
        
        choice = input(f"{ORANGE}Execute Option #: {RESET}").strip()
        if choice == "1":
            while True:
                engine.display_categories()
                cat_choice = input(f"\n{ORANGE}Select target module (0 to exit): {RESET}").strip()
                if cat_choice == "0": break
                try: engine.manage_tool(int(cat_choice))
                except ValueError: pass
        elif choice == "2": engine.scan_and_list_online_tools()
        elif choice == "3":
            keyword = input(f"\n{ORANGE}Enter keyword to scan online database: {RESET}").strip()
            if keyword: engine.fetch_live_vulnerabilities(keyword)
        elif choice == "4": engine.launch_tool_interface()
        elif choice == "5": engine.view_buglist()
        elif choice == "0": print(f"{RED}[*] Disconnecting engine terminals.{RESET}"); sys.exit(0)

if __name__ == "__main__":
    main_menu()
