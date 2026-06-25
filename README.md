# 🍊 Orange-Citrus Framework (v5.5.0-Stable)

![Platform](https://shields.io)
![Python](https://shields.io)
![License](https://shields.io)

> **A Plethora of Tools:** An advanced, modular penetration testing automation framework designed specifically for mobile and restricted terminal environments like Termux.

Orange-Citrus acts as a central command dashboard that provides live threat intelligence, automates multi-engine scanning, handles dynamic penetration tool installation routes, and resolves system-level runtime exceptions automatically through a built-in AI auto-healing core.

---

## ⚡ One-Line Automated Installation

Deploy the complete Orange-Citrus framework instantly on any new Termux instance using this single command:

```bash
mkdir -p ~/orange_v1 && cd ~/orange_v1 && curl -sLO https://githubusercontent.com && curl -sLO https://githubusercontent.com && chmod +x orange.py && python3 orange.py
```

---

## 🎯 Key Features & Modules

### 1. Dynamic Pre-Flight Dependency Guard
Never suffer a `ModuleNotFoundError` again. Before *any* tool is allowed to launch, the engine dynamically crawls and reads its `requirements.txt` file. If any unlisted libraries (such as `tomli`, `pandas`, or `ujson`) are missing, it summarizes them and prompts you before downloading them globally via `pip`.

### 2. Cross-Tool Audit & Comparison Matrix
Enables side-by-side comparative analysis across separate scanner nodes. Input a target domain to tabulate parallel intelligence metrics simultaneously—stacking open port network discovery data alongside path fuzzing and vulnerability indexes.

### 3. AI Self-Healing Core & Fault Tolerant Sandbox
If a pentest tool crashes or rejects an argument (like `exit status 1` or `2`), the error interceptor captures the stack trace. It identifies the root issue, patches the code formatting, or drops the tool into a clean, isolated **Sandbox Overriding Environment** to ensure your main menu session never freezes.

### 4. Background GitHub Auto-Sync Matrix
The workspace features a non-blocking background connection framework. Every time you download a tool, purge files, or capture a critical runtime bug, the engine automatically runs `git add`, `git commit`, and `git push --force` straight to your online repository using your verified local key mappings.

---

## 🛠️ Integrated Tool Suite

The core and expansion repositories are dynamically mapped and routed cleanly into separate categories under `~/orange_tools/`:

| Option | Tool Target | Operational Category Profile | Installation Method |
| :---: | :--- | :--- | :--- |
| **1** | **Recon-ng** | Information Gathering & OSINT | Local / SSH Key Sync |
| **2** | **Nikto** | Web Vulnerability Scanning | Local / SSH Key Sync |
| **3** | **Sublist3r** | Subdomain Brute-Forcing | Local / SSH Key Sync |
| **4** | **WPScan** | CMS & WordPress Auditing | Local / SSH Key Sync |
| **5** | **Nmap** | Port Scanning & Discovery | Local / SSH Key Sync |
| **+** | **theHarvester** | Advanced Public Data Harvesting | Online Expansion Feed |
| **+** | **Sqlmap** | Automated SQL Injection Testing | Online Expansion Feed |
| **+** | **Amass** | External Asset Mapping & Discovery | Online Expansion Feed |
| **+** | **Dirsearch** | Web Directory Brute-Forcing | Online Expansion Feed |
| **+** | **Sherlock** | Username Intelligence Tracking | Online Expansion Feed |

---

## 🕹️ How to Use

Run the master script interface:
```bash
python3 orange.py
```

### Navigating the Control Boards:
*   **Menu `[1]` (Core Categories)**: View installation statuses, fetch fresh patches, or download the baseline auditing utilities.
*   **Menu `[2]` (Expansion Catalogue)**: Scan the internet utility feed for expansion tool upgrades.
*   **Menu `[3]` (Live Exploit Lookup)**: Queries real-time vulnerability indices on the fly based on a system keyword (e.g., `android`, `nginx`).
*   **Menu `[4]` (Comparison Matrix)**: Stacks and simulates multi-scanner audit responses for comprehensive data mapping.
*   **Menu `[5]` (Launch Terminal)**: Fires up your deployed applications natively.
*   **Menu `[6]` (Buglist Viewer)**: Inspects logs, time metrics, and exception summaries captured by the AI interceptor.
*   **Option `[0]`**: Safely takes you one level backward or terminates your interface session gracefully.

---

## ⚠️ Requirements & Troubleshooting

If you encounter system compilation issues inside Termux during heavy data analytics operations (like installing `pandas`), clean up your environments using this standard sequence:

```bash
pkg install clang python-numpy python-scipy -y
python3 -m pip install pandas --prefer-binary
```

---
*Maintained and automated by **MrFrostySU999**. Always use this software responsibly and within authorized audit scopes.*
