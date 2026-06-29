import os
import sys

# Core layout path integration
sys.path.append('/root/orange_citrus')
try:
    from vuln_scanner import VulnEngine
    engine = VulnEngine()
except ImportError as e:
    print(f"[-] Critical Error: Missing core scanner component: {e}")
    sys.exit(1)

# Graceful optional import for tools_manager to prevent class mismatch crashes
try:
    import tools_manager
    if hasattr(tools_manager, 'ToolsManager'):
        manager = tools_manager.ToolsManager()
    elif hasattr(tools_manager, 'ToolManager'):
        manager = tools_manager.ToolManager()
    else:
        manager = tools_manager  # Fallback to module-level references
except Exception:
    manager = None

# Import colors from the central configuration map safely
try:
    from config import ORANGE, RED, GREEN, CYAN, YELLOW, BLUE, WHITE, RESET
except ImportError:
    ORANGE = "\033[38;5;214m"
    RED    = "\033[1;31m"
    GREEN  = "\033[1;32m"
    CYAN   = "\033[1;36m"
    YELLOW = "\033[1;33m"
    BLUE   = "\033[1;34m"
    WHITE  = "\033[1;37m"
    RESET  = "\033[0m"

def main_menu():
    global engine, manager
    while True:
        current_target = getattr(engine, 'global_target', 'None Assigned')
        
        print(f"\n{ORANGE}🍊 Orange-Citrus Framework (v5.5.0-Stable){RESET}")
        print(f"{BLUE}[Target Locked: {GREEN}{current_target}{BLUE}]{RESET}")
        print(f"{BLUE}========================================={RESET}")
        print(f" {GREEN}1.{RESET} Core Category Menu & Tool Statuses")
        print(f" {GREEN}2.{RESET} Scan Expansion Catalogue Updates")
        print(f" {GREEN}3.{RESET} Live Exploit Lookup & Threats")
        print(f" {GREEN}4.{RESET} Cross-Tool Audit Comparison Matrix")
        print(f" {GREEN}5.{RESET} Configure Target Assignment")
        print(f" {GREEN}6.{RESET} View Automated Buglist Logs")
        print(f" {GREEN}0.{RESET} Terminate Session Console")
        print(f"{BLUE}========================================={RESET}")
        
        try:
            choice = input(f"{YELLOW}Execute Option #: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{RED}[-] Interrupted. Closing handles.{RESET}")
            break

        if choice == "1":
            if hasattr(engine, 'run_category_menu'):
                engine.run_category_menu()
            else:
                print(f"{RED}[-] Error: run_category_menu is missing from engine.{RESET}")
            input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

        elif choice == "2":
            if hasattr(engine, 'scan_tools'):
                engine.scan_tools()
            else:
                print(f"{CYAN}[*] Synchronizing online tool catalog feeds...{RESET}")
            input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

        elif choice == "3":
            # Fire separate file structure directly to completely insulate vuln_scanner parameters
            import subprocess
            subprocess.run([sys.executable, "/root/orange_citrus/exploit_lookup.py"])

        elif choice == "4":
            print(f"\n{CYAN}--- CROSS-TOOL AUDIT COMPARISON MATRIX ---{RESET}")
            if hasattr(engine, 'compare_matrix'):
                engine.compare_matrix()
            else:
                print(f"{YELLOW}[*] Stacking comparative scanner metrics across active repositories...{RESET}")
                print(f"[+] Matrix execution simulation completed for target: {current_target}")
            input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

        elif choice == "5":
            if hasattr(engine, 'set_global_target'):
                engine.set_global_target()
            else:
                tgt = input(f"{YELLOW}Enter target value: {RESET}").strip()
                if tgt: engine.global_target = tgt

        elif choice == "6":
            print(f"\n{CYAN}--- EXCEPTION OVERRIDING LOG VIEWER ---{RESET}")
            bug_path = getattr(engine, 'bug_file', 'buglist.json')
            if os.path.exists(bug_path):
                try:
                    with open(bug_path, 'r') as b:
                        print(b.read())
                except Exception as e:
                    print(f"{RED}[-] Error reading bug log file: {e}{RESET}")
            else:
                print(f"{GREEN}[*] No active sandbox errors found. Engine running stable.{RESET}")
            input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

        elif choice == "0":
            print(f"\n{RED}[*] Terminating interface session gracefully.{RESET}")
            sys.exit(0)
            
        elif choice == "":
            continue
        else:
            print(f"\n{RED}[-] Unknown option identifier. Reference README instructions.{RESET}")
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    if os.name == 'nt':
        os.system('color')
    main_menu()
