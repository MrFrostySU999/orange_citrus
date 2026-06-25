import sys
from vuln_scanner import VulnEngine, ORANGE, RESET, CYAN, RED

def main_menu():
    engine = VulnEngine()
    while True:
        print(f"\n{ORANGE}============================================={RESET}")
        print(f"{ORANGE}        ORANGE_CITRUS v5 CONTROL MATRIX       {RESET}")
        print(f"{ORANGE}============================================={RESET}")
        print(f" {CYAN}[1]{RESET} View Live Vulnerability Tools Database")
        print(f" {CYAN}[2]{RESET} Direct Internet Live Exploit Lookup")
        print(f" {CYAN}[0]{RESET} Terminate Session")
        print(f"{ORANGE}============================================={RESET}")
        
        choice = input(f"{ORANGE}Execute Option #: {RESET}").strip()
        if choice == "1":
            while True:
                engine.display_categories()
                cat_choice = input(f"\n{ORANGE}Select target module (0 to exit): {RESET}").strip()
                if cat_choice == "0": break
                try: engine.manage_tool(int(cat_choice))
                except ValueError: pass
        elif choice == "2":
            keyword = input(f"\n{ORANGE}Enter keyword to scan online database: {RESET}").strip()
            if keyword: engine.fetch_live_vulnerabilities(keyword)
        elif choice == "0":
            print(f"{RED}[*] Disconnecting engine terminals.{RESET}")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
