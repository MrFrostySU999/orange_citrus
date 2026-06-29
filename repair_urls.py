import re

file_path = "/root/orange_citrus/vuln_scanner.py"

with open(file_path, "r") as f:
    content = f.read()

# 1. Clean up the vendor maps so they are pure repository handles without broken prefixes
content = content.replace("https://github.com/owasp-amass/amass", "owasp-amass/amass")
content = content.replace("
https://github.com/
", "")
content = content.replace("://
github.com
", "")

# 2. Rewrite the precise git clone command to structure the URL perfectly
old_git_line = 'subprocess.run(["git", "clone", f"
https://github.com/
{repo}", os.path.join(self.install_path, name.lower())])'
new_git_line = 'subprocess.run(["git", "clone", f"
https://github.com/
{repo}.git", os.path.join(self.install_path, name.lower())])'

# If the old line variant with .git is present, normalize it
if "f\"
https://github.com/
{repo}\"" in content:
    content = content.replace(old_git_line, new_git_line)

# Fallback sweeping replacement to force absolute structural alignment
content = re.sub(
    r'subprocess\.run\(\["git", "clone", f"https.*?\]\)',
    'subprocess.run(["git", "clone", f"
https://github.com/
{repo}.git", os.path.join(self.install_path, name.lower())])',
    content
)

with open(file_path, "w") as f:
    f.write(content)

print("[+] URL logic structure harmonized successfully.")
