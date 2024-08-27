import json
import re
from stat import S_IXUSR, S_IRGRP, S_IROTH, S_IREAD, S_IWRITE
import os


def encode_text(text, codebook):
    delimiters = [" ", ".", ":", "=", "\n", "\t","\n","\t"]
    encoded_text = ""

    delimiter_codebook = {deli: codebook.get(deli, '') for deli in delimiters}

    delimiter_pattern = '|'.join(map(re.escape, delimiters))

    lines = text.splitlines()
    new_line = "\\n"
    for line in lines:
        if line in codebook:
            encoded_text += codebook[line]
            encoded_text += codebook[new_line]
            continue

        words_and_delimiters = re.split(f'({delimiter_pattern})', line)

        for segment in words_and_delimiters:
            if segment in codebook:
                encoded_text += codebook[segment]
            else:
                if segment.strip():
                    for char in segment:
                        if char in codebook:
                            encoded_text += codebook[char]
                        else:
                            print(f"Character '{char}' not found in codebook.")
                else:
                    encoded_text += delimiter_codebook.get(segment, '')

        if '\n' not in encoded_text:
            encoded_text += delimiter_codebook.get('\n', '')

    print("Encoded text:", encoded_text)


    if encoded_text:  
        encoded_bytes = int(encoded_text, 2).to_bytes((len(encoded_text) + 7) // 8, byteorder='big')


        return encoded_bytes
    else:
        print("Error: Encoded text is empty.")
        return None

with open('codebook.json', 'r') as f:
    codebook = json.load(f)

with open("Mode01.ini", "r") as ini_file:
    lines = ini_file.readlines()

text = ""
for line in lines:
    line = line.rstrip()  
    if line.startswith('#'):
        text += f'{line}\n'
    elif line:
        if '=' in line:
            text += f'{line}\n'
        else:
            text += f'{line}\n'
    else:
        text += '\n'

print("Text from file:")
print(text)

encoded_bytes = encode_text(text, codebook)
encoded_file = "encoded_text.bin"
os.chmod(encoded_file, S_IXUSR | S_IWRITE )

if encoded_bytes:
    with open('encoded_text.bin', 'wb') as bin_file:
        bin_file.write(encoded_bytes)

    os.chmod(encoded_file, S_IREAD | S_IRGRP | S_IROTH)

# textToBit.py

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
