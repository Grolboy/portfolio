import os
import subprocess
import sys

def run(command):
    print(f"Running: {command}")
    subprocess.check_call(command, shell=True)

def main():
    # Change venv_dir to point to the API folder
    api_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    venv_dir = os.path.join(api_dir, "venv")

    # Step 1: Create virtual environment
    if not os.path.exists(venv_dir):
        run(f"{sys.executable} -m venv {venv_dir}")
        print("✅ Virtual environment created.")
    else:
        print("ℹ️ Virtual environment already exists.")

    # Step 2: Install requirements
    pip_executable = os.path.join(venv_dir, "Scripts", "pip") if os.name == "nt" else os.path.join(venv_dir, "bin", "pip")

    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found.")
        return

    run(f"{pip_executable} install -r requirements.txt")
    print("✅ Dependencies installed.")

    # Step 3: Activation instructions (cannot auto-activate from script)
    print("\nℹ️ To activate the virtual environment, run:")
    if os.name == "nt":
        print(rf"{venv_dir}\Scripts\activate")
    else:
        print(f"source {venv_dir}/bin/activate")

if __name__ == "__main__":
    main()
