import subprocess
import os
import platform
from stat import S_IXUSR, S_IRGRP, S_IROTH, S_IREAD, S_IWRITE, S_IWGRP, S_IWOTH

def find_7zip():
    """7-Zip'in kurulu olduğu yolu bulmaya çalışır veya kullanıcıdan ister."""
    seven_zip_cmd = '7z'
    
    if platform.system() == 'Windows':
        # Windows'ta '7z.exe' kurulu ve PATH'te mi?
        seven_zip_cmd = '7z.exe'
        try:
            subprocess.run([seven_zip_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return seven_zip_cmd
        except FileNotFoundError:
            # PATH'te değilse tam yolu kontrol et
            possible_paths = [
                r'C:\Program Files\7-Zip\7z.exe',
                r'C:\Program Files (x86)\7-Zip\7z.exe'
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return path
            
            # Kullanıcıdan yol iste
            user_path = input("7-Zip bulunamadı. Lütfen 7z.exe dosyasının tam yolunu girin: ")
            if os.path.exists(user_path):
                return user_path
            else:
                raise FileNotFoundError("7-Zip bulunamadı ve verilen yol geçersiz.")
    
    elif platform.system() == 'Linux':
        # Linux'ta '7z' kurulu ve PATH'te mi?
        try:
            subprocess.run([seven_zip_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return seven_zip_cmd
        except FileNotFoundError:
            raise FileNotFoundError("7-Zip Linux'ta bulunamadı. 'p7zip-full' paketini yükleyin.")
    
    return seven_zip_cmd

def compress_file(input_file, output_file):
    """Dosyayı 7z formatında sıkıştırır."""
    seven_zip_cmd = find_7zip()
    try:
        subprocess.run([seven_zip_cmd, 'a', output_file, input_file], check=True)
        print(f"{input_file} başarıyla {output_file} olarak sıkıştırıldı.")
    except subprocess.CalledProcessError:
        print(f"{input_file} sıkıştırılırken hata oluştu.")
    os.chmod(input_file, S_IREAD | S_IRGRP | S_IROTH)
        

def decompress_file(input_file, output_name):
    # Dosya izinlerini ayarla
    
    # Geçici bir dizin oluştur
    temp_dir = "temp_extract"
    os.makedirs(temp_dir, exist_ok=True)
    
    seven_zip_cmd = find_7zip()
    try:
        # 7-Zip ile geçici dizine çıkar
        subprocess.run([seven_zip_cmd, 'e', input_file, f"-o{temp_dir}"], check=True)

        # Geçici dizindeki dosyayı yeni ismiyle yeniden adlandır
        extracted_file = os.listdir(temp_dir)[0]  # Çıkarılan ilk dosyayı al
        extracted_path = os.path.join(temp_dir, extracted_file)
        os.rename(extracted_path, output_name)

        # Geçici dizini temizle
        os.rmdir(temp_dir)

    except subprocess.CalledProcessError:
        print(f"{input_file} açılırken hata oluştu.")
    except Exception as e:
        print(f"Bir hata oluştu: {str(e)}")
    os.chmod(output_name, S_IXUSR | S_IWRITE | S_IREAD | S_IRGRP | S_IROTH | S_IWGRP | S_IWOTH )
    if os.path.exists(f'{output_name}.bin'):
        os.chmod(f'{output_name}.bin', S_IXUSR | S_IWRITE | S_IREAD | S_IRGRP | S_IROTH | S_IWGRP | S_IWOTH )

def main():
    input_path = input("Sıkıştırmak istediğiniz dosya veya dizin: ").strip()
    
    if not os.path.exists(input_path):
        print(f"Hata: {input_path} bulunamadı.")
        return

    output_tar_7z = input("Çıkış dosyasının adı (örneğin, Mode01.7z): ").strip()
    
    if not output_tar_7z.endswith('.7z'):
        output_tar_7z += '.7z'

    # Dosyayı sıkıştırma
    compress_file(input_path, output_tar_7z)

    # Dosyayı açma
    output_folder = input("Dosyaları çıkarmak istediğiniz klasör adı: ").strip()
    
    decompress_file(output_tar_7z, output_folder)

if __name__ == "__main__":
    main()
