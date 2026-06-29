file_path = "/root/orange_citrus/vuln_scanner.py"
with open(file_path, "r") as f:
    content = f.read()

# Locate the broken attribute call and replace it with direct inline string logic rules
old_broken_line = "target_url = self.auto_url_validation_scanner(target_url)"

new_inline_logic = """# Inline Pre-Scan URL Interceptor Injection Wrapper
                    scrub_str = target_url.replace("https://", "").replace("http://", "")
                    scrub_str = scrub_str.replace("://", "").replace("github.com", "")
                    clean_repo_path = scrub_str.replace(".git/", "").replace(".git", "").strip("/")
                    # Force strict pattern format enforcement matching rules
                    target_url = f"https://github.com{clean_repo_path}.git/\""""

if old_broken_line in content:
    content = content.replace(old_broken_line, new_inline_logic)
    print("[+] Part 1: Inline URL validation scanner logic injected successfully.")
else:
    print("[-] Part 1: Targeted broken source attribute string line not found.")

with open(file_path, "w") as f:
    f.write(content)
