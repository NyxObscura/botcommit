import os
import sys
import subprocess
import urllib.request
from datetime import date, timedelta, datetime # Import modul yang diperlukan untuk tanggal

try:
    import progressbar
except ImportError:
    print('[-] Gagal mengimpor progressbar.')
    print('    Silakan jalankan "pip install progressbar2"')
    print('    Pastikan Anda menggunakan Python 3.')
    sys.exit(1)

# Logo yang lebih generik
logo="""
   _______  ______  ____  __  __ ____  _   _
  |__   __||  ____|/ __ \|  \/  |  _ \| \ | |
     | |   | |__  | |  | | \  / | |_) |  \| |
     | |   |  __| | |  | | |\/| |  _ <| . ` |
     | |   | |____| |__| | |  | | |_) | |\  |
     |_|   |______|\____/|_|  |_|____/|_| \_|

"""

def run_command(command, cwd=None, suppress_output=False, return_output=False, env=None):
    """
    Fungsi pembantu untuk menjalankan perintah shell.
    Ditambahkan parameter 'env' untuk mengatur tanggal komit.
    """
    try:
        # Gabungkan environment sistem dengan environment kustom jika ada
        full_env = os.environ.copy()
        if env:
            full_env.update(env)

        if suppress_output:
            process = subprocess.run(command, shell=True, check=True, cwd=cwd,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=full_env)
        else:
            process = subprocess.run(command, shell=True, check=True, cwd=cwd, text=True, env=full_env)

        if return_output:
            return process.stdout.strip()
        return True
    except subprocess.CalledProcessError as e:
        print(f"[-] Error saat menjalankan perintah: {e.cmd}")
        print(f"    Kode Keluar: {e.returncode}")
        if e.stdout:
            print(f"    Output Standar: {e.stdout.strip()}")
        if e.stderr:
            print(f"    Error Standar: {e.stderr.strip()}")
        return False
    except FileNotFoundError:
        print(f"[-] Perintah tidak ditemukan. Pastikan Git terinstal dan ada di PATH.")
        return False
    except Exception as e:
        print(f"[-] Terjadi kesalahan tak terduga: {e}")
        return False

def check_internet_connection():
    """Mengecek koneksi internet."""
    try:
        urllib.request.urlopen('https://www.google.com', timeout=5)
        return True
    except urllib.error.URLError:
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
            if not check_internet_connection():
                print('[-] Anda tidak terhubung ke internet!!!')
                input('\nTekan Enter untuk melanjutkan...')
                continue

            try:
                # --- INPUT BARU ---
                year_to_fill = int(input('Masukkan Tahun yang ingin diisi (misal: 2023): '))
                loop_count = int(input('Berapa kali perulangan tahun? (misal: 1 untuk 1 tahun penuh): '))
                if year_to_fill < 1970 or loop_count <= 0:
                    raise ValueError("Tahun atau jumlah perulangan tidak valid.")
            except ValueError as e:
                print(f'[-] Input tidak valid. Harap masukkan angka yang benar. {e}')
                input('\nTekan Enter untuk melanjutkan...')
                continue

            gu = input('Masukkan URL Repositori Git LENGKAP (termasuk https://): ')
            gn = input('Masukkan Nama Pengguna GitHub Anda: ')
            ge = input('Masukkan E-Mail GitHub Anda: ')

            if not gu.startswith('https://'):
                print('\n\n[!] SELALU masukkan URL repositori LENGKAP.')
                input('\nTekan Enter untuk melanjutkan...')
                continue
            if gu.endswith('.git'):
                gu = gu[:-4]

            # Cek validitas URL (opsional, bisa diskip jika yakin)
            try:
                req = urllib.request.Request(gu, method='HEAD')
                urllib.request.urlopen(req, timeout=5)
            except Exception as e:
                print(f'[!] URL Repositori Salah atau tidak dapat diakses: {e}')
                input('\nTekan Enter untuk melanjutkan...')
                continue

            print("\nPilih branch utama repositori Anda:")
            branch_name = 'main' if input("1-main, 2-master (default: main): ") != '2' else 'master'

            print('[+] Menginisialisasi....')
            test_dir = 'temp_repo_for_commits'
            if os.path.exists(test_dir):
                print(f'[+] Direktori "{test_dir}" ditemukan. Membersihkan...')
                run_command(f'rm -rf {test_dir}')
            
            os.makedirs(test_dir)

            print(f"[+] Kloning {gu} ke direktori temporer...")
            if not run_command(f'git clone {gu} .', cwd=test_dir):
                print("[-] Gagal mengkloning repositori.")
                input('\nTekan Enter untuk melanjutkan...')
                continue
            
            print('[+] Repositori Berhasil Ditarik dan Dipersiapkan.')

            readme_path = os.path.join(test_dir, 'README.md')
            with open(readme_path, 'a') as f:
                f.write("\n\n*Commits generated by Gemini's Commit Bot.*")

            run_command(f'git config user.name "{gn}"', cwd=test_dir, suppress_output=True)
            run_command(f'git config user.email "{ge}"', cwd=test_dir, suppress_output=True)
            
            # --- LOGIKA KOMIT BARU ---
            total_days = 365 * loop_count
            start_date = date(year_to_fill, 1, 1)
            
            print(f'[+] Memulai {total_days} komit dari {start_date.year} selama {loop_count} tahun...')

            for i in progressbar.progressbar(range(total_days), redirect_stdout=True):
                commit_date = start_date + timedelta(days=i)
                
                # Format tanggal agar sesuai dengan yang dibutuhkan Git
                # Ini adalah bagian terpenting untuk memalsukan tanggal
                date_str = f"{commit_date.isoformat()} 12:00:00"
                env_for_commit = {
                    'GIT_AUTHOR_DATE': date_str,
                    'GIT_COMMITTER_DATE': date_str,
                }

                # Membuat atau menimpa file untuk setiap komit
                with open(os.path.join(test_dir, 'gemini.log'), 'w') as f:
                    f.write(f"Commit for {commit_date.strftime('%Y-%m-%d')}")

                run_command('git add .', cwd=test_dir, suppress_output=True)
                
                # Jalankan komit dengan environment tanggal yang sudah diatur
                commit_message = f"feat: Gemini daily commit for {commit_date.strftime('%Y-%m-%d')}"
                run_command(f'git commit -m "{commit_message}"', cwd=test_dir, suppress_output=True, env=env_for_commit)

            print('\n[+] Membersihkan file log...')
            run_command('rm gemini.log', cwd=test_dir, suppress_output=True)
            run_command('git add .', cwd=test_dir, suppress_output=True)
            run_command('git commit -m "chore: clean up log file"', cwd=test_dir, suppress_output=True)

            print(f'[+] Mendorong semua komit ke {gu} pada branch {branch_name}...')
            # --force diperlukan karena kita menulis ulang histori dengan tanggal palsu
            if not run_command(f'git push -u --force origin {branch_name}', cwd=test_dir):
                print("[-] Gagal melakukan push. Pastikan Anda memiliki kredensial Git yang benar.")
            else:
                print(f'[+] {total_days} Komit Selesai... \n\t\tAnda akan melihatnya di Kontribusi Anda segera.')
            
            print('[+] Menutup Bot....')
            break

        elif inp == '2':
            os.system('clear')
            print('                       BANTUAN')
            print('           -----------------------------')
            print(logo+'\n')
            print('Bot ini akan mengisi kalender kontribusi GitHub Anda dengan komit harian.')
            print('Anda akan diminta memasukkan TAHUN dan JUMLAH PERULANGAN.')
            print('Contoh: Tahun 2023, Perulangan 1 akan membuat 365 komit, satu untuk setiap hari di tahun 2023.')
            print('\nPASTIKAN MENGGUNAKAN REPOSITORI KOSONG ATAU REPOSITORI KHUSUS UNTUK INI!\n')
            print('Input yang Diperlukan:\n')
            print('\t Tahun              -   Tahun awal untuk memulai komit harian (misal: 2023)')
            print('\t Jumlah Perulangan  -   Berapa tahun penuh yang ingin diisi (misal: 2 untuk 2 tahun)')
            print('\t URL Repositori     -   URL repositori target Anda (misal: https://github.com/user/repo)')
            print('\t Nama Pengguna & Email  -   Untuk identitas komit Anda.')
            print('\nBot ini menggunakan --force push, yang akan menimpa histori di branch target.')
            input('\nTekan Enter untuk melanjutkan...')
        elif inp == '3':
            break
        else:
            print("Input Tidak Valid !!!\nTekan Lagi!!!")
            input()

    print(logo)
    print('\nTerima Kasih telah menggunakan Proyek saya!')
    sys.exit(0)

if __name__ == "__main__":
    main()
