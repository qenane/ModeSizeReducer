import gzip
import os

def compress_file(input_file, output_file):
    with open(input_file, 'rb') as f_in, gzip.open(output_file, 'wb') as f_out:
        f_out.writelines(f_in)


def decompress_file(input_file, output_file):
    with gzip.open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        f_out.writelines(f_in)


def main():
    input_file = 'output.bin'
    compressed_file = f"{input_file}.gz" 

    compress_file(input_file, compressed_file)

    # decompressed_file = f"{input_file[:-3]}"
    # decompress_file(compressed_file, decompressed_file)

    # Uncomment to remove the original file after decompression (optional)
    # os.remove(input_file)
    # print(f"Original file '{input_file}' deleted.")


if __name__ == "__main__":
    main()