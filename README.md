# Hamming SEC-DED Simülatörü

Bu uygulama, Hamming SEC-DED (Single Error Correction - Double Error Detection) kodlamasını ve hata düzeltme işlemlerini görselleştirir ve simüle eder. Kullanıcılar 8, 16 veya 32 bitlik verileri kodlayabilir, belleğe yazabilir, yapay hatalar oluşturabilir ve düzeltebilir.

## Özellikler

- **Bit Uzunluğu Seçimi**: 8, 16 veya 32 bit veri kodlama
- **Veri Girişi**: İkili (0101...) veya hexadecimal (0x...) formatında veri girişi
- **Bellek Simülasyonu**: Verileri simüle edilmiş bir bellekte saklama ve okuma
- **Hata Simülasyonu**: İstenen bit pozisyonunda hata enjekte etme
- **Hata Tespiti ve Düzeltme**: Hamming SEC-DED ile hataları tespit etme ve düzeltme
- **Görselleştirme**: Bit pozisyonlarının ve değerlerinin renkli gösterimi
- **İşlem Geçmişi**: Yapılan işlemlerin kaydını tutma

## Kurulum

1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2. Uygulamayı çalıştırın:
   ```bash
   python main.py
   ```

## Kullanım

1. **Veri Kodlama ve Belleğe Yazma**:
   - Bit uzunluğu seçin (8, 16, 32)
   - Veri girişi yapın (ikili veya hex formatında)
   - Bellek adresi seçin
   - "Kodla ve Belleğe Yaz" butonuna tıklayın

2. **Bellekten Okuma**:
   - Okumak istediğiniz bellek adresini seçin
   - "Bellekten Oku" butonuna tıklayın

3. **Hata Oluşturma**:
   - Mevcut veri gösterilirken "Hata Oluştur" butonuna tıklayın
   - Hata enjekte etmek istediğiniz bit pozisyonunu girin

4. **Hata Tespiti ve Düzeltme**:
   - "Hata Tespit/Düzelt" butonuna tıklayın
   - Sonuçları görüntüleyin

## Hamming SEC-DED Kodlaması Hakkında

Hamming SEC-DED kodlaması, tek bit hatalarını düzeltme ve çift bit hatalarını tespit etme yeteneğine sahip bir hata düzeltme kodudur. 

- **Parite Biti Hesaplama**: 2^r ≥ m + r + 1 (m = veri biti sayısı, r = parite biti sayısı)
- **Veri Bitleri**: Parite bitlerinin pozisyonları dışındaki konumlara yerleştirilir
- **Parite Bitleri**: 2'nin kuvveti olan pozisyonlara yerleştirilir (1, 2, 4, 8, ...)
- **Genel Parite Biti**: Çift/tek parite kontrolü yapar, çift hataları tespit etmek için eklenir

## Teknik Detaylar

- **PyQt5**: Grafik kullanıcı arayüzü
- **Python**: Algoritma ve işlev implementasyonu
- **Hamming Kodlayıcı**: 8, 16 ve 32 bit destekler

## Lisans

Bu uygulama açık kaynaklıdır ve eğitim amaçlı kullanım için serbestçe dağıtılabilir.
