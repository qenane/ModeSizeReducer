import gzip
import os
import tarfile

def compress_tar_gz(input_dir, output_filename):
    # 'w:gz' mode: write with gzip compression
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(input_dir, arcname=".")




def compress_file(input_file, output_file):

    with open(input_file, 'rb') as f_in, gzip.open(output_file, 'wb') as f_out:
        f_out.writelines(f_in)



def decompress_file(input_file, output_file):

    with gzip.open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        f_out.writelines(f_in)



def main():
    # Örnek kullanım
    input_directory = "Mode01 (2).tar"  # Sıkıştırmak istediğiniz dosya veya dizin
    output_tar_gz = "Mode01.tarr.gz"  # Çıkış dosya adı
    compress_tar_gz(input_directory, output_tar_gz)
    # input_file = 'Mode01.tar'
    # compressed_file = "Mode01.gz" 

    # compress_file(input_file, compressed_file)

    # decompressed_file = f"{input_file}"
    # decompress_file(compressed_file, decompressed_file)

    # Uncomment to remove the original file after decompression (optional)
    # os.remove(input_file)
    # print(f"Original file '{input_file}' deleted.")


if __name__ == "__main__":
    main()