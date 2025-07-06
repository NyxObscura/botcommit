import os
import sys
import subprocess
import urllib.request
from datetime import datetime # Import datetime untuk timestamp

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

def run_command(command, cwd=None, suppress_output=False, return_output=False):
    """Fungsi pembantu untuk menjalankan perintah shell."""
    try:
        if suppress_output:
            process = subprocess.run(command, shell=True, check=True, cwd=cwd,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            process = subprocess.run(command, shell=True, check=True, cwd=cwd, text=True)

        if return_output:
            return process.stdout.strip()
        return True # Mengembalikan True untuk menandakan sukses jika tidak perlu output
    except subprocess.CalledProcessError as e:
        print(f"[-] Error saat menjalankan perintah: {e.cmd}")
        print(f"    Kode Keluar: {e.returncode}")
        if e.stdout:
            print(f"    Output Standar: {e.stdout.strip()}")
        if e.stderr:
            print(f"    Error Standar: {e.stderr.strip()}")
        return False # Mengembalikan False untuk menandakan kegagalan
    except FileNotFoundError:
        print(f"[-] Perintah tidak ditemukan. Pastikan Git terinstal dan ada di PATH.")
        return False # Mengembalikan False untuk menandakan kegagalan
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
                # Periksa hanya respons header, lebih cepat dan ringan
                req = urllib.request.Request(gu, method='HEAD')
                if not urllib.request.urlopen(req, timeout=5).getcode() == 200:
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
            except Exception as e:
                print(f'[!] Terjadi kesalahan tak terduga saat memeriksa URL: {e}')
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
                # Pastikan ini aman, hanya membersihkan konten dalam direktori test_dir
                if not run_command(f'rm -rf {test_dir}/*', suppress_output=True, cwd=os.getcwd()):
                    print("[-] Gagal membersihkan direktori lama. Coba hapus secara manual.")
                    input('\nTekan Enter untuk melanjutkan...')
                    continue
            else:
                print(f'[+] Direktori "{test_dir}" tidak ditemukan. Membuat satu....')
                try:
                    os.makedirs(test_dir)
                except OSError as e:
                    print(f"[-] Gagal membuat direktori '{test_dir}': {e}")
                    input('\nTekan Enter untuk melanjutkan...')
                    continue


            print('[+] Menyiapkan Direktori...')
            print('[+] Menarik Repositori Jauh ke Direktori Lokal...')

            # Git clone akan membuat direktori baru jika tidak ada,
            # jadi kita langsung clone ke test_dir tanpa membuat test_dir terpisah sebelumnya
            # (tapi kita tetap buat untuk kasus kalau ada proses sebelumnya)
            # clone_success = run_command(f'git clone {gu} {test_dir}', suppress_output=False) # Ganti ini
            
            # Kloning ke direktori temporer terlebih dahulu, lalu pindahkan isinya
            # ini lebih aman jika direktori tujuan sudah ada dan tidak kosong
            temp_clone_dir_name = gu.split('/')[-1] # Nama repo dari URL
            if temp_clone_dir_name.endswith('.git'):
                temp_clone_dir_name = temp_clone_dir_name[:-4]

            temp_clone_path = os.path.join(os.getcwd(), temp_clone_dir_name) # Path absolut untuk clone

            print(f"[+] Kloning {gu} ke {temp_clone_path}...")
            clone_result = run_command(f'git clone {gu} {temp_clone_path}', suppress_output=False)
            
            if not clone_result: # Jika clone_result adalah False (gagal)
                print("[-] Gagal mengkloning repositori. Pastikan URL benar, Anda memiliki izin, dan tidak ada masalah koneksi.")
                input('\nTekan Enter untuk melanjutkan...')
                continue
            
            print(f"[+] Memindahkan konten dari {temp_clone_path} ke {test_dir}...")
            # Pindahkan semua konten dari temp_clone_path ke test_dir
            move_success = True
            for item in os.listdir(temp_clone_path):
                source = os.path.join(temp_clone_path, item)
                destination = os.path.join(test_dir, item)
                try:
                    # Menggunakan shutils.move untuk penanganan yang lebih baik
                    import shutil
                    shutil.move(source, destination)
                except Exception as e:
                    print(f"[-] Gagal memindahkan {source} ke {destination}: {e}")
                    move_success = False
                    break
            
            if not move_success:
                print("[-] Gagal memindahkan file setelah kloning. Silakan cek izin dan coba lagi.")
                run_command(f'rm -rf {temp_clone_path}', suppress_output=True) # Bersihkan sisa
                input('\nTekan Enter untuk melanjutkan...')
                continue

            # Hapus direktori kloning sementara
            run_command(f'rm -rf {temp_clone_path}', suppress_output=True)

            print('[+] Repositori Berhasil Ditarik dan Dipersiapkan.')

            # Tambahkan informasi Gemini ke README.md jika belum ada
            readme_path = os.path.join(test_dir, 'README.md')
            if not os.path.exists(readme_path):
                open(readme_path, 'a').close() # Buat file jika tidak ada

            try:
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
            except Exception as e:
                print(f"[-] Gagal memodifikasi README.md: {e}")
                input('\nTekan Enter untuk melanjutkan...')
                continue


            # Konfigurasi Git
            if not run_command(f'git config user.name "{gn}"', cwd=test_dir, suppress_output=True):
                print("[-] Gagal mengatur user.name Git.")
                input('\nTekan Enter untuk melanjutkan...')
                continue
            if not run_command(f'git config user.email "{ge}"', cwd=test_dir, suppress_output=True):
                print("[-] Gagal mengatur user.email Git.")
                input('\nTekan Enter untuk melanjutkan...')
                continue
            if not run_command('git add .', cwd=test_dir, suppress_output=True):
                print("[-] Gagal menambahkan perubahan awal ke staging.")
                input('\nTekan Enter untuk melanjutkan...')
                continue
            
            # Initial commit jika repo benar-benar kosong atau baru dikloning dan perlu commit pertama
            # GitHub repo yang baru dikloning biasanya sudah ada commit pertamanya
            # Jika tidak, ini bisa menyebabkan masalah
            # Jika user ingin mengisi dari tanggal awal akun dibuat, pendekatan ini tidak cukup.
            # Script ini hanya akan mengisi jumlah commit dari waktu berjalan.
            print('[+] Direktori Diinisialisasi.')

            print('[+] Memulai Komit untuk Mendapatkan Kontribusi...')
            for i in progressbar.progressbar(range(nc), redirect_stdout=True): # nc-1 menjadi nc
                temp_file_path = os.path.join(test_dir, 'gemini_commit_trace.txt')
                
                # Tambahkan konten baru atau update yang sudah ada
                with open(temp_file_path, 'a') as f:
                    f.write(f"Commit oleh Gemini Bot pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Komit {i+1}/{nc}\n")

                if not run_command('git add .', cwd=test_dir, suppress_output=True):
                    print(f"\n[-] Gagal menambahkan perubahan untuk komit {i+1}. Melanjutkan...")
                    continue
                if not run_command(f'git commit -m "Commit oleh Gemini Bot!!! {i+1}/{nc}"', cwd=test_dir, suppress_output=True):
                    print(f"\n[-] Gagal melakukan komit {i+1}. Melanjutkan...")
                    continue
                # Tambahkan delay kecil jika perlu untuk menghindari "too fast" issues
                # import time
                # time.sleep(0.1)

            print('\n[+] Membersihkan Repositori...')
            # Menghapus file jejak komit terakhir.
            # Jika Anda ingin menyimpan jejak, hapus baris ini.
            if os.path.exists(temp_file_path):
                run_command(f'rm {temp_file_path}', suppress_output=True)

            if not run_command('git gc', cwd=test_dir, suppress_output=True):
                print("[-] Gagal membersihkan repositori Git.")
            print('[+] Repositori Dibersihkan.')

            print('[-] Komit Terakhir...')
            if not run_command('git add .', cwd=test_dir, suppress_output=True):
                print("[-] Gagal menambahkan perubahan terakhir.")
            if not run_command(f'git commit -m "Final Commit oleh Gemini Bot!!!"', cwd=test_dir, suppress_output=True):
                print("[-] Gagal melakukan komit terakhir.")

            print(f'[+] Mendorong Repo ke URL Remote: {gu} pada branch {branch_name}')
            push_success = run_command(f'git push -u --force origin {branch_name}', cwd=test_dir, suppress_output=False)

            if not push_success:
                print("[-] Gagal melakukan push. Pastikan Anda memiliki kredensial Git yang benar.")
                print("    Anda mungkin perlu melakukan autentikasi (misalnya, Personal Access Token).")
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
            print(f'\t\tcd temp_repo_for_commits && git push -u --force origin <nama_branch_anda>')
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
