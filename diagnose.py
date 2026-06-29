import ast
import os
import sys

def analyze_project():
    report = []
    report.append("=== ORANGE CITRUS DIAGNOSTIC REPORT ===")
    
    # 1. Check Python Version and Files
    report.append(f"Python Version: {sys.version}")
    files = [f for f in os.listdir('.') if f.endswith('.py')]
    report.append(f"Found Python files: {files}\n")

    # 2. Extract methods called in orange.py
    orange_calls = set()
    if os.path.exists('orange.py'):
        try:
            with open('orange.py', 'r') as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == 'engine':
                        orange_calls.add(node.func.attr)
            report.append(f"Methods orange.py tries to call on 'engine':\n  {list(orange_calls)}\n")
        except Exception as e:
            report.append(f"Error parsing orange.py: {e}\n")

    # 3. Extract actual methods defined in other files
    for filename in files:
        if filename == 'orange.py' or filename == 'diagnose.py':
            continue
        try:
            with open(filename, 'r') as f:
                tree = ast.parse(f.read())
            
            report.append(f"--- File: {filename} ---")
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    report.append(f"Class found: {node.name}")
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    report.append(f"  Defined methods: {methods}")
            report.append("")
        except Exception as e:
            report.append(f"Error parsing {filename}: {e}\n")

    # Write out the report
    with open('diagnostic_report.txt', 'w') as f:
        f.write("\n".join(report))
    print("\n[+] Diagnostics complete! Report saved to: /root/orange_citrus/diagnostic_report.txt")

if __name__ == "__main__":
    analyze_project()
