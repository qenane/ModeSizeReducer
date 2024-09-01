import os
import re
import gz_utils
import textToBit
import bitToText
import json


def edit_line(selected_line):
    """Edits a line in the data structure."""
    if ':' in selected_line:
        complex_match = re.match(r'^(\w+)=([\w\.\-:]+)$', selected_line)
        if not complex_match:
            print("Kompleks satır beklenen formatta değil.")
            return selected_line
        
        key, value_string = complex_match.groups()
        subkey_value_pairs = re.findall(r'([a-zA-Z]+):(-?\d*\.?\d+)', value_string)
        
        if not subkey_value_pairs:
            print("Kompleks satırda anahtar-değer çiftleri bulunamadı.")
            return selected_line
        
        line_dict = dict(subkey_value_pairs)
        print(f"Mevcut Line: {selected_line}")
        for i, (subkey, value) in enumerate(line_dict.items(), 1):
            print(f"{i}. {subkey}: {value}")

        while True:
            try:
                subkey_choice = input(f"Değiştirmek istediğiniz subkey'in numarasını seçin (1-{len(line_dict)}), 'q' ile çık: ")
                if subkey_choice.lower() == 'q':
                    return selected_line
                subkey_index = int(subkey_choice) - 1
                if 0 <= subkey_index < len(line_dict):
                    selected_subkey = list(line_dict.keys())[subkey_index]
                    new_value = input(f"{selected_subkey} için yeni değeri girin: ")
                    line_dict[selected_subkey] = new_value
                    break
                else:
                    print(f"Lütfen 1 ile {len(line_dict)} arasında bir sayı girin.")
            except ValueError:
                print("Geçersiz giriş. Lütfen bir sayı girin veya 'q' ile çıkın.")
        
        new_line = f"{key}={''.join(f'{subkey}:{value}' for subkey, value in line_dict.items())}"
        print(f"Güncellenmiş Line: {new_line}")
        return new_line
    
    else:
        selected_line = selected_line.strip()
        simple_match = re.match(r'^(\w+)=(-?[\w\.\-]+)$', selected_line)
        if not simple_match:
            print("Basit satır beklenen formatta değil.")
            return selected_line
        
        key, value = simple_match.groups()
        print(f"Mevcut Line: {selected_line}")
        print(f"{key}: {value}")
        
        new_value = input(f"{key} için yeni değeri girin: ")
        new_line = f"{key}={new_value}"
        print(f"Güncellenmiş Line: {new_line}")
        return new_line

def format_lines_for_saving(data):
    formatted_lines = []
    current_header = None

    for line in data:
        if line["header"] != current_header:
            current_header = line["header"]
            formatted_lines.append(current_header)
        
        if "key" in line and line["key"]:
            all_values = {**line["numeric_values"], **line["non_numeric_values"]}
            sub_values = "".join([f"{subkey}={subvalue}" for subkey, subvalue in all_values.items()])
            formatted_line = sub_values
        else:
            formatted_line = line["line"]

        formatted_lines.append(formatted_line)
    
    return formatted_lines

def display_menu(options, prompt="Seçiminiz: "):
    for i, option in enumerate(options, 1):
        print(f"{i}- {option}")
    print("r- Üst Menüye Dön")
    print("q- Programdan Çık")
    return input(prompt)

def file_menu(file_extension):
    files = [f for f in os.listdir() if f.endswith(file_extension)]
    if not files:
        print(f"Bu dizinde .{file_extension} dosyası yok.")
        return None, None   
    while True:
        print(f"\nMevcut .{file_extension} dosyaları:")
        for i, file in enumerate(files, 1):
            print(f"{i}- {file}")
        print("r- Üst menüye dön.")

        file_choice = input("Bir dosya seçin (q ile çıkış yapın): ")

        if file_choice.lower() == "q":
            save_choice = input("Değişiklikleri kaydetmek istiyor musunuz? (E/H): ").lower()
            if save_choice == "e":
                with open('codebook.json', 'r') as f:
                    codebook = json.load(f)
                    formatted_lines = format_lines_for_saving(data['lines'])
                    print(formatted_lines)
                textToBit.encode_text(formatted_lines, codebook)

            return None, None
        elif file_choice.lower() == "r":
            return "back", None
        try:
            file_index = int(file_choice) - 1
            if 0 <= file_index < len(files):
                filename = files[file_index]
                break
            else:
                print(f"Geçersiz seçim. Lütfen 1 ile {len(files)} arasında bir sayı girin.")
        except ValueError:
            print("Geçersiz seçim. Lütfen bir sayı girin.")

    decoded_text = None    
    if file_extension == ".gz":
        new_filename = filename[:-3]
        gz_utils.decompress_file(filename, new_filename)
        with open('codebook.json', 'r') as f:
            codebook = json.load(f)
    
        with open(new_filename, "rb") as bin_file:
            encoded_data = bin_file.read()
        decoded_text = bitToText.decode_text(encoded_data, codebook)
            
    elif file_extension == ".ini":
        with open(filename, "r") as file:
            decoded_text = file.read()  
    if decoded_text is not None:
        data = parse_data(decoded_text)
        return data, filename
    else:
        print("Dosya işleme sırasında bir hata oluştu.")
        return None, None


def main_menu():
    while True:
        print("\nAna Menü:")
        print("1- Dizindeki .ini dosyalarıyla işlem yap.")
        print("2- Dizindeki .gz dosyalarıyla işlem yap.")
        print("q- Çıkış")

        choice = input("Seçiminiz: ").strip().lower()

        if choice == '1':
            data, filename = file_menu('.ini')
        elif choice == '2':
            data, filename = file_menu('.gz')
        elif choice == 'q':
            print("Programdan çıkılıyor...")
            return None, None
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")

        if data == "back":
            continue

        return data, filename

def parse_line(line, current_header):
    if ':' in line:
        complex_match = re.match(r'^(\w+)=([\w\.\-:]+)$', line)
        if complex_match:
            key, value_string = complex_match.groups()
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

def main():
    while True:
        data, filename = main_menu()

        if not data:
            return

        while True:
            print("\nMenü:")
            print("1- Edit")
            print("2- Read")
            print("r- Üst menüye dön.")
            choice = input("Seçiminiz: ")

            if choice in ["1", "2"]:
                if not data["headers"]:
                    print("Hiçbir header bulunmamaktadır.")
                    continue

                while True:
                    print("\nHeader'lar:")
                    header_choice = display_menu(data["headers"], "Header seçiniz: ")

                    if header_choice.lower() == "q":
                        save_choice = input("Değişiklikleri kaydetmek istiyor musunuz? (E/H): ").lower()
                        if save_choice == "e":
                            with open('codebook.json', 'r') as f:
                                codebook = json.load(f)
                            formatted_lines = "\n".join(format_lines_for_saving(data['lines']))
                            print(formatted_lines)
                            textToBit.encode_text(formatted_lines, codebook)
                        return
                    elif header_choice.lower() == "r":
                        break
                    else:
                        try:
                            header_index = int(header_choice) - 1
                            if 0 <= header_index < len(data["headers"]):
                                selected_header = data["headers"][header_index]
                            else:
                                print(f"Lütfen 1 ile {len(data['headers'])} arasında bir sayı girin.")
                                continue

                            while True:
                                matching_lines = [line for line in data["lines"] if line["header"] == selected_header]
                                if not matching_lines:
                                    print("Bu header altında satır bulunmamaktadır.")
                                    break

                                print(f"\n{selected_header} altındaki satırlar:")
                                line_options = [line["line"] for line in matching_lines]
                                line_choice = display_menu(line_options, "Satır seçiniz: ")

                                if line_choice.lower() == "q":
                                    save_choice = input("Değişiklikleri kaydetmek istiyor musunuz? (E/H): ").lower()
                                    if save_choice == "e":
                                        with open('codebook.json', 'r') as f:
                                            codebook = json.load(f)
                                        formatted_lines = "\n".join(format_lines_for_saving(data['lines']))
                                        print("LİNES", formatted_lines)
                                        textToBit.encode_text(formatted_lines, codebook)
                                    return
                                elif line_choice.lower() == "r":
                                    break
                                else:
                                    try:
                                        line_index = int(line_choice) - 1
                                        if 0 <= line_index < len(matching_lines):
                                            selected_line = matching_lines[line_index]["line"]
                                        else:
                                            print(f"Lütfen 1 ile {len(matching_lines)} arasında bir sayı girin.")
                                            continue

                                        if choice == "1":
                                            new_line = edit_line(selected_line)
                                            if new_line:
                                                updated_parsed = parse_line(new_line, selected_header)
                                                if updated_parsed["key"]:
                                                    data["lines"][data["lines"].index(matching_lines[line_index])] = updated_parsed
                                                else:
                                                    print("Güncellenmiş satır parse edilemedi. Değişiklik yapılmadı.")
                                        elif choice == "2":
                                            print(f"Seçilen satır: {selected_line}")
                                        else:
                                            print("Geçersiz seçim.")
                                    except ValueError:
                                        print("Geçersiz seçim. Lütfen bir sayı girin.")
                        except ValueError:
                            print("Geçersiz seçim. Lütfen bir sayı girin.")
            elif choice.lower() == "r":
                break
            elif choice.lower() == "q":
                save_choice = input("Değişiklikleri kaydetmek istiyor musunuz? (E/H): ").lower()
                if save_choice == "e":
                    with open('codebook.json', 'r') as f:
                        codebook = json.load(f)
                    formatted_lines = "\n".join(format_lines_for_saving(data['lines']))
                    
                    print(formatted_lines)
                    textToBit.encode_text(formatted_lines, codebook)
                return
            else:
                print("Geçersiz seçim. Lütfen tekrar deneyin.")



if __name__ == "__main__":
    main()