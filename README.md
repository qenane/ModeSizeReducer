# RST_ModeSizeReducer
Yazılımın çalışması için kullanılan bilgisayarda 7zip'in PATH'e eklenmiş olması lazım.(Linux sistemde gerek yok.)
7zip kullanmamın sebebidaha fazla sıkıştırma sağlayabilmek ve linuxta kullandığım bazı diğer çözümleri windowsa uyumlu hale getirememek.(İstek doğrultusunda yöntemler değişebilir. Boyut azalmasını -belki- artırabilecek bazı fikirlerim var istenirse deneyebilirim.)

Programın kullanılışı:
Programın bulunduğu dizine dosya boyutunu düşürmek istenilen .ini dosyaları yüklenir.
Programda main.py dosyası çalıştırılıp "dizindeki .ini dosyalarıyla işlem yap" seçeneği seçildiği an tüm .ini dosyaları küçültülerek .7z dosyalarına dönüşür.
Daha sonra edit seçeneği seçilerek dosya içeriği değiştirilebilir.
"dizindeki 7z dosyalarıyla işlem yap" seçeneği seçildiğinde ise dizinde hali hazırda boyutu azaltılmış dosya bulunuyorsa bunlar arasındans seçim yapılarak işlem gerçekleştirilebilir. 


Dizin içerisinde deneme amaçlı 3 tane birbirinden farklı .ini dosyası var. Header olarak tanımladığım satırlar bulunmayan .ini dosyaları 7z formatına dönüştürülmüyor.
Programın içine aynı isimde dosya atıldığında sıkıştırılmış dosyanın üstüne yazar eğer önceki dosyaların korunmasını istiyorsanız başka bir klasöre taşıyın.


Not : Bazı kısımlarda(programdan çıkış veya üst menüye dönüş gibi) error handling yapmadım. Programın çalışmasını ve işlevlerini engellemiyor.
Bu tarz şeylerle alakalı düzenleme veya geliştirme yapmamı isterseniz bana ulaşabilirsiniz. Eksik bulduğunuz noktalarda feedback verirseniz sevinirim.

kerciyes66@gmail.com