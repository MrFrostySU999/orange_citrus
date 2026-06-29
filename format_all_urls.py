file_path = "/root/orange_citrus/vuln_scanner.py"

with open(file_path, "r") as f:
    content = f.read()

# Locate the dynamic git cloning execution block in your file
old_git_block = """                    repo = self.vendor_maps.get(exe, "")
                    if repo:
                        dest = os.path.join(self.install_path, exe)
                        if os.path.exists(dest):
                            shutil.rmtree(dest)
                        
                        # Absolute URL scrubbing mechanism
                        clean_repo = repo.replace("

https://github.com/
", "").replace("://
github.com
", "").replace("
github.com
", "").strip("/")
                        target_url = f"
https://github.com/
{clean_repo}.git"
                        
                        print(f"{CYAN}[*] Fetching raw repository from: {target_url}{RESET}")
                        subprocess.run(["git", "clone", target_url, dest])"""

# Overwrite it with your explicit requested syntax format trailing with a clean .git/ slash pattern
new_git_block = """                    repo = self.vendor_maps.get(exe, "")
                    if repo:
                        dest = os.path.join(self.install_path, exe)
                        if os.path.exists(dest):
                            shutil.rmtree(dest)
                        
                        # Complete scrub to isolate only the raw module repository handle paths
                        clean_repo = repo.replace("
https://github.com/
", "").replace("://
github.com
", "").replace("
github.com
", "").strip("/")
                        
                        # FORCE YOUR EXACT SPECIFIED FORMAT: 
https://github.com/
 + repo + .git/
                        target_url = f"
https://github.com/
{clean_repo}.git/"
                        
                        print(f"{CYAN}[*] Fetching raw repository from: '{target_url}'{RESET}")
                        subprocess.run(["git", "clone", target_url, dest])"""

if old_git_block in content:
    content = content.replace(old_git_block, new_git_block)
    print("[+] Core download matrix locked into the precise layout format.")
else:
    # Sweeping macro injection pattern if line indents differed slightly
    content = content.replace('target_url = f"
https://github.com/
{clean_repo}.git"', 'target_url = f"
https://github.com/
{clean_repo}.git/"')
    print("[+] Fallback string format pattern updated successfully.")

with open(file_path, "w") as f:
    f.write(content)
