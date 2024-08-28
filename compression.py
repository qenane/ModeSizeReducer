import gzip
import os
import time


def main():
    input_file = 'encoded_text.bin'
    output_file = f"{input_file}.gz"  # Create output filename with .gz extension

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

    gzip_time, gzip_size = measure_compression_time(gzip_compress, output_file)

    original_size = os.path.getsize(input_file)
    print(f"Original Size: {original_size} bytes")

    print(f"Gzip Time: {gzip_time:.6f} seconds, Size: {gzip_size} bytes")



    # os.remove(input_file)
    # print(f"Original file '{input_file}' deleted.")


if __name__ == "__main__":
    main()