import os
import sys
import subprocess # Menggunakan subprocess untuk perintah shell
import urllib.request # Untuk Python 3

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

def run_command(command, cwd=None, suppress_output=False):
    """Fungsi pembantu untuk menjalankan perintah shell."""
    try:
        if suppress_output:
            result = subprocess.run(command, shell=True, check=True, cwd=cwd,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            result = subprocess.run(command, shell=True, check=True, cwd=cwd, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[-] Error saat menjalankan perintah: {e}")
        if not suppress_output:
            print(f"    Output: {e.stdout}")
            print(f"    Error: {e.stderr}")
        return None
    except FileNotFoundError:
        print(f"[-] Perintah tidak ditemukan. Pastikan Git terinstal dan ada di PATH.")
        return None

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
        print("\n\t\tDIBUAT OLEH GEMINI!!!")
        print("\n\n1 - Mulai Bot")
        print("2 - Cara Penggunaan")
        print("3 - Keluar")
        inp = input('Pilih OPSI > ')

        if inp == '1':
            if not check_internet_connection():
                print('[-] Anda tidak terhubung ke internet!!!')
                print('    Harap sambungkan ke internet untuk melanjutkan....')
                input('\nTekan Enter untuk melanjutkan...')
                continue

            try:
                nc = int(input('Masukkan Jumlah Komit yang Ingin Dilakukan: '))
            except ValueError:
                print('[-] Input jumlah komit tidak valid. Harap masukkan angka.')
                input('\nTekan Enter untuk melanjutkan...')
                continue

            gu = input('Masukkan URL Repositori Git LENGKAP (termasuk https://): ')
            gn = input('Masukkan Nama Pengguna GitHub Anda: ')
            ge = input('Masukkan E-Mail GitHub Anda: ')

            if nc <= 0:
                print('[!] Error: Harap masukkan jumlah komit lebih dari 0.')
                input('Tekan Enter untuk melanjutkan...')
                continue
            if not gu.startswith('https://'):
                print('\n\n[!] SELALU masukkan URL repositori LENGKAP.')
                print('\tContoh: https://github.com/yourusername/your-repo')
                input('\nTekan Enter untuk melanjutkan...')
                continue
            if gu.endswith('.git'):
                gu = gu[0:len(gu)-4]

            # Cek validitas URL GitHub (sederhana)
            try:
                if not urllib.request.urlopen(gu).getcode() == 200:
                    print('[!] URL Repositori Salah atau tidak dapat diakses!!!')
                    print('\n\n[!] SELALU masukkan URL repositori LENGKAP.')
                    print('\tContoh: https://github.com/yourusername/your-repo\n')
                    input('\nTekan Enter untuk melanjutkan...')
                    continue
            except urllib.error.URLError as e:
                print(f'[!] URL Repositori Salah atau tidak dapat diakses: {e}')
                print('\n\n[!] SELALU masukkan URL repositori LENGKAP.')
                print('\tContoh: https://github.com/yourusername/your-repo\n')
                input('\nTekan Enter untuk melanjutkan...')
                continue


            # Opsi pemilihan branch
            print("\nPilih branch utama repositori Anda:")
            print("1 - main")
            print("2 - master")
            branch_choice = input("Masukkan pilihan Anda (1/2): ")
            if branch_choice == '1':
                branch_name = 'main'
            elif branch_choice == '2':
                branch_name = 'master'
            else:
                print("[-] Pilihan branch tidak valid. Menggunakan 'main' secara default.")
                branch_name = 'main'


            print('[+] Menginisialisasi....')
            test_dir = 'temp_repo_for_commits' # Nama direktori yang lebih jelas

            if os.path.exists(test_dir):
                print(f'[+] Direktori "{test_dir}" ditemukan. Membersihkan...')
                run_command(f'rm -rf {test_dir}/*', suppress_output=True)
            else:
                print(f'[+] Direktori "{test_dir}" tidak ditemukan. Membuat satu....')
                os.makedirs(test_dir)

            print('[+] Menyiapkan Direktori...')
            print('[+] Menarik Repositori Jauh ke Direktori Lokal...')

            clone_success = run_command(f'git clone {gu} {test_dir}', suppress_output=False)
            if clone_success is None:
                print("[-] Gagal mengkloning repositori. Pastikan URL benar dan Anda memiliki izin.")
                input('\nTekan Enter untuk melanjutkan...')
                continue

            # Karena sudah clone langsung ke test_dir, tidak perlu mv lagi
            # run_command(f'mv -f {test_dir}/{rn}/* {test_dir}', suppress_output=True)
            # run_command(f'mv -f {test_dir}/{rn}/.??* {test_dir}', suppress_output=True)
            # run_command(f'rm -rf {test_dir}/{rn}', suppress_output=True)

            print('[+] Repositori Berhasil Ditarik.')

            # Tambahkan informasi Gemini ke README.md jika belum ada
            readme_path = os.path.join(test_dir, 'README.md')
            if not os.path.exists(readme_path):
                open(readme_path, 'a').close() # Buat file jika tidak ada

            with open(readme_path, 'r+') as f:
                content = f.read()
                # Hindari duplikasi jika sudah ada
                if "This Repo Was Commited By Gemini's Commit Bot" not in content:
                    f.seek(0, 0) # Kembali ke awal file
                    f.write("# This Repo Was Commited By Gemini's Commit Bot\n")
                    f.write("## GitHub Link to Gemini's Commit Bot\n")
                    f.write("<a href='https://github.com/google-gemini/commit-bot-example'> Click Here </a>\n\n") # Placeholder
                    f.write(content) # Tambahkan konten lama setelah header
                else:
                    print("[!] Informasi Gemini sudah ada di README.md.")


            # Konfigurasi Git
            run_command(f'git config user.name "{gn}"', cwd=test_dir, suppress_output=True)
            run_command(f'git config user.email "{ge}"', cwd=test_dir, suppress_output=True)
            run_command('git add .', cwd=test_dir, suppress_output=True)
            print('[+] Direktori Diinisialisasi.')

            print('[+] Memulai Komit untuk Mendapatkan Kontribusi...')
            for i in progressbar.progressbar(range(nc), redirect_stdout=True): # nc-1 menjadi nc
                temp_file_path = os.path.join(test_dir, 'gemini_commit_trace.txt')
                with open(temp_file_path, 'a') as f:
                    f.write(f"Commit oleh Gemini Bot pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

                run_command('git add .', cwd=test_dir, suppress_output=True)
                run_command(f'git commit -m "Commit oleh Gemini Bot!!! {i+1}/{nc}"', cwd=test_dir, suppress_output=True)
                # Tambahkan delay kecil jika perlu untuk menghindari "too fast" issues
                # import time
                # time.sleep(0.1)

            print('\n[+] Membersihkan Repositori...')
            # run_command(f'rm {test_dir}/gemini_commit_trace.txt', suppress_output=True)
            # Karena file ini akan berubah setiap commit, biarkan saja. Atau hapus kalau tidak mau terlihat.
            # Jika ingin menghapus, pastikan untuk menghapus file terakhir yang dibuat setelah loop selesai
            # Misalnya: run_command(f'rm {test_dir}/gemini_commit_trace.txt', suppress_output=True)
            # Jika tidak, biarkan saja sebagai jejak commit.

            run_command('git gc', cwd=test_dir, suppress_output=True)
            print('[+] Repositori Dibersihkan.')

            print('[-] Komit Terakhir...')
            run_command('git add .', cwd=test_dir, suppress_output=True)
            run_command(f'git commit -m "Final Commit oleh Gemini Bot!!!"', cwd=test_dir, suppress_output=True)

            print(f'[+] Mendorong Repo ke URL Remote: {gu} pada branch {branch_name}')
            push_success = run_command(f'git push -u --force origin {branch_name}', cwd=test_dir, suppress_output=False)

            if push_success is None:
                print("[-] Gagal melakukan push. Pastikan Anda memiliki kredensial Git yang benar.")
                print("    Anda mungkin perlu melakukan autentikasi.")
            else:
                print(f'[+] {nc} Komit Selesai... \n\t\tAnda akan melihatnya di Kontribusi Anda segera.')
            print('[+] Menutup Bot....')
            break

        elif inp == '2':
            os.system('clear')
            print('                       BANTUAN')
            print('           -----------------------------')
            print(logo+'\n')
            print('Ini adalah BOT KOMIT yang Dibuat oleh Gemini untuk mendapatkan KONTRIBUSI SECARA GRATIS...')
            print('Skrip ini menghasilkan Komit Palsu dan sangat Cepat....')
            print('\nSELALU GUNAKAN REPOSITORI KOSONG DENGAN KOMIT AWAL UNTUK BOT KOMIT!!\n')
            print('Kami mengambil Input Berikut:\n')
            print('\t Jumlah Komit     -   Untuk Menghasilkan Jumlah Komit Palsu Tersebut')
            print('\t URL Repositori   -   Untuk Mendorong dan Menarik Kode Ke/Dari Repositori Tersebut (Harus Milik Anda)')
            print('\t Nama Pengguna GitHub - Kadang GitHub meminta Nama Pengguna (Masukkan yang Asli) ...')
            print('\t Email GitHub     -   Kadang GitHub meminta Email (Masukkan yang Asli) ...')
            print('\nKami tidak pernah menyimpan Nama Pengguna, Email, atau Kata Sandi GitHub Anda... ')
            print('Jika Anda tidak mempercayai kami, doronglah repositori sendiri setelah Komit berhasil dengan:')
            print(f'\t\tcd {test_dir} && git push -u --force origin <nama_branch_anda>')
            print('\n\tUntuk Detail Lebih Lanjut, Periksa README.md Anda setelah push.\nSemoga Anda menyukai Proyek ini!!!')
            input('\nTekan Enter untuk melanjutkan...')
        elif inp == '3':
            break
        else:
            print("Input Tidak Valid !!!\nCoba Lagi!!!\nTekan Enter untuk melanjutkan...")
            input()

    print(logo)
    print('\nTerima Kasih telah menggunakan Proyek saya!')
    print('SILAKAN BERI BINTANG, FORK, TONTON JIKA ANDA MENYUKAINYA!')
    sys.exit(0)

if __name__ == "__main__":
    main()
