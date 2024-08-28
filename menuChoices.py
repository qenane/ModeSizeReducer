import bitToText

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
                data['lines'].append({'header': current_header, 'key': key, 'value': value.strip()})
            except ValueError:
                data['lines'].append({'header': current_header, 'line': line})

    return data

def display_menu(title, options):
    print(f"\n{title}")
    for i, option in enumerate(options, start=1):  # Menü seçenekleri 1'den başlatılıyor
        print(f"{i} - {option}")
    print("q - Programdan çık")

def select_option(prompt, options):
    while True:
        choice = input(f"\n{prompt}: ").strip()
        if choice == 'q':
            return 'quit'
        elif choice == 'r':
            return 'back'
        try:
            index = int(choice)
            if 0 <= index <= len(options):  # Tüm dosyayı göster seçeneğini de dahil etmek için <= kullanılıyor
                return index - 1  # Kullanıcının 1'den başlayan seçimini 0 tabanlı indekse dönüştürüyoruz
            else:
                print("Geçersiz seçim, tekrar deneyin.")
        except ValueError:
            print("Lütfen bir sayı girin veya 'r' ya da 'q' seçeneklerini kullanın.")

def handle_read_mode(data):
    while True:
        display_menu("Header'lar", data['headers'])
        header_choice = select_option("Header seçiniz", data['headers'])

        if header_choice == -1:  # Tüm dosyayı göster seçeneği
            print("\nTüm dosya:")
            for line in data['lines']:
                if 'key' in line:
                    print(f"{line['key']} = {line['value']}")
                else:
                    print(line['line'])
            input("\nDevam etmek için herhangi bir tuşa basın...")  # Kullanıcıya devam etme seçeneği
            continue

        if header_choice in ['quit', 'back']:
            return header_choice

        selected_header = data['headers'][header_choice]
        lines = [line for line in data['lines'] if line['header'] == selected_header]
        line_options = [f"{line['key']} = {line['value']}" if 'key' in line else line['line'] for line in lines]

        while True:
            display_menu(f"{selected_header} header'ının line'ları", line_options)
            line_choice = select_option("Line seçiniz", line_options)

            if line_choice in ['quit', 'back']:
                break

            selected_line = lines[line_choice]
            print(f"\nSeçilen line: {selected_line['key']}")

def main(decoded_text):
    data = parse_data(decoded_text)

    while True:
        display_menu("Ana Menü", ["Edit", "Read"])
        choice = select_option("Seçiminiz", ["Edit", "Read"])

        if choice == 'quit':
            print("Programdan çıkılıyor...")
            break
        elif choice == 'back':
            continue
        elif choice == 0:
            print("Edit seçeneği henüz desteklenmiyor.")
        elif choice == 1:
            read_mode_result = handle_read_mode(data)
            if read_mode_result == 'quit':
                break

if __name__ == "__main__":
    decoded_text = bitToText.main()  # bitToText'den decodedText'i alıyoruz
    main(decoded_text)  # decodedText'i ana fonksiyona gönderiyoruz