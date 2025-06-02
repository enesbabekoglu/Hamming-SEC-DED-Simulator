#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hamming SEC-DED Simülatörü için Sık Sorulan Sorular (FAQ) modülü
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QScrollArea, QWidget, QGroupBox, QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class FAQDialog(QDialog):
    """FAQ Penceresi"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hamming SEC-DED Simülatörü - Sık Sorulan Sorular")
        self.setMinimumSize(700, 600)
        self.setup_ui()

    def setup_ui(self):
        """Arayüzü oluşturur"""
        layout = QVBoxLayout(self)
        
        # Başlık
        title_label = QLabel("Hamming SEC-DED Simülatörü - Yardım ve FAQ")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # Tab widget
        tab_widget = QTabWidget()
        tab_widget.addTab(self.create_how_to_use_tab(), "Nasıl Kullanılır")
        tab_widget.addTab(self.create_how_it_works_tab(), "Nasıl Çalışır")
        tab_widget.addTab(self.create_faq_tab(), "Sık Sorulan Sorular")
        
        # Kapat butonu
        close_button = QPushButton("Kapat")
        close_button.clicked.connect(self.accept)
        
        layout.addWidget(title_label)
        layout.addWidget(tab_widget)
        layout.addWidget(close_button)
        
    def create_how_to_use_tab(self):
        """Nasıl Kullanılır sekmesini oluşturur"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        
        # Giriş
        intro = QGroupBox("Simülatör Kullanımı")
        intro_layout = QVBoxLayout()
        intro_text = """
        <h3>Simülatörün Temel Kullanımı</h3>
        <p>Hamming SEC-DED Simülatörü, veri iletimi sırasında oluşabilecek hataların tespiti ve düzeltilmesi için 
        kullanılan Hamming kodlarının çalışma prensiplerini görselleştiren bir uygulamadır.</p>
        
        <h3>Temel Adımlar</h3>
        <ol>
            <li><b>Veri Kodlama ve Belleğe Yazma</b>: Veriyi kodlayıp simüle edilmiş belleğe yazar</li>
            <li><b>Bellekten Okuma</b>: Bellekteki verileri okur ve görselleştirir</li>
            <li><b>Hata Enjekte Etme</b>: Kodlanmış veride hata oluşturarak hata senaryoları oluşturur</li>
            <li><b>Hata Tespiti ve Düzeltme</b>: Hamming kodunun hata tespiti ve düzeltme yeteneğini gösterir</li>
        </ol>
        """
        intro_label = QLabel(intro_text)
        intro_label.setWordWrap(True)
        intro_layout.addWidget(intro_label)
        intro.setLayout(intro_layout)
        
        # Adım adım kullanım
        steps = QGroupBox("Adım Adım Kullanım")
        steps_layout = QVBoxLayout()
        steps_text = """
        <h3>1. Bit Uzunluğu Seçimi</h3>
        <p>Açılır listeden 8, 16 veya 32 bit veri uzunluğunu seçin. Bu, kodlanacak veri bitlerinin sayısını belirler.</p>
        
        <h3>2. Veri Girişi</h3>
        <p>Veri giriş alanına ikili formatta (örn. 1010) veya onaltılık formatta (örn. 0x1A) veri girin. 
        Seçilen bit uzunluğundan daha büyük veriler otomatik olarak kesilir.</p>
        
        <h3>3. Bellek Adresi</h3>
        <p>Verinizin yazılacağı bellek adresini seçin (0-1023 arası).</p>
        
        <h3>4. Kodlama ve Belleğe Yazma</h3>
        <p>"Kodla ve Belleğe Yaz" düğmesine tıklayarak veriyi Hamming SEC-DED algoritması ile kodlayın 
        ve belleğe yazın. Kodlanmış veri bit görselleştirme panelinde renkli kutular olarak gösterilir.</p>
        
        <h3>5. Bellekten Okuma</h3>
        <p>Bir bellek adresi seçip "Bellekten Oku" düğmesine tıklayarak o adresteki kodlanmış veriyi görüntüleyin.</p>
        
        <h3>6. Hata Oluşturma</h3>
        <p>"Hata Oluştur" düğmesine tıklayarak gösterilen veride bir bit hatası oluşturun. 
        İletişim kutusunda hangi bit pozisyonunda hata oluşturmak istediğinizi belirleyin.</p>
        
        <h3>7. Hata Tespiti ve Düzeltme</h3>
        <p>"Hata Tespit/Düzelt" düğmesine tıklayarak Hamming algoritmasının hata tespiti ve 
        düzeltme işlemini gerçekleştirin. Sonuçlar bir iletişim kutusunda gösterilir.</p>
        """
        steps_label = QLabel(steps_text)
        steps_label.setWordWrap(True)
        steps_layout.addWidget(steps_label)
        steps.setLayout(steps_layout)
        
        # Arayüz bileşenleri
        ui = QGroupBox("Arayüz Bileşenleri")
        ui_layout = QVBoxLayout()
        ui_text = """
        <h3>Bit Görselleştirme Paneli</h3>
        <p>Bit kutuları şu renk kodlarına sahiptir:</p>
        <ul>
            <li><b>Açık Mavi</b>: Veri bitleri</li>
            <li><b>Açık Yeşil</b>: Parite bitleri</li>
            <li><b>Açık Sarı</b>: Genel parite biti</li>
            <li><b>Kırmızı</b>: Hata enjekte edilmiş bitler</li>
        </ul>
        
        <h3>Bellek Simülasyonu</h3>
        <p>Bellek tablosunda şu bilgiler görüntülenir:</p>
        <ul>
            <li><b>Adres</b>: Bellek adresi</li>
            <li><b>Kodlanmış Veri</b>: Hamming kodu ile kodlanmış veri (onaltılık)</li>
            <li><b>Orijinal Veri</b>: Kodlanmadan önceki orijinal veri (onaltılık)</li>
        </ul>
        
        <h3>İşlem Geçmişi</h3>
        <p>Gerçekleştirilen tüm işlemlerin kaydını tutar:</p>
        <ul>
            <li><b>İşlem</b>: Yapılan işlemin türü</li>
            <li><b>Durum</b>: İşlemin sonucu veya detayları</li>
            <li><b>Zaman</b>: İşlemin gerçekleştirildiği zaman</li>
        </ul>
        """
        ui_label = QLabel(ui_text)
        ui_label.setWordWrap(True)
        ui_layout.addWidget(ui_label)
        ui.setLayout(ui_layout)
        
        layout.addWidget(intro)
        layout.addWidget(steps)
        layout.addWidget(ui)
        layout.addStretch()
        
        scroll.setWidget(content)
        return scroll
        
    def create_how_it_works_tab(self):
        """Nasıl Çalışır sekmesini oluşturur"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        
        # Hamming Kod Teorisi
        theory = QGroupBox("Hamming Kod Teorisi")
        theory_layout = QVBoxLayout()
        theory_text = """
        <h3>Hamming Kodları Nedir?</h3>
        <p>Hamming kodları, 1950'lerde Richard Hamming tarafından geliştirilen ve veri iletimi sırasında 
        oluşabilecek hataların tespiti ve düzeltilmesi için kullanılan bir hata düzeltme kodudur.</p>
        
        <h3>SEC-DED (Single Error Correction - Double Error Detection)</h3>
        <p>Bu simülatörde kullanılan Hamming SEC-DED, tek bit hatalarını düzeltebilen ve çift bit hatalarını 
        tespit edebilen genişletilmiş bir Hamming kodudur.</p>
        
        <h3>Temel Çalışma Prensibi</h3>
        <p>Hamming kodları, veri içine belirli pozisyonlara ek parite bitleri ekleyerek çalışır. 
        Bu parite bitleri, belirli veri bitlerinin paritesini (çift/tek sayıda 1 olup olmadığını) kontrol eder.</p>
        <p>SEC-DED versiyonu, ek bir genel parite biti daha ekleyerek çift bit hatalarını tespit eder.</p>
        """
        theory_label = QLabel(theory_text)
        theory_label.setWordWrap(True)
        theory_layout.addWidget(theory_label)
        theory.setLayout(theory_layout)
        
        # Parite Bit Hesaplama
        parity = QGroupBox("Parite Bit Hesaplama")
        parity_layout = QVBoxLayout()
        parity_text = """
        <h3>Parite Bit Sayısı</h3>
        <p>m veri biti için gereken parite biti sayısı (r) şu eşitsizliği sağlamalıdır:</p>
        <p><b>2^r ≥ m + r + 1</b></p>
        <p>Yani:</p>
        <ul>
            <li>8 bit veri için 4 parite biti + 1 genel parite biti = 13 bit toplam</li>
            <li>16 bit veri için 5 parite biti + 1 genel parite biti = 22 bit toplam</li>
            <li>32 bit veri için 6 parite biti + 1 genel parite biti = 39 bit toplam</li>
        </ul>
        
        <h3>Parite Bitlerinin Pozisyonları</h3>
        <p>Parite bitleri 2'nin kuvvetleri olan pozisyonlara yerleştirilir: 1, 2, 4, 8, 16, 32, ...</p>
        <p>Genel parite biti genellikle en yüksek bitli pozisyona (örn. pozisyon 0) yerleştirilir.</p>
        
        <h3>Parite Biti Hesaplama</h3>
        <p>Her parite biti, belirli bir veri biti kümesinin paritesini kontrol eder:</p>
        <ul>
            <li>Parite bit 1: 1, 3, 5, 7, 9, ... pozisyonlarını kontrol eder</li>
            <li>Parite bit 2: 2, 3, 6, 7, 10, ... pozisyonlarını kontrol eder</li>
            <li>Parite bit 4: 4, 5, 6, 7, 12, ... pozisyonlarını kontrol eder</li>
            <li>Parite bit 8: 8, 9, 10, 11, ... pozisyonlarını kontrol eder</li>
            <li>Ve bu böyle devam eder</li>
        </ul>
        <p>Genel parite biti tüm bitlerin (kendisi dahil) paritesini kontrol eder.</p>
        """
        parity_label = QLabel(parity_text)
        parity_label.setWordWrap(True)
        parity_layout.addWidget(parity_label)
        parity.setLayout(parity_layout)
        
        # Hata Tespiti ve Düzeltme
        error = QGroupBox("Hata Tespiti ve Düzeltme")
        error_layout = QVBoxLayout()
        error_text = """
        <h3>Hata Tespiti</h3>
        <p>Hamming SEC-DED kodu, şu şekilde hataları tespit eder:</p>
        <ol>
            <li>Alıcı, her parite bit için parite hesaplar ve hatalı olanları belirler.</li>
            <li>Hatalı parite bitleri, 'sendrom' olarak adlandırılan bir değer oluşturur.</li>
            <li>Genel parite biti ayrıca kontrol edilir.</li>
        </ol>
        
        <h3>Hata Düzeltme</h3>
        <p>Hata tespiti sonuçlarına göre:</p>
        <ul>
            <li><b>Genel parite doğru, sendrom sıfır</b>: Hata yok</li>
            <li><b>Genel parite yanlış, sendrom sıfır değil</b>: Tek bit hatası var, sendrom değeri hatalı bitin pozisyonunu gösterir</li>
            <li><b>Genel parite doğru, sendrom sıfır değil</b>: Çift bit hatası tespit edildi, düzeltilemiyor</li>
            <li><b>Genel parite yanlış, sendrom sıfır</b>: Genel parite bitinde hata var</li>
        </ul>
        
        <h3>Simülatörde Görselleştirme</h3>
        <p>Bu simülatör, Hamming SEC-DED kodlaması ve hata tespiti/düzeltme sürecini adım adım görselleştirir:</p>
        <ul>
            <li>Veri ve parite bitleri farklı renklerle gösterilir</li>
            <li>Hata enjekte edilmiş bitler kırmızı renkte gösterilir</li>
            <li>Hata tespiti ve düzeltme sonuçları ayrıntılı olarak raporlanır</li>
        </ul>
        """
        error_label = QLabel(error_text)
        error_label.setWordWrap(True)
        error_layout.addWidget(error_label)
        error.setLayout(error_layout)
        
        layout.addWidget(theory)
        layout.addWidget(parity)
        layout.addWidget(error)
        layout.addStretch()
        
        scroll.setWidget(content)
        return scroll
    
    def create_faq_tab(self):
        """Sık Sorulan Sorular sekmesini oluşturur"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        
        faq = QGroupBox("Sık Sorulan Sorular")
        faq_layout = QVBoxLayout()
        faq_text = """
        <h3>Soru: Hamming kodu ne için kullanılır?</h3>
        <p>Cevap: Hamming kodları, veri iletişimi ve depolama sistemlerinde hata tespiti ve düzeltme için kullanılır. 
        Bilgisayar belleği, iletişim kanalları ve uzay araçları gibi çeşitli uygulamalarda güvenilir veri iletimi sağlar.</p>
        
        <h3>Soru: Hamming SEC-DED, kaç tane bit hatasını düzeltebilir?</h3>
        <p>Cevap: Hamming SEC-DED (Single Error Correction - Double Error Detection) tek bit hatalarını 
        düzeltebilir ve çift bit hatalarını tespit edebilir ancak çift bit hatalarını düzeltemez.</p>
        
        <h3>Soru: Parite bitleri nedir ve nasıl çalışır?</h3>
        <p>Cevap: Parite bitleri, belirli bir veri biti grubunun paritesini (içindeki 1'lerin sayısının çift 
        veya tek olması) kontrol eden ek bitlerdir. Veri iletildiğinde, alıcı parite bitlerini tekrar hesaplar 
        ve orijinal parite bitleriyle karşılaştırır. Herhangi bir uyuşmazlık, bir hata olduğunu gösterir.</p>
        
        <h3>Soru: SEC-DED kodlamasındaki genel parite biti ne işe yarar?</h3>
        <p>Cevap: Genel parite biti, tüm veri ve parite bitlerinin genel paritesini kontrol eder. 
        Bu ek bit, çift bit hatalarının tespitini mümkün kılar (bu olmadan Hamming kodu çift bit hatalarını 
        tespit edemez, yanlış bir şekilde düzeltme yapabilir).</p>
        
        <h3>Soru: Hamming SEC-DED kodu gerçek dünyada nerede kullanılır?</h3>
        <p>Cevap: Hamming SEC-DED kodları, ECC (Error Correcting Code) bellekler, veri iletişim sistemleri, 
        uydu iletişimi ve uzay araçları gibi hata toleranslı sistemlerde yaygın olarak kullanılır.</p>
        
        <h3>Soru: Veri uzunluğunu (8/16/32 bit) değiştirdiğimde ne olur?</h3>
        <p>Cevap: Veri uzunluğunu değiştirmek, kodlama için gereken parite bit sayısını değiştirir. 
        Daha büyük veri uzunlukları, daha fazla parite biti gerektirir ve toplam bit sayısı artar.</p>
        
        <h3>Soru: Hamming kodu ile Reed-Solomon gibi diğer hata düzeltme kodları arasındaki fark nedir?</h3>
        <p>Cevap: Hamming kodları, tek bit hatalarını düzeltmek için optimize edilmiştir ve nispeten basittir. 
        Reed-Solomon gibi daha karmaşık kodlar, çoklu bit hatalarını düzeltebilir ve daha yüksek hata düzeltme 
        kapasitesine sahiptir, ancak daha fazla hesaplama gerektirir.</p>
        
        <h3>Soru: Bu simülatör ne öğretiyor?</h3>
        <p>Cevap: Bu simülatör, Hamming SEC-DED kodlamasının temel prensiplerini, parite bit hesaplamalarını, 
        hata enjeksiyonunu ve hata tespiti/düzeltme mekanizmalarını görsel olarak anlamanıza yardımcı olur.</p>
        """
        faq_label = QLabel(faq_text)
        faq_label.setWordWrap(True)
        faq_layout.addWidget(faq_label)
        faq.setLayout(faq_layout)
        
        layout.addWidget(faq)
        layout.addStretch()
        
        scroll.setWidget(content)
        return scroll
