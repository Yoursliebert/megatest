#!/usr/bin/env python3
import os
import sys
import asyncio
from asyncio.subprocess import PIPE
from subprocess import CalledProcessError
from colorama import init, Fore, Style
import pyfiglet
from halo import Halo

init(autoreset=True)

def display_header():
    ascii_banner = pyfiglet.figlet_format("YANTA YAGXAAA")
    border = "=" * 80
    print(Style.BRIGHT + Fore.CYAN + border)
    print(Style.BRIGHT + Fore.YELLOW + ascii_banner)
    print(Style.BRIGHT + Fore.MAGENTA + "AUTO TX MEGAETH".center(80))
    print(Style.BRIGHT + Fore.CYAN + border + "\n")
    print(Style.BRIGHT + Fore.CYAN + "======================================")
    print(Style.BRIGHT + Fore.CYAN + "         AUTO SWAP TESTING            ")
    print(Style.BRIGHT + Fore.CYAN + "====================================\n")

module_folder = "./modules"
if not os.path.isdir(module_folder):
    print(Fore.RED + f"Folder '{module_folder}' tidak ditemukan!")
    sys.exit(1)

module_files = [f for f in os.listdir(module_folder) if f.endswith(".py")]
scripts = [{"name": os.path.splitext(f)[0].title(), "path": os.path.join(module_folder, f)} for f in module_files]

async def run_script(script):
    print(Fore.YELLOW + f"\n📜 Menjalankan: {script['name']}...")
    cmd = [sys.executable, script["path"]]

    spinner = Halo(text='Sedang mengeksekusi...', spinner='dots', color='cyan')
    spinner.start()
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = await proc.communicate()
    spinner.stop()

    if stdout:
        print(Fore.WHITE + stdout.decode())
    if stderr:
        print(Fore.RED + "Error: " + stderr.decode())

    if proc.returncode == 0:
        print(Fore.GREEN + f"✅ Berhasil: {script['name']}")
    else:
        print(Fore.RED + f"❌ Gagal: {script['name']} (Kode keluar: {proc.returncode})")
        raise CalledProcessError(proc.returncode, cmd)

async def run_scripts_per_account(accounts, loop_count, selected_scripts):
    for account_index, private_key in enumerate(accounts):
        os.environ["PRIVATE_KEY"] = private_key
        print(Fore.CYAN + f"\n🔐 Akun {account_index+1}: {private_key[:10]}...")

        for i in range(loop_count):
            print(Fore.BLUE + f"🔁 Loop {i + 1} dari {loop_count} untuk akun {account_index+1}")
            for script in selected_scripts:
                try:
                    await run_script(script)
                except Exception:
                    print(Fore.RED + f"⚠️ Melewati {script['name']} karena error")

async def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    display_header()

    # Load akun dari accounts.txt
    if not os.path.exists("accounts.txt"):
        print(Fore.RED + "File 'accounts.txt' tidak ditemukan.")
        sys.exit(1)
    with open("accounts.txt", "r") as f:
        accounts = [line.strip() for line in f if line.strip()]

    print(Fore.BLUE + Style.BRIGHT + "\n🚀 Jalankan Modul Auto\n")
    print(Fore.CYAN + "-" * 80)
    print("Pilih modul yang ingin dijalankan (misal: 1,2,3). Kosong = semua modul.\n")
    for idx, script in enumerate(scripts, start=1):
        print(f"{Fore.YELLOW}{idx}. {Fore.WHITE}{script['name']}")
    print(Fore.CYAN + "-" * 80)

    selection = input(Fore.CYAN + "\nMasukkan nomor modul (default semua): ").strip()
    if selection == "":
        selected_modules = scripts
    else:
        try:
            indices = [int(x.strip()) for x in selection.split(",") if x.strip().isdigit()]
            selected_modules = [scripts[i - 1] for i in indices if 1 <= i <= len(scripts)]
            if not selected_modules:
                selected_modules = scripts
        except Exception:
            selected_modules = scripts

    loop_count_str = input(Fore.CYAN + "\nBerapa kali ingin menjalankan per akun? (default 1): ").strip()
    try:
        loop_count = int(loop_count_str) if loop_count_str else 1
        if loop_count <= 0:
            print(Fore.RED + "Angka harus lebih dari 0. Gunakan default 1.")
            loop_count = 1
    except:
        loop_count = 1

    print(Fore.GREEN + f"\n🚀 Memulai {len(selected_modules)} modul × {loop_count} loop per {len(accounts)} akun\n")
    await run_scripts_per_account(accounts, loop_count, selected_modules)

    print(Fore.GREEN + Style.BRIGHT + "\n✅✅ Semua akun & modul selesai dijalankan! ✅✅\n")
    print(Fore.MAGENTA + "*" * 80)
    print(Fore.MAGENTA + "Terima kasih telah menggunakan script ini!".center(80))
    print(Fore.MAGENTA + "*" * 80 + "\n")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram dihentikan oleh user.")
        sys.exit(0)
