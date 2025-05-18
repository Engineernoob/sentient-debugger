import subprocess
import os

def analyze_file(filepath: str):
    try:
        print(f"[STATIC] Analyzing {filepath}...")
        result = subprocess.run(
            ["./target/debug/tree_sitter_parser", filepath],
            cwd="static_analysis",
            capture_output=True,
            text=True
        )
        print(f"[STATIC] Output:\n{result.stdout}")
    except Exception as e:
        print(f"[ERROR] Static analysis failed: {e}")
