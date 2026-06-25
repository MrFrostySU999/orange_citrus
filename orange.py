#!/usr/bin/env python3
import os, sys, shutil
from config import PURPLE, YELLOW, WHITE, CYAN, RED, GREEN, RESET, DATABASE
import tools_manager, explorer

def get_system_storage():
    _, _, free = shutil.disk_usage("/")
    return f"{free / (1024**3):.2f} GB"

def main():
    while True:
        os.system('clear')
        print(f"{PURPLE}=====================================================${RESET}")
        print(f"{YELLOW}         🍊 ORANGE PY-CORE ENGINE V5 🍊              {RESET}")
        print(f"{WHITE} Storage Remaining on Device: {CYAN}{get_system_storage()}{RESET}")
        print(f"{PURPLE}=====================================================${RESET}")
        print(f" {YELLOW}1) 🌐 Live Internet Exploit Explorer & Scanner{RESET}")
        
        for key in DATABASE:
            print(f" {GREEN}{int(key)+1}){RESET} {DATABASE[key]['title']} Menu")
            
        print(f" {RED}5) Exit Orange Interface{RESET}")
        print(f"{PURPLE}=====================================================${RESET}")
        
        choice = input("Select category routing [1-5]: ").strip()
        if choice == "1":
            explorer.run_exploit_explorer()
        elif str(int(choice)-1) in DATABASE:
            tools_manager.run_category_menu(str(int(choice)-1))
        elif choice == "5":
            print(f"\n{YELLOW}Terminating Orange core stack. Happy hunting.{RESET}")
            sys.exit(0)

if __name__ == "__main__":
    main()
