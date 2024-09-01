import re
import json

def parse_line(line, current_header):
    # Remove tab characters
    line = line.replace('\t', ' ')
    
    # Parse lines with ':' and '='
    if ':' in line:
        complex_match = re.match(r'^(\w+)=([\w\.\-:]+)$', line)
        if complex_match:
            key, value_string = complex_match.groups()
            # Extract numeric values, including negative and decimal numbers
            subkey_value_pairs = re.findall(r'([a-zA-Z]+):(-?\d*\.?\d+)', value_string)
            numeric_values = {subkey: subvalue for subkey, subvalue in subkey_value_pairs}
            return {
                'key': key,
                'numeric_values': numeric_values,
                'non_numeric_values': {},
                'header': current_header,
                'line': line
            }
        return {'key': None, 'numeric_values': {}, 'non_numeric_values': {}, 'header': current_header, 'line': line}
    
    # Simple parsing for lines without ':'
    simple_match = re.match(r'^(\w+)=(.+)$', line)
    if simple_match:
        key, value = simple_match.groups()
        if re.match(r'^-?\d+(\.\d+)?$', value):
            return {'key': key, 'numeric_values': {key: value}, 'non_numeric_values': {}, 'header': current_header, 'line': line}
        else:
            return {'key': key, 'numeric_values': {}, 'non_numeric_values': {key: value}, 'header': current_header, 'line': line}
    
    return {'key': None, 'numeric_values': {}, 'non_numeric_values': {}, 'header': current_header, 'line': line}

def parse_data(decoded_text):
    data = {'headers': [], 'lines': []}
    current_header = None

    for line in decoded_text.splitlines():
        if line.startswith('#'):
            current_header = line.strip()
            data['headers'].append(current_header)
        else:
            result = parse_line(line, current_header)
            data['lines'].append(result)

    return data

def encode_text(parsed_data, codebook):
    """Encodes parsed data based on the provided codebook and newline character.

    Args:
        parsed_data: Parsed data dictionary from `parse_data` (dict).
        codebook: A dictionary mapping characters/words to binary strings (dict).

    Returns:
        Encoded text as a string or None if no encoding is possible.
    """
    
    # Define special characters in codebook
    tab_char = "\t"
    new_line = "\n"
    encoded_text = ""

    for header in parsed_data['headers']:
        if header in codebook:
            encoded_text += codebook[header]
            encoded_text += codebook[new_line]
            continue

    for segment in parsed_data['lines']:
        # Check if the entire line is in the codebook
        if segment['line'] in codebook:
            encoded_text += codebook[segment['line']]
            encoded_text += codebook[new_line]
        elif segment['key'] in codebook:
            encoded_text += codebook[segment['key']]
            encoded_text += codebook['=']
            # Encode numeric values
            for value in segment['numeric_values'].values():
                for char in value:
                    if char in codebook:
                        encoded_text += codebook[char]
                    else:
                        print(f"Missing character in codebook: {char}")  # Log missing character
            encoded_text += codebook.get(new_line, '')
        elif segment['non_numeric_values']:
            # Encode non-numeric values
            for char in segment['non_numeric_values'][segment['key']]:
                if char in codebook:
                    encoded_text += codebook[char]
                else:
                    print(f"Missing character in codebook: {char}")
            encoded_text += codebook.get(new_line, '')
        else:
            # Encode the entire line if it doesn't match any key or value
            for char in segment['line']:
                if char in codebook:
                    encoded_text += codebook[char]
                else:
                    print(f"Missing character in codebook: {char}")

    if not encoded_text:
        print("Error: No encoding possible for the provided data.")
        return None

    return encoded_text

def main():
    with open('codebook.json', 'r') as f:
        codebook = json.load(f)

    # Ensure codebook has entries for tab and newline characters


    with open("Mode01.ini", "r") as ini_file:
        decoded_text = ini_file.read()

    parsed_data = parse_data(decoded_text)

    encoded_text = encode_text(parsed_data, codebook)

    if encoded_text:
        # Ensure the length of encoded_text is a multiple of 8
        length = len(encoded_text)
        padded_length = (length + 7) // 8 * 8
        encoded_text = encoded_text.ljust(padded_length, '0')

        encoded_bytes = int(encoded_text, 2).to_bytes(padded_length // 8, byteorder='big')
        with open("output.bin", "wb") as bin_file:
            bin_file.write(encoded_bytes)

if __name__ == "__main__":
    main()
