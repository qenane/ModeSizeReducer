import textToBit
import bitToText
import compression
import menuChoices

def main():
    # 1. Metni ikili (binary) veriye çevirme
    textToBit.main()

    # 2. Sıkıştırma işlemi
    compression.main()
    
    # 3. İkili veriyi tekrar metne çevirme ve decodedText'i alma
    decodedText = bitToText.main()

    # 4. Kullanıcıya terminal menüsünü gösterme
    menuChoices.main(decodedText)

if __name__ == "__main__":
    main()
