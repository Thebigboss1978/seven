# seVen_Engine/Engine/seVen_Execution_Hub.py
# ♠️ The Action Layer for seVen Engine ♠️

import os
import subprocess
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / "Skills"

def run_imperial_command(cmd_key):
    """
    Maps EXE: keywords to actual system scripts.
    Example: EXE:DOCKER_SYNC -> Skills/docker_check.sh
    """
    mapping = {
        "EXE:DOCKER_SYNC": "docker_check.sh",
        "EXE:SYSTEM_RECOVER": "system_recover.sh",
        "EXE:BARCELONA_INGEST": "ingest_all.sh", # I need to create this
        "EXE:VSCODE_INIT": "vscode_init.sh"
    }

    script_name = mapping.get(cmd_key)
    if not script_name:
        return f"⚠️ Warning: Command '{cmd_key}' is recognized but no script is mapped yet."

    script_path = SKILLS_DIR / script_name
    if not script_path.exists():
        return f"⚠️ Error: Script '{script_name}' not found in Skills directory."

    try:
        # Run the script and capture output
        print(f"🚀 EXECUTING: {script_name}")
        result = subprocess.run([str(script_path)], capture_output=True, text=True, shell=True)
        return f"\n[SYSTEM OUTPUT FOR {cmd_key}]:\n{result.stdout}\n{result.stderr}"
    except Exception as e:
        return f"❌ Execution Failed: {str(e)}"

if __name__ == "__main__":
    # Test
    print(run_imperial_command("EXE:DOCKER_SYNC"))
