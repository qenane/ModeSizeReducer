# main.py

import bitToText  # bitToText.py dosyasını içe aktarır
import compression  # compression.py dosyasını içe aktarır
import textToBit  # textToBit.py dosyasını içe aktarır

def main():
    # 1. Metni ikili (binary) veriye çevirme
    textToBit.main()

    # 2. Sıkıştırma işlemi
    compression.main()

    # 3. İkili veriyi tekrar metne çevirme
    bitToText.main()

if __name__ == "__main__":
    main()
