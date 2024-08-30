def edit_line(selected_line):
    if 'key' in selected_line:
        print(f"Mevcut line: {selected_line['key']} = {selected_line['value']}")

        # Eğer value bir dictionary ise, subkey-subvalue formatında olduğunu varsayıyoruz
        if isinstance(selected_line['value'], dict):
            # Subkey-subvalue çiftlerini göster
            subkeys = list(selected_line['value'].keys())
            for i, subkey in enumerate(subkeys):
                print(f"{i + 1}. {subkey}: {selected_line['value'][subkey]}")

            # Kullanıcıdan subkey seçmesini iste
            subkey_index = int(input(f"Değiştirmek istediğiniz subkey'in numarasını seçin (1-{len(subkeys)}): ")) - 1
            selected_subkey = subkeys[subkey_index]

            # Seçilen subkey'in subvalue'sini değiştir
            current_value = selected_line['value'][selected_subkey]
            new_value = input(f"{selected_subkey} için yeni değeri girin (mevcut: {current_value}): ")
            if new_value:
                selected_line['value'][selected_subkey] = new_value
        else:
            # Eğer value string ise, doğrudan değiştirilmesine izin veriyoruz
            new_value = input(f"Yeni değer girin ({selected_line['value']}): ")
            if new_value:
                selected_line['value'] = new_value

    elif 'line' in selected_line:
        print(f"Mevcut line: {selected_line['line']}")
        new_line = input("Yeni line girin: ")
        if new_line:
            selected_line['line'] = new_line

    print("Değişiklik kaydedildi.")



def format_lines_for_saving(lines):
    formatted_lines = []
    for line in lines:
        if 'key' in line:
            sub_values = ' '.join([f"{subkey}:{subvalue}" for subkey, subvalue in line['value'].items()])
            formatted_line = f"{line['key']} = {sub_values}"
            formatted_lines.append(formatted_line)
        else:
            formatted_lines.append(line['line'])
    return formatted_lines

def display_menu(options, prompt="Seçiminiz: "):
    for i, option in enumerate(options, 1):
        print(f"{i}- {option}")
    print("r- Üst menü")
    print("q- Programdan çık")

    return input(prompt)

def main_menu():
    import os
    txt_files = [f for f in os.listdir() if f.endswith('.txt')]
    if not txt_files:
        print("Bulunacak TXT dosyası yok.")
        return None, None

    print("Mevcut TXT dosyaları:")
    for i, file in enumerate(txt_files, 1):
        print(f"{i}- {file}")

    file_choice = input("Bir dosya seçin (q ile çıkış yapın): ")

    if file_choice.lower() == 'q':
        return None, None

    try:
        file_index = int(file_choice) - 1
        filename = txt_files[file_index]
    except (IndexError, ValueError):
        print("Geçersiz seçim.")
        return None, None

    with open(filename, "r") as file:
        decoded_text = file.read()

    data = parse_data(decoded_text)
    return data, filename

def parse_data(decoded_text):
    data = {'headers': [], 'lines': []}
    current_header = None

    for line in decoded_text.splitlines():
        if line.startswith('#'):
            current_header = line.strip()
            data['headers'].append(current_header)
        else:
            try:
                key, value = line.split('=', 1)
                sub_values = {}
                for sub_value in value.strip().split():
                    subkey, subval = sub_value.split(':')
                    sub_values[subkey] = subval
                data['lines'].append({'header': current_header, 'key': key, 'value': sub_values})
            except ValueError:
                data['lines'].append({'header': current_header, 'line': line.strip()})

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

        if choice == '1' or choice == '2':
            print("\nHeader'lar:")
            header_choice = display_menu(data['headers'], "Header seçiniz: ")

            if header_choice == 'q':
                break
            elif header_choice == 'r':
                continue
            else:
                try:
                    header_index = int(header_choice) - 1
                    selected_header = data['headers'][header_index]

                    print(f"\n{selected_header} header'ının line'ları:")
                    lines = [line for line in data['lines'] if line['header'] == selected_header]

                    line_choice = display_menu([f"{line['key']} = {line['value']}" if 'key' in line else f"{line['line']}" for line in lines], "Line seçiniz: ")

                    if line_choice == 'q':
                        break
                    elif line_choice == 'r':
                        continue
                    elif line_choice == '0' and choice == '2':  # Tümünü Göster seçeneği sadece Read'de mevcut
                        print(f"\n{selected_header} Header'ındaki tüm line'lar:")
                        for line in lines:
                            if 'key' in line:
                                sub_values = ' '.join([f"{subkey}:{subvalue}" for subkey, subvalue in line['value'].items()])
                                print(f"{line['key']} = {sub_values}")
                            else:
                                print(f"{line['line']}")
                        continue
                    else:
                        try:
                            line_index = int(line_choice) - 1
                            selected_line = lines[line_index]
                            print(f"Seçilen line: {selected_line}")
                            if choice == '1':  # Sadece Edit modunda değişiklik yapılabilir
                                edit_line(selected_line)  # Burada 'selected_line' nesnesini gönderiyoruz
                        except (IndexError, ValueError):
                            print("Geçersiz line seçimi.")
                except (IndexError, ValueError):
                    print("Geçersiz header seçimi.")
        else:
            print("Geçersiz seçim.")

    save_choice = input("Değişiklikler kaydedilsin mi? (e/h): ")
    if save_choice.lower() == 'e':
        with open(filename, "w") as file:
            for header in data['headers']:
                file.write(f"{header}\n")
                header_lines = [line for line in data['lines'] if line['header'] == header]
                formatted_lines = format_lines_for_saving(header_lines)
                file.write("\n".join(formatted_lines) + "\n")
        print(f"Değişiklikler {filename} dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
