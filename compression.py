import gzip
import bz2
import lzma
import os
import time

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

def bzip2_compress(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        with bz2.open(output_file, 'wb') as f_out:
            f_out.writelines(f_in)

def lzma_compress(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        with lzma.open(output_file, 'wb') as f_out:
            f_out.writelines(f_in)

gzip_time, gzip_size = measure_compression_time(gzip_compress, 'encoded_text.bin.gz')
bzip2_time, bzip2_size = measure_compression_time(bzip2_compress, 'encoded_text.bin.bz2')
lzma_time, lzma_size = measure_compression_time(lzma_compress, 'encoded_text.bin.xz')

original_size = os.path.getsize(input_file)
print(f"Original Size: {original_size} bytes")

print(f"Gzip Time: {gzip_time:.6f} seconds, Size: {gzip_size} bytes")
print(f"Bzip2 Time: {bzip2_time:.6f} seconds, Size: {bzip2_size} bytes")
print(f"LZMA Time: {lzma_time:.6f} seconds, Size: {lzma_size} bytes")
