import os
import sys
import subprocess
import urllib.request
import random # Import modul random
from datetime import date, timedelta, time, datetime # Import modul yang diperlukan

try:
    import progressbar
except ImportError:
    print('[-] Gagal mengimpor progressbar.')
    print('    Silakan jalankan "pip install progressbar2"')
    print('    Pastikan Anda menggunakan Python 3.')
    sys.exit(1)

logo="""
   _______  ______  ____  __  __ ____  _   _
  |__   __||  ____|/ __ \|  \/  |  _ \| \ | |
     | |   | |__  | |  | | \  / | |_) |  \| |
     | |   |  __| | |  | | |\/| |  _ <| . ` |
     | |   | |____| |__| | |  | | |_) | |\  |
     |_|   |______|\____/|_|  |_|____/|_| \_|

"""

def run_command(command, cwd=None, suppress_output=False, env=None):
    """Fungsi pembantu untuk menjalankan perintah shell dengan environment kustom."""
    try:
        full_env = os.environ.copy()
        if env:
            full_env.update(env)

        process_args = {
            'shell': True,
            'check': True,
            'cwd': cwd,
            'text': True,
            'env': full_env
        }
        if suppress_output:
            process_args['stdout'] = subprocess.PIPE
            process_args['stderr'] = subprocess.PIPE

        subprocess.run(command, **process_args)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[-] Error saat menjalankan perintah: {e.cmd}")
        if e.stderr:
            print(f"    Error Standar: {e.stderr.strip()}")
        return False
    except Exception as e:
        print(f"[-] Terjadi kesalahan tak terduga: {e}")
        return False

def main():
    while True:
        os.system('clear')
        print(logo)
        print("\n\t\tDIBUAT & DISEMPURNAKAN OLEH GEMINI!!!")
        print("\n\n1 - Mulai Bot")
        print("2 - Cara Penggunaan")
        print("3 - Keluar")
        inp = input('Pilih OPSI > ')

        if inp == '1':
            try:
                year_to_fill = int(input('Masukkan Tahun yang ingin diisi (misal: 2024): '))
                loop_count = int(input('Berapa kali perulangan tahun? (misal: 3 untuk 3x komit per hari): '))
                if year_to_fill < 1970 or loop_count <= 0:
                    raise ValueError("Tahun atau jumlah perulangan tidak valid.")
            except ValueError as e:
                print(f'[-] Input tidak valid: {e}')
                input('\nTekan Enter untuk melanjutkan...')
                continue

            gu = input('Masukkan URL Repositori Git LENGKAP (https://...): ')
            gn = input('Masukkan Nama Pengguna GitHub Anda: ')
            ge = input('Masukkan E-Mail GitHub Anda: ')

            if not gu.startswith('https://'):
                print('\n[!] URL repositori tidak valid.')
                input('\nTekan Enter untuk melanjutkan...')
                continue

            print("\nPilih branch utama (default: main):")
            branch_name = 'main' if input("1-main, 2-master: ") != '2' else 'master'

            test_dir = 'temp_repo_for_commits'
            print('[+] Membersihkan direktori lama jika ada...')
            run_command(f'rm -rf {test_dir}')
            os.makedirs(test_dir)

            print(f"[+] Kloning {gu} ke direktori temporer...")
            if not run_command(f'git clone {gu} .', cwd=test_dir):
                print("[-] Gagal mengkloning repositori.")
                input('\nTekan Enter untuk melanjutkan...')
                continue

            run_command(f'git config user.name "{gn}"', cwd=test_dir, suppress_output=True)
            run_command(f'git config user.email "{ge}"', cwd=test_dir, suppress_output=True)

            # --- LOGIKA KOMIT YANG DIPERBAIKI ---
            total_commits = 365 * loop_count
            start_date = date(year_to_fill, 1, 1)

            print(f'[+] Memulai {total_commits} komit untuk tahun {year_to_fill} ({loop_count} siklus)...')

            for i in progressbar.progressbar(range(total_commits), redirect_stdout=True):
                # --- INI BAGIAN YANG DIUBAH ---
                # Gunakan modulo untuk memastikan hari kembali ke 0 setelah 364
                day_in_year = i % 365
                commit_date_only = start_date + timedelta(days=day_in_year)
                
                # Tambahkan waktu acak agar timestamp setiap komit unik
                random_time = time(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
                full_commit_datetime = datetime.combine(commit_date_only, random_time)

                # Format tanggal untuk environment variable Git
                date_str = full_commit_datetime.isoformat()
                env_for_commit = {
                    'GIT_AUTHOR_DATE': date_str,
                    'GIT_COMMITTER_DATE': date_str,
                }
                # --- AKHIR BAGIAN YANG DIUBAH ---

                with open(os.path.join(test_dir, 'gemini.log'), 'w') as f:
                    f.write(f"Commit #{i+1}/{total_commits} at {date_str}")

                run_command('git add gemini.log', cwd=test_dir, suppress_output=True)
                
                current_cycle = (i // 365) + 1
                commit_message = f"feat: Commit for {commit_date_only.strftime('%Y-%m-%d')} (Cycle {current_cycle}/{loop_count})"
                run_command(f'git commit -m "{commit_message}"', cwd=test_dir, suppress_output=True, env=env_for_commit)

            print('\n[+] Membersihkan file log...')
            run_command('rm gemini.log', cwd=test_dir, suppress_output=True)
            run_command('git add .', cwd=test_dir, suppress_output=True)
            run_command('git commit -m "chore: clean up log file"', cwd=test_dir, suppress_output=True)

            print(f'[+] Mendorong semua komit ke {gu} pada branch {branch_name}...')
            if not run_command(f'git push -u --force origin {branch_name}', cwd=test_dir):
                print("[-] Gagal melakukan push. Pastikan kredensial benar dan branch ada.")
            else:
                print(f'[+] {total_commits} Komit Selesai... Cek profil GitHub Anda!')
            
            input('\nTekan Enter untuk kembali ke menu utama...')

        elif inp == '2':
            os.system('clear')
            print('                       BANTUAN')
            print('Bot ini akan mengisi kalender kontribusi GitHub Anda dengan komit harian.')
            print('Contoh: Tahun 2024, Perulangan 3 akan membuat 3 komit untuk setiap hari di tahun 2024.')
            print('\nPASTIKAN MENGGUNAKAN REPOSITORI KOSONG ATAU REPOSITORI KHUSUS UNTUK INI!\n')
            input('\nTekan Enter untuk melanjutkan...')
        elif inp == '3':
            break
        else:
            print("Input Tidak Valid!")
            input()

    print('\nTerima Kasih telah menggunakan bot ini!')
    sys.exit(0)

if __name__ == "__main__":
    main()
