import json

def decode_text(encoded_bytes, codebook):

    inverted_codebook = {v: k for k, v in codebook.items()}
    
    encoded_binary_str = bin(int.from_bytes(encoded_bytes, byteorder='big'))[2:].zfill(len(encoded_bytes) * 8)
    
    decoded_text = ""
    current_binary = ""

    for bit in encoded_binary_str:
        current_binary += bit
        if current_binary in inverted_codebook:
            decoded_text += inverted_codebook[current_binary]
            current_binary = ""

    return decoded_text

with open('codebook.json', 'r') as f:
    codebook = json.load(f)

with open('encoded_text.bin', 'rb') as bin_file:
    encoded_bytes = bin_file.read()

decoded_text = decode_text(encoded_bytes, codebook)

with open('decoded_text.txt', 'w') as decoded_file:
    decoded_file.write(decoded_text)

print("Decoded text:")
print(decoded_text)


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
