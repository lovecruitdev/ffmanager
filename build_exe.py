import os
import subprocess
import sys
import shutil


def build():
    print("[*] Starting FFlag Manager build with Nuitka...")

    # 1. Clean previous build output
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            print(f"[*] Removing old {folder} folder...")
            shutil.rmtree(folder, ignore_errors=True)

    # 2. Ensure Nuitka is installed
    try:
        import nuitka
    except ImportError:
        print("[!] Nuitka not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nuitka", "zstandard"])

    # 4. Define paths
    script_path = "main.pyw"
    icon_file = "ffm_v3_logo.ico"
    
    # 5. Nuitka build command
    # --standalone: packages all DLLs and dependencies
    # --windows-disable-console: makes it a windowed app
    # --windows-icon-from-ico: sets the executable icon
    # --include-data-dir / --include-data-files: bundle assets
    # --assume-yes-for-downloads: auto-downloads gcc/mingw compiler if missing
    # --output-filename=FFM.exe: names the binary FFM.exe
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--windows-disable-console",
        f"--windows-icon-from-ico={icon_file}",
        "--include-data-dir=src/gui/ui=src/gui/ui",
        "--include-data-files=version.json=version.json",
        "--include-data-dir=src/data=src/data",
        "--assume-yes-for-downloads",
        "--output-filename=FFM.exe",
        "--output-dir=dist",
        script_path
    ]

    print(f"[*] Executing Nuitka: {' '.join(cmd)}")
    subprocess.check_call(cmd)

    # Nuitka standalone puts the output in dist/main.dist
    # Rename it to dist/FFM to keep installer/installer.iss configs happy
    main_dist_dir = os.path.join("dist", "main.dist")
    ffm_dir = os.path.join("dist", "FFM")
    
    if os.path.exists(main_dist_dir):
        if os.path.exists(ffm_dir):
            shutil.rmtree(ffm_dir)
        os.rename(main_dist_dir, ffm_dir)
        print(f"[+] Renamed build folder to {ffm_dir}")
    else:
        print("[!] Warning: dist/main.dist was not found, checking if dist/FFM already exists...")

    print("\n[+] Nuitka Build Complete!")
    print(f"[+] Application folder: {os.path.abspath('dist/FFM')}")
    print("[+] EXE path: dist/FFM/FFM.exe")


if __name__ == "__main__":
    build()
