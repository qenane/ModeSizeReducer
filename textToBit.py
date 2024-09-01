import json
import re

def is_numeric(value):
    """Check if a string represents a numeric value."""
    try:
        float(value)
        return True
    except ValueError:
        return False

def parse_segment(segment):
    """Split segment into numeric and non-numeric parts."""
    result = []
    # Match numeric values (including negative and decimal) and non-numeric parts
    matches = re.findall(r'(-?\d*\.?\d+|\D+)', segment)
    for match in matches:
        if match.strip() and not match.strip().isdigit() and not re.match(r'-?\d*\.?\d+', match):
            result.extend(re.findall(r'\D+', match))
        else:
            result.append(match)
    return result

def encode_text(text, codebook):
    delimiters = [" ", ".", ":", "=", "\n", "\t"]
    encoded_text = ""

    delimiter_codebook = {deli: codebook.get(deli, '') for deli in delimiters}
    delimiter_pattern = '|'.join(map(re.escape, delimiters))

    lines = text.splitlines()
    new_line = "\n"
    for line in lines:
        if line in codebook:
            encoded_text += codebook[line]
            encoded_text += codebook[new_line]
            continue

        words_and_delimiters = re.split(f'({delimiter_pattern})', line)
        print("Original segments:", words_and_delimiters)
        
        for segment in words_and_delimiters:
            segment = segment.strip()
            if segment:
                if segment in codebook:
                    # Directly encode segment if it's in codebook
                    encoded_text += codebook[segment]
                else:
                    # Split into numeric and non-numeric parts
                    parts = parse_segment(segment)
                    print("Parsed parts:", parts)
                    for part in parts:
                        if part in codebook:
                            encoded_text += codebook[part]
                        elif is_numeric(part):
                            for char in part:
                                if char in codebook:
                                    encoded_text += codebook[char]
                                else:
                                    print(f"Character '{char}' not found in codebook.")
                        else:
                            print(f"Non-numeric segment '{part}' not found in codebook.")
                            for char in part:
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
        # Ensure the length of encoded_text is a multiple of 8
        length = len(encoded_text)
        padded_length = (length + 7) // 8 * 8
        encoded_text = encoded_text.ljust(padded_length, '0')

        encoded_bytes = int(encoded_text, 2).to_bytes(padded_length // 8, byteorder='big')
        return encoded_bytes
    else:
        print("Error: Encoded text is empty.")
        return None


def main():
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
    encoded_file = "output.bin"
    if encoded_bytes:
        with open(encoded_file, "wb") as bin_file:
            bin_file.write(encoded_bytes)
            
    print(encoded_file)

if __name__ == "__main__":
    main()
