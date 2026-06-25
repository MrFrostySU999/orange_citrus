import sys
from vuln_scanner import VulnEngine, ORANGE, RESET, CYAN, RED, GREEN

def main_menu():
    engine = VulnEngine()
    version_tag = "v5.5.0-Stable"
    
    while True:
        print(f"\n{ORANGE}============================================={RESET}")
        print(f"{ORANGE}    ORANGE_CITRUS CONTROL MATRIX ({version_tag})   {RESET}")
        print(f"{ORANGE}============================================={RESET}")
        print(f" Core Vulnerability Categories Manager")
        print(f" Scan & Download Expansion Pentest Tools")
        print(f" Direct Internet Live Exploit Lookup")
        print(f" CROSS-TOOL SCANNER COMPARISON MATRIX")
        print(f" LAUNCH INSTALLED TOOLS TERMINAL")
        print(f" VIEW INTERCEPTED ERROR LOGS (BUGLIST)")
        print(f" Terminate Session")
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
        elif choice == "4": engine.execute_scan_comparison()
        elif choice == "5": engine.launch_tool_interface()
        elif choice == "6": engine.view_buglist()
        elif choice == "0": 
            print(f"{RED}[*] Disconnecting engine terminals.{RESET}"); sys.exit(0)

if __name__ == "__main__":
    main_menu()
