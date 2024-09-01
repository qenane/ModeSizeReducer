import json

def decode_text(encoded_bytes, codebook):
    """
    İkili verileri, verilen kod kitabını kullanarak metne çevirir.

    Args:
        encoded_bytes: Encode edilmiş ikili veri.
        codebook: Kod kitabı (karakter-ikili eşleştirmeleri).

    Returns:
        Çevrilen metin.
    """

    # İkili verileri bir bit dizisine çevir
    binary_string = ''.join(format(byte, '08b') for byte in encoded_bytes)

    # Kod kitabını tersine çevir (ikili değer: karakter)
    reverse_codebook = {v: k for k, v in codebook.items()}

    decoded_text = ""
    current_code = ""
    for bit in binary_string:
        current_code += bit
        if current_code in reverse_codebook:
            decoded_text += reverse_codebook[current_code]
            current_code = ""

    return decoded_text

def main():
    with open('codebook.json', 'r') as f:
        codebook = json.load(f)

    with open("output.bin", "rb") as bin_file:
        encoded_data = bin_file.read()

    decoded_text = decode_text(encoded_data, codebook)

    # Çevrilen metni bir dosyaya yaz veya ekrana yazdır
    with open("decoded.txt", "w") as f:
        f.write(decoded_text)

if __name__ == "__main__":
    main()