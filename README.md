# Hamming Error-Correcting Code Simülatörü

BLM230 Bilgisayar Mimarisi proje ödevi için standart **Hamming Error-Correcting Code** simülatörü. 8, 16 ve 32 bit veriler kodlanır, bellekte simüle edilir, yapay tek bit hatası oluşturulur; sendrom ile hata teyit edilip düzeltilir ve **Data Out** gösterilir.

## Özellikler

- 8 / 16 / 32 bit veri uzunluğu
- Hamming kodlama ve bellek simülasyonu (adres tablosu)
- 1 tabanlı bit numaralandırma (bit 1 = sağ uç)
- Yapay hata enjeksiyonu, sendrom kelimesi, teyit, Error Signal, Data Out
- Renkli bit görselleştirme ve işlem geçmişi

## Kurulum

```bash
cd Hamming-SEC-DED-Simulator
pip3 install -r requirements.txt
python3 main.py
```

> macOS’ta `PyQt5==5.15.7` derleme hatası verirse `requirements.txt` zaten wheel sürümü (`>=5.15.10`) kullanır.

### macOS — çift tıkla başlatma

`start_hamming.command` dosyasına çift tıklayın.

“Erişim ayrıcalıkları” uyarısı çıkarsa:

```bash
chmod +x start_hamming.command
xattr -cr start_hamming.command
```

İlk seferde sağ tık → **Aç** de kullanılabilir.

## Kullanım (kısa akış)

1. **Bit Uzunluğu** ve **Veri Girişi** (seçilen uzunlukta ikili)
2. **Bellek Adresi** → **Kodla ve Belleğe Yaz**
3. **Hata Oluştur** → bit pozisyonu (1 tabanlı)
4. **Hata Tespit/Düzelt** → sendrom paneli ve Data Out

İsteğe bağlı: **Bellekten Oku**, **Yardım ve S.S.S.**

## Test senaryoları

Her test: **Kodla ve Belleğe Yaz** → **Hata Oluştur** → **Hata Tespit/Düzelt**.  
Beklenen: **Teyit** başarılı, **Data Out** = giriş verisi. Testler arasında farklı bellek adresi kullanın.

### Test 1 — 8 bit

| Alan | Değer |
|------|--------|
| Bit Uzunluğu | `8 bit` |
| Veri Girişi | `10110010` |
| Bellek Adresi | `0` |
| Hamming uzunluğu | 12 bit |
| Yapay hata (bit no) | `6` |

**Beklenen:** Sendrom ondalık `6`, Data Out `10110010`.

### Test 2 — 16 bit

| Alan | Değer |
|------|--------|
| Bit Uzunluğu | `16 bit` |
| Veri Girişi | `1011001010110010` |
| Bellek Adresi | `1` |
| Hamming uzunluğu | 21 bit |
| Yapay hata (bit no) | `10` |

**Beklenen:** Sendrom ondalık `10`, Data Out `1011001010110010`.

### Test 3 — 32 bit

| Alan | Değer |
|------|--------|
| Bit Uzunluğu | `32 bit` |
| Veri Girişi | `10110010101100101011001010110010` |
| Bellek Adresi | `2` |
| Hamming uzunluğu | 38 bit |
| Yapay hata (bit no) | `15` |

**Beklenen:** Sendrom ondalık `15`, Data Out girişteki 32 bit ile aynı.

### Test kontrol listesi

- [ ] Veri uzunluğu tam (8 / 16 / 32 karakter)
- [ ] Kodlama sonrası bellek tablosunda satır görünüyor
- [ ] Hatalı bit kırmızı; “Kullanıcının Bozduğu Bit” doğru
- [ ] Sendrom ondalık = bozulan bit
- [ ] Data Out = Data In
- [ ] Üç test sonunda bellekte adres 0, 1, 2 dolu

Demo videosu için adım adım rehber: [`docs/demo-sessiz-adimlar.md`](docs/demo-sessiz-adimlar.md)

## Hamming kodu (özet)

- Parite sayısı: 2^r ≥ m + r + 1
- Parite pozisyonları: 1, 2, 4, 8, 16, …
- Toplam kod uzunluğu: 8→12, 16→21, 32→38 bit
- Sendrom 0 → hata yok; aksi halde hatalı bitin 1 tabanlı pozisyonu

## Proje dosyaları

| Dosya | Açıklama |
|-------|----------|
| `main.py` | Giriş noktası |
| `ui.py` | PyQt5 arayüz |
| `hamming_codec.py` | Kodlama / sendrom / düzeltme |
| `faq.py` | Yardım penceresi |
| `start_hamming.command` | macOS başlatıcı |

## Lisans

Eğitim amaçlı kullanım için açık kaynaklıdır.
