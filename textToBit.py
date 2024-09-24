import json
import re

#Numerik ve numerik olmadığını kontrol eder.
def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
#Numerik ve numerik olmayan kısımları segmentler halinde ayırır.
def parse_segment(segment):
    result = []
    matches = re.findall(r'(-?\d*\.?\d+|\D+)', segment)
    for match in matches:
        if match.strip() and not match.strip().isdigit() and not re.match(r'-?\d*\.?\d+', match):
            result.extend(re.findall(r'\D+', match))
        else:
            result.append(match)
    return result

#Codebook'tan encode işlemini yapar.
def encode_text(text, codebook):
    delimiters = [" ", ".", ":", "=", "\n", "\t"]
    encoded_text = ""

    delimiter_codebook = {deli: codebook.get(deli, '') for deli in delimiters}#ayraçların codebooktaki karşılığını alır ve 
    delimiter_pattern = '|'.join(map(re.escape, delimiters))                  #ayraçları da dönüştürmek üzere değişkende tutar
    
    lines = text.splitlines()#texti satırlara ayırır
    new_line = "\n"
    
    #Satırlar arasında codebook'ta direkt bütün satır olarak kaydedilenleri bulur. 
    for line in lines:
        if line in codebook:
            encoded_text += codebook[line]
            encoded_text += codebook[new_line]
            continue

        #Codebookta bulunmayan satırları kelime ve ayraç tutacak şekilde ayırır
        words_and_delimiters = re.split(f'({delimiter_pattern})', line)
        for segment in words_and_delimiters:
            segment = segment.strip()
            if segment:
                if segment in codebook:
                    encoded_text += codebook[segment]
                else:

                    parts = parse_segment(segment)
                    for part in parts:
                        if part in codebook:
                            encoded_text += codebook[part]
                        elif is_numeric(part):
                            for char in part:
                                if char in codebook:
                                    encoded_text += codebook[char]
                                else:
                                    print(f"'{char}' codebook'ta bulunamadı.")
                        else:
                            print(f" '{part}' codebook'ta bulunamadı.")
                            for char in part:
                                if char in codebook:
                                    encoded_text += codebook[char]
                                else:
                                    print(f"'{char}' codebook'ta bulunamadı.")
            else:
                encoded_text += delimiter_codebook.get(segment, '')

        if '\n' not in encoded_text:
            encoded_text += delimiter_codebook.get('\n', '')

    #Yazıyı byte haline getirir
    if encoded_text:
        length = len(encoded_text)
        padded_length = (length + 7) // 8 * 8
        encoded_text = encoded_text.ljust(padded_length, '0')

        encoded_bytes = int(encoded_text, 2).to_bytes(padded_length // 8, byteorder='big')
        return encoded_bytes
    else:
        print("Error: Encoded text boş.")
        return None

#codebook açar ve tüm işlemleri gerçekleştirip .bin dosyasını oluşturur.
def main():
    with open('codebook.json', 'r') as f:
        codebook = json.load(f)


    text = ""   
    encoded_bytes = encode_text(text, codebook)
    encoded_file = "output.bin"
    if encoded_bytes:
        with open(encoded_file, "wb") as bin_file:
            bin_file.write(encoded_bytes)
            
    print(f"Encoded file saved as: {encoded_file}")

if __name__ == "__main__":
    main()
else:
    export_encode_text= encode_text
