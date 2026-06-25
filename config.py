RED = '\033[1;31m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[1;34m'
PURPLE = '\033[1;35m'
CYAN = '\033[1;36m'
WHITE = '\033[1;37m'
RESET = '\033[0m'

DATABASE = {
    "1": {
        "title": "Information Gathering",
        "color": BLUE,
        "tools": {
            "1": {"name": "Nmap Scanner", "pkg": "nmap", "size": "5.5 MB", "desc": "Network map scanning and port auditing.", "syntax": "nmap -sT -v target-ip"},
            "2": {"name": "DMitry Recon", "pkg": "dmitry", "size": "150 KB", "desc": "Information Gathering software for subdomains.", "syntax": "dmitry -wnpb target.com"}
        }
    },
    "2": {
        "title": "Vulnerability Analysis",
        "color": CYAN,
        "tools": {
            "1": {"name": "Sqlmap Engine", "pkg": "sqlmap", "size": "7.8 MB", "desc": "Automated SQL injection mapping framework.", "syntax": "sqlmap -u 'url?id=1' --dbs"}
        }
    },
    "3": {
        "title": "Password Exploits",
        "color": GREEN,
        "tools": {
            "1": {"name": "Hydra Cracker", "pkg": "hydra", "size": "1.1 MB", "desc": "Parallelized login credential brute-forcer.", "syntax": "hydra -l user -P passes.txt ssh://target"}
        }
    }
}
