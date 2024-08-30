import os
import re

def edit_line(selected_line):
    """Edits a line in the data structure.

    Args:
        selected_line (str): The line containing key-value pairs in the format.
    """
    
    # Example line format: 'X5=ppi:0tmc:3Smin:0Smax:104Rmin:0Rmax:50000Amin:0.0Amax:359.0Hmin:0.0Hmax:1000.0Vmin:-250.0Vmax:250.0Cmin:0.0Cmax:361.0'
    key_value_pairs = re.findall(r'(\w+)=([\w\.\-:]+)', selected_line)
    
    if not key_value_pairs:
        print("Line does not contain key-value pairs in the expected format.")
        return

    # Create a dictionary to hold subkeys and their corresponding values
    line_dict = {}
    for key, value in key_value_pairs:
        subkey_value_pairs = re.findall(r'(\w+):([\w\.\-]+)', value)
        if subkey_value_pairs:
            line_dict[key] = dict(subkey_value_pairs)
        else:
            line_dict[key] = value

    # Display the line and allow user to edit it
    print(f"Mevcut Line: {selected_line}")
    for i, (key, sub_dict) in enumerate(line_dict.items()):
        print(f"{i + 1}. {key}: {sub_dict}")
    
    # Allow user to select a key to edit
    key_choice = int(input(f"Değiştirmek istediğiniz anahtarın numarasını seçin (1-{len(line_dict)}): ")) - 1
    selected_key = list(line_dict.keys())[key_choice]
    
    if isinstance(line_dict[selected_key], dict):
        # If the selected key has subkeys, allow user to select a subkey to edit
        subkeys = list(line_dict[selected_key].keys())
        for i, subkey in enumerate(subkeys):
            print(f"{i + 1}. {subkey}: {line_dict[selected_key][subkey]}")
        
        subkey_choice = int(input(f"Değiştirmek istediğiniz subkey'in numarasını seçin (1-{len(subkeys)}): ")) - 1
        selected_subkey = subkeys[subkey_choice]
        new_value = input(f"{selected_subkey} için yeni değeri girin: ")
        line_dict[selected_key][selected_subkey] = new_value
    else:
        # If no subkeys, edit the main value
        new_value = input(f"{selected_key} için yeni değeri girin: ")
        line_dict[selected_key] = new_value

    # Reconstruct the line from the edited dictionary
    new_line = ""
    for key, sub_dict in line_dict.items():
        if isinstance(sub_dict, dict):
            subkey_str = "".join([f"{subkey}:{value}" for subkey, value in sub_dict.items()])
            new_line += f"{key}={subkey_str}"
        else:
            new_line += f"{key}={sub_dict}"

    print(f"Güncellenmiş Line: {new_line}")
    return new_line


def format_lines_for_saving(lines):
    formatted_lines = []
    for line in lines:
        if "key" in line:
            sub_values = " ".join(
                [f"{subkey}:{subvalue}" for subkey, subvalue in line["numeric_values"].items()]
            ) + " " + " ".join(
                [f"{subkey}:{subvalue}" for subkey, subvalue in line["non_numeric_values"].items()]
            )
            formatted_line = f"{line['key']} = {sub_values.strip()}"
        else:
            formatted_line = line["line"]
        formatted_lines.append(formatted_line)
    return formatted_lines


def display_menu(options, prompt="Seçiminiz: "):
    """Displays a menu with numbered options and 'r' and 'q' choices.

    Args:
        options (list): A list of menu options.
        prompt (str, optional): Prompt message for user input. Defaults to "Seçiminiz: ".

    Returns:
        str: The user's choice (option number, 'r', or 'q').
    """

    for i, option in enumerate(options, 1):
        print(f"{i}- {option}")
    print("r- Üst Menüye Dön")
    print("q- Programdan Çık")

    return input(prompt)


def main_menu():
    """Displays a menu for selecting a TXT file and returns data and filename.

    Returns:
        tuple: A tuple containing the parsed data (dict) and the filename (str),
               or None, None if no file is selected.
    """

    txt_files = [f for f in os.listdir() if f.endswith(".txt")]
    if not txt_files:
        print("Bulunacak TXT dosyası yok.")
        return None, None

    print("Mevcut TXT dosyaları:")
    for i, file in enumerate(txt_files, 1):
        print(f"{i}- {file}")

    while True:
        file_choice = input("Bir dosya seçin (q ile çıkış yapın): ")
        if file_choice.lower() == "q":
            return None, None
        try:
            file_index = int(file_choice) - 1
            if (
                0 <= file_index < len(txt_files)
            ):  # İndeks 0'dan başlar ve liste uzunluğundan 1 eksik olmalıdır
                filename = txt_files[file_index]
                break
            else:
                print(
                    "Geçersiz seçim. Lütfen 1 ile",
                    len(txt_files),
                    "arasında bir sayı girin.",
                )
        except ValueError:
            print("Geçersiz seçim. Lütfen bir sayı girin.")
    with open(filename, "r") as file:
        decoded_text = file.read()

    data = parse_data(decoded_text)
    return data, filename

def parse_line(line, current_header):
    # Karmaşık formatı kontrol et (X0=ppi:0tmc:3Smin:0Smax:109...)
    complex_match = re.match(r'^(\w+)=([\w\.\-:]+)$', line)
    if complex_match:
        key, value_string = complex_match.groups()
        numeric_values = {}
        non_numeric_values = {}

        # ':', ':', ve ':''den sonraki numerik olmayan kısımları ayır
        segments = re.split(r'(?<=\d)(?=\D)|(?<=\D)(?=\d)', value_string)

        # Segmentleri işleyerek anahtar-değer çiftlerini ayrıştır
        for i in range(0, len(segments) - 1, 2):
            subkey = segments[i]
            subvalue = segments[i+1]
            if re.match(r'^-?\d+(\.\d+)?$', subvalue):  # Numerik mi değil mi kontrol et
                numeric_values[subkey] = subvalue
            else:
                non_numeric_values[subkey] = subvalue

        return {
            'key': key,
            'numeric_values': numeric_values,
            'non_numeric_values': non_numeric_values,
            'header': current_header,
            'line': line
        }

    # Basit formatı kontrol et (ASS0=351, SECTOR=0, Lang=-1...)
    simple_match = re.match(r'^(\w+)=(.+)$', line)
    if simple_match:
        key, value = simple_match.groups()
        return {
            'key': key,
            'numeric_values': {key: value} if re.match(r'^-?\d+(\.\d+)?$', value) else {},
            'non_numeric_values': {} if re.match(r'^-?\d+(\.\d+)?$', value) else {key: value},
            'header': current_header,
            'line': line
        }

    # Hiçbir formata uymayan satırlar
    return {
        'key': None,
        'numeric_values': {},
        'non_numeric_values': {},
        'header': current_header,
        'line': line
    }

    
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
    data, filename = main_menu()

    if not data:
        return

    while True:
        print("\nMenü:")
        print("1- Edit")
        print("2- Read")
        choice = input("Seçiminiz: ")

        if choice == "1" or choice == "2":
            print("\nHeader'lar:")
            header_choice = display_menu(data["headers"], "Header seçiniz: ")

            if header_choice == "q":
                break
            elif header_choice == "r":
                continue
            else:
                try:
                    header_index = int(header_choice) - 1
                    selected_header = data["headers"][header_index]

                    matching_lines = [
                        line for line in data["lines"] if line["header"] == selected_header
                    ]
                    if not matching_lines:
                        print("Bu header altında satır bulunmamaktadır.")
                        continue

                    print(f"\n{selected_header} altındaki satırlar:")
                    line_choice = display_menu(
                        [line["line"] for line in matching_lines],
                        "Satır seçiniz: ",
                    )

                    if line_choice == "q":
                        break
                    elif line_choice == "r":
                        continue
                    else:
                        try:
                            line_index = int(line_choice) - 1
                            selected_line = matching_lines[line_index]["line"]

                            if choice == "1":  # Edit işlemi
                                new_line = edit_line(selected_line)
                                if new_line:
                                    data["lines"][
                                        line_index
                                    ] = new_line  # Değiştirilen satırı güncelle

                            elif choice == "2":  # Read işlemi
                                print(f"Seçilen satır: {selected_line}")
                            else:
                                print("Geçersiz seçim.")

                        except ValueError:
                            print("Geçersiz seçim. Lütfen bir sayı girin.")

                except ValueError:
                    print("Geçersiz seçim. Lütfen bir sayı girin.")

        elif choice == "q":
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")

    save_choice = input("Değişiklikleri kaydetmek istiyor musunuz? (E/H): ").lower()

    if save_choice == "e":
        formatted_lines = format_lines_for_saving(data["lines"])
        with open(filename, "w") as file:
            file.write("\n".join(formatted_lines))
        print("Değişiklikler kaydedildi.")


if __name__ == "__main__":
    main()
