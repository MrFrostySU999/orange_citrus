# =====================================================
# ORANGE_CITRUS CONFIGURATION MODULE
# Contains ANSI color constants and master tool mapping.
# =====================================================

ORANGE = '\033[38;5;208m'
RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
WHITE = '\033[97m'
RESET = '\033[0m'

DATABASE = {
    1: {
        "title": "Information Gathering & OSINT",
        "color": CYAN,
        "tools": {
            "1": {
                "type": "git", 
                "name": "Recon-ng", 
                "path": "git@github.com:lanmaster53/recon-ng.git", 
                "dir": "recon-ng", 
                "pkg": "recon-ng", 
                "size": "4.2 MB", 
                "desc": "Powerful web-based open source intelligence framework.", 
                "syntax": "recon-ng"
            },
            "2": {
                "type": "git", 
                "name": "theHarvester", 
                "path": "git@github.com:laramies/theHarvester.git", 
                "dir": "theHarvester", 
                "pkg": "theharvester", 
                "size": "2.1 MB", 
                "desc": "Gathers emails, subdomains, hosts, employee names, and open ports.", 
                "syntax": "theHarvester -d target.com -l 500 -b google"
            },
            "3": {
                "type": "apt", 
                "name": "Nmap Scanner", 
                "pkg": "nmap", 
                "size": "26.4 MB", 
                "desc": "Network exploration tool and security / port scanner.", 
                "syntax": "nmap -sV -sC -T4 target.com"
            }
        }
    },
    2: {
        "title": "Web Vulnerability Scanning",
        "color": ORANGE,
        "tools": {
            "1": {
                "type": "git", 
                "name": "Sqlmap", 
                "path": "git@github.com:sqlmapproject/sqlmap.git", 
                "dir": "sqlmap", 
                "pkg": "sqlmap", 
                "size": "28.5 MB", 
                "desc": "Automatic SQL injection and database takeover tool.", 
                "syntax": "sqlmap -u 'http://target.com' --dbs"
            },
            "2": {
                "type": "apt", 
                "name": "Nikto Web", 
                "pkg": "nikto", 
                "size": "4.5 MB", 
                "desc": "Web server assessment tool for dangerous files and outdated software.", 
                "syntax": "nikto -h target.com"
            }
        }
    }
}
