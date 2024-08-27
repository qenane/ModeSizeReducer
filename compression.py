import gzip
import os
import time
import json

input_file = 'encoded_text.bin'

def measure_compression_time(compression_func, output_file):
    start_time = time.time()
    compression_func(input_file, output_file)
    end_time = time.time()
    compression_time = end_time - start_time
    compressed_size = os.path.getsize(output_file)
    return compression_time, compressed_size

def gzip_compress(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        with gzip.open(output_file, 'wb') as f_out:
            f_out.writelines(f_in)

gzip_time, gzip_size = measure_compression_time(gzip_compress, 'encoded_text.bin.gz')


original_size = os.path.getsize(input_file)
print(f"Original Size: {original_size} bytes")

print(f"Gzip Time: {gzip_time:.6f} seconds, Size: {gzip_size} bytes")


# Mevcut kodlar...

def main():
    # Text to binary çevirme işlemlerini buraya taşıyın
    with open('codebook.json', 'r') as f:
        codebook = json.load(f)
    with open("Mode01.ini", "r") as ini_file:
        # Buraya mevcut işlemler...
        pass

if __name__ == "__main__":
    main()
