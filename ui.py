#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hamming Error-Correcting Code Simülatörü için PyQt5 tabanlı kullanıcı arayüzü
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QGroupBox, QGridLayout,
                             QMessageBox, QSpinBox, QFrame, QScrollArea)
from PyQt5.QtCore import Qt

# Hamming kodlayıcı modülünü içe aktar
from hamming_codec import HammingCodec

# FAQ modülünü içe aktar
from faq import FAQDialog

# Ana pencere sınıfı
class HammingSimulatorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Ana pencere ayarları
        self.setWindowTitle("Hamming Error-Correcting Code Simülatörü - Enes Babekoğlu")
        self.setGeometry(100, 100, 1024, 768)
        
        # Ana widget ve düzen
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Hamming kodlayıcı
        self.bit_length = 16  # Varsayılan 16 bit
        self.codec = HammingCodec(self.bit_length)
        
        # Durum bilgisi
        self.current_data = {
            'original': None,    # Orijinal veri
            'encoded': None,     # Kodlanmış veri
            'address': None,     # Bellek adresi
            'error_position': None  # Hata pozisyonu
        }
        
        # Bellek (simüle edilmiş)
        self.memory = {}
        
        # Kontrol paneli
        self.create_control_panel()
        
        # Bit görselleştirme paneli
        self.create_bit_panel()
        
        # Bellek simülasyonu paneli
        self.create_memory_panel()

        # Sendrom ve düzeltme sonucu paneli
        self.create_syndrome_panel()
        
        # Geçmiş paneli
        self.create_history_panel()
        
        # Sinyal bağlantıları
        self.connect_signals()
        
        # Bit kutularını oluştur
        self.create_bit_boxes(self.codec.total_bits)
        
        # Durum çubuğu
        self.statusBar().showMessage("Hazır")
        
        # Bellek simülasyonu (adres:veri şeklinde sözlük)
        self.memory = {}
        
    def create_control_panel(self):
        """Kontrol panelini oluşturur: Bit seçimi ve veri girişi"""
        control_group = QGroupBox("Kontrol Paneli")
        control_layout = QGridLayout()
        
        # Bit uzunluğu seçimi
        bit_label = QLabel("Bit Uzunluğu:")
        self.bit_combo = QComboBox()
        self.bit_combo.addItems(["8 bit", "16 bit", "32 bit"])
        self.bit_combo.setCurrentIndex(1)  # Varsayılan 16 bit
        
        # Veri girişi (ikili veya hex)
        data_label = QLabel("Veri Girişi:")
        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText("Seçilen uzunlukta ikili veri girin (örn. 10110010)")
        
        # Adres alanı
        addr_label = QLabel("Bellek Adresi:")
        self.addr_input = QSpinBox()
        self.addr_input.setRange(0, 1023)  # 0-1023 arası adresler
        
        # Butonlar
        self.encode_button = QPushButton("Kodla ve Belleğe Yaz")
        self.read_button = QPushButton("Bellekten Oku")
        self.error_inject_button = QPushButton("Hata Oluştur")
        self.error_correct_button = QPushButton("Hata Tespit/Düzelt")
        
        # FAQ butonu
        self.faq_button = QPushButton("Yardım ve S.S.S.")
        
        # Düzene yerleştir
        control_layout.addWidget(bit_label, 0, 0)
        control_layout.addWidget(self.bit_combo, 0, 1)
        control_layout.addWidget(data_label, 1, 0)
        control_layout.addWidget(self.data_input, 1, 1, 1, 3)
        control_layout.addWidget(addr_label, 2, 0)
        control_layout.addWidget(self.addr_input, 2, 1)
        control_layout.addWidget(self.encode_button, 3, 0)
        control_layout.addWidget(self.read_button, 3, 1)
        control_layout.addWidget(self.error_inject_button, 3, 2)
        control_layout.addWidget(self.error_correct_button, 3, 3)
        control_layout.addWidget(self.faq_button, 4, 0, 1, 4)
        
        control_group.setLayout(control_layout)
        self.main_layout.addWidget(control_group)
        
    def create_bit_panel(self):
        """Bitleri gösteren paneli oluşturur"""
        bit_group = QGroupBox("Bit Görselleştirme")
        bit_layout_main = QVBoxLayout()
        
        # Bilgi etiketi
        info_layout = QHBoxLayout()
        bit_info = QLabel("Renkler: ")
        data_bit_sample = QLabel("Veri")
        data_bit_sample.setStyleSheet("background-color: #a0d0ff; padding: 2px 8px; border-radius: 4px; font-weight: bold;")
        parity_bit_sample = QLabel("Parite")
        parity_bit_sample.setStyleSheet("background-color: #a0ffa0; padding: 2px 8px; border-radius: 4px; font-weight: bold;")
        error_bit_sample = QLabel("Hatalı")
        error_bit_sample.setStyleSheet("background-color: #ff8080; padding: 2px 8px; border-radius: 4px; font-weight: bold;")
        numbering_info = QLabel("Bit numarası: soldan sağa N ... 1, bit 1 sağ uçtadır.")
        numbering_info.setStyleSheet("color: #555;")
        
        info_layout.addWidget(bit_info)
        info_layout.addWidget(data_bit_sample)
        info_layout.addWidget(parity_bit_sample)
        info_layout.addWidget(error_bit_sample)
        info_layout.addWidget(numbering_info)
        info_layout.addStretch()
        
        self.bit_scroll = QScrollArea()
        self.bit_scroll.setWidgetResizable(True)
        self.bit_scroll.setMinimumHeight(130)  # Minimum yükseklik
        
        self.bit_container = QWidget()
        self.bit_layout = QHBoxLayout(self.bit_container)
        self.bit_layout.setAlignment(Qt.AlignLeft)
        self.bit_layout.setSpacing(8)  # Kutular arası boşluk
        self.bit_layout.setContentsMargins(10, 10, 10, 10)  # Kenar boşlukları
        
        self.bit_scroll.setWidget(self.bit_container)
        
        bit_layout_main.addLayout(info_layout)
        bit_layout_main.addWidget(self.bit_scroll)
        
        bit_group.setLayout(bit_layout_main)
        self.main_layout.addWidget(bit_group)
        
    def create_memory_panel(self):
        """Bellek simülasyonu panelini oluşturur"""
        memory_group = QGroupBox("Bellek Simülasyonu")
        memory_layout = QVBoxLayout()
        
        # Değer etiketleri
        labels_layout = QHBoxLayout()
        
        data_label = QLabel("Data In / Orijinal Veri:")
        self.data_value_label = QLabel("0")
        data_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.data_value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        encoded_label = QLabel("Hamming Kodu:")
        self.encoded_value_label = QLabel("0")
        encoded_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.encoded_value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        labels_layout.addWidget(data_label)
        labels_layout.addWidget(self.data_value_label)
        labels_layout.addStretch()
        labels_layout.addWidget(encoded_label)
        labels_layout.addWidget(self.encoded_value_label)
        
        # Bellek tablosu
        self.memory_table = QTableWidget(0, 4)
        self.memory_table.setHorizontalHeaderLabels(["Adres", "Veri Bitleri", "Hamming Kodu", "Uzunluk"])
        self.memory_table.horizontalHeader().setStretchLastSection(True)
        self.memory_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        memory_layout.addLayout(labels_layout)
        memory_layout.addWidget(self.memory_table)
        memory_group.setLayout(memory_layout)
        self.main_layout.addWidget(memory_group)

    def create_syndrome_panel(self):
        """Sendrom, hata teyidi ve Data Out alanlarını oluşturur."""
        syndrome_group = QGroupBox("Sendrom, Compare ve Corrector")
        syndrome_layout = QGridLayout()

        self.syndrome_word_label = QLabel("-")
        self.syndrome_decimal_label = QLabel("-")
        self.detected_bit_label = QLabel("-")
        self.injected_bit_label = QLabel("-")
        self.confirmation_label = QLabel("-")
        self.data_out_label = QLabel("-")
        self.error_signal_label = QLabel("-")

        syndrome_layout.addWidget(QLabel("Sendrom Kelimesi:"), 0, 0)
        syndrome_layout.addWidget(self.syndrome_word_label, 0, 1)
        syndrome_layout.addWidget(QLabel("Ondalık Karşılığı:"), 0, 2)
        syndrome_layout.addWidget(self.syndrome_decimal_label, 0, 3)
        syndrome_layout.addWidget(QLabel("Tespit Edilen Bit:"), 1, 0)
        syndrome_layout.addWidget(self.detected_bit_label, 1, 1)
        syndrome_layout.addWidget(QLabel("Kullanıcının Bozduğu Bit:"), 1, 2)
        syndrome_layout.addWidget(self.injected_bit_label, 1, 3)
        syndrome_layout.addWidget(QLabel("Teyit:"), 2, 0)
        syndrome_layout.addWidget(self.confirmation_label, 2, 1, 1, 3)
        syndrome_layout.addWidget(QLabel("Data Out:"), 3, 0)
        syndrome_layout.addWidget(self.data_out_label, 3, 1)
        syndrome_layout.addWidget(QLabel("Error Signal:"), 3, 2)
        syndrome_layout.addWidget(self.error_signal_label, 3, 3)

        syndrome_group.setLayout(syndrome_layout)
        self.main_layout.addWidget(syndrome_group)
        
    def create_history_panel(self):
        """İşlem geçmişi panelini oluşturur"""
        history_group = QGroupBox("İşlem Geçmişi")
        history_layout = QVBoxLayout()
        
        # Geçmiş tablosu
        self.history_table = QTableWidget(0, 4)
        self.history_table.setHorizontalHeaderLabels(["#", "İşlem", "Durum", "Zaman"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setMinimumHeight(100)
        
        # Telif hakkı etiketi
        copyright_label = QLabel(" 2026 Enes Babekoğlu - Hamming Error-Correcting Code Simülatörü")
        copyright_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        copyright_label.setStyleSheet("color: gray; font-size: 10px;")
        
        history_layout.addWidget(self.history_table)
        history_layout.addWidget(copyright_label)
        history_group.setLayout(history_layout)
        self.main_layout.addWidget(history_group)
    
    def create_bit_boxes(self, total_bits):
        """Belirtilen bit sayısı kadar bit kutuları oluşturur"""
        # Önceki kutuları temizle
        for i in reversed(range(self.bit_layout.count())): 
            widget = self.bit_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        
        self.bit_boxes = []
        
        data_positions = [
            pos for pos in range(1, total_bits + 1)
            if not self.codec._is_power_of_two(pos)
        ]
        data_index_by_position = {
            position: index + 1
            for index, position in enumerate(data_positions)
        }

        # Kutular ödevdeki tablo gibi soldan sağa N ... 1 olarak gösterilir.
        for position in range(total_bits, 0, -1):
            bit_frame = QFrame()
            bit_frame.setFrameShape(QFrame.NoFrame)
            bit_frame.setFixedSize(50, 70)  # Daha büyük kutular
            
            # Bit için düzen oluştur
            layout = QVBoxLayout(bit_frame)
            layout.setContentsMargins(2, 2, 2, 2)
            layout.setSpacing(0)
            
            # Bit pozisyon etiketi
            pos_label = QLabel(str(position))
            pos_label.setAlignment(Qt.AlignCenter)
            pos_label.setStyleSheet("font-size: 10px; color: #666; margin-bottom: 2px;")
            
            # Bit değeri için kutu
            bit_value_frame = QFrame()
            bit_value_frame.setFixedSize(40, 40)
            bit_value_frame.setFrameShape(QFrame.Box)
            bit_value_frame.setFrameShadow(QFrame.Raised)
            bit_value_frame.setLineWidth(1)
            
            # Bit değeri etiketi
            value_layout = QVBoxLayout(bit_value_frame)
            value_layout.setContentsMargins(0, 0, 0, 0)
            bit_label = QLabel('0')
            bit_label.setAlignment(Qt.AlignCenter)
            bit_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            value_layout.addWidget(bit_label)
            
            if self.codec._is_power_of_two(position):
                bit_type = 'parity'
                type_text = f"P{position}"
                bit_value_frame.setStyleSheet('background-color: #a0ffa0; border-radius: 6px; border: 1px solid #00c000;')  # Açık yeşil
            else:
                bit_type = 'data'
                type_text = f"D{data_index_by_position[position]}"
                bit_value_frame.setStyleSheet('background-color: #a0d0ff; border-radius: 6px; border: 1px solid #0080ff;')  # Açık mavi
            
            type_label = QLabel(type_text)
            type_label.setAlignment(Qt.AlignCenter)
            type_label.setStyleSheet("font-size: 10px; color: #333; margin-top: 2px;")
            
            # Düzene ekle
            layout.addWidget(pos_label)
            layout.addWidget(bit_value_frame)
            layout.addWidget(type_label)
            
            # Bit kutusu bilgilerini sakla
            self.bit_boxes.append({
                'frame': bit_frame,
                'value_frame': bit_value_frame,
                'label': bit_label,
                'position': position,
                'type': bit_type,
                'value': 0
            })
            
            # Bit kutusunu düzene ekle
            self.bit_layout.addWidget(bit_frame)
    
    def update_bit_display(self, encoded_value=None, error_position=None):
        """Bit kutularını günceller"""
        if encoded_value is None:
            encoded_value = self.current_data.get('encoded')

        if encoded_value is None:
            encoded_value = 0
        
        # Her bit için değeri güncelle
        for bit_box in self.bit_boxes:
            position = bit_box['position']
            value = 1 if encoded_value & (1 << (position - 1)) else 0
            bit_box['value'] = value
            bit_box['label'].setText(str(value))

            # Hata enjekte edilmiş biti kırmızı yap
            if error_position is not None and position == error_position:
                bit_box['value_frame'].setStyleSheet('background-color: #ff8080; border-radius: 6px; border: 1px solid #d00000;')  # Kırmızı
                bit_box['label'].setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
            else:
                # Normal renkler
                if bit_box['type'] == 'parity':
                    bit_box['value_frame'].setStyleSheet('background-color: #a0ffa0; border-radius: 6px; border: 1px solid #00c000;')  # Açık yeşil
                else:
                    bit_box['value_frame'].setStyleSheet('background-color: #a0d0ff; border-radius: 6px; border: 1px solid #0080ff;')  # Açık mavi
                bit_box['label'].setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
    
    def add_history_item(self, operation, status):
        """Geçmiş tablosuna yeni bir giriş ekler"""
        row = self.history_table.rowCount()
        self.history_table.insertRow(row)
        
        # Sıra numarası
        self.history_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        
        # İşlem
        self.history_table.setItem(row, 1, QTableWidgetItem(operation))
        
        # Durum
        self.history_table.setItem(row, 2, QTableWidgetItem(status))
        
        # Zaman
        import datetime
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.history_table.setItem(row, 3, QTableWidgetItem(now))
        
        # Son eklenen satıra kaydır
        self.history_table.scrollToBottom()

    def format_data_value(self, value):
        """Veri alanını seçili veri uzunluğunda ikili biçimde döndürür."""
        if value is None:
            return "-"
        return bin(value)[2:].zfill(self.codec.data_bits)

    def format_encoded_value(self, value):
        """Kod kelimesini seçili Hamming uzunluğunda ikili biçimde döndürür."""
        if value is None:
            return "-"
        return self.codec.get_bit_string(value)

    def update_value_labels(self, data_value=None, encoded_value=None):
        """Bellek panelindeki Data In ve Hamming kodu etiketlerini günceller."""
        self.data_value_label.setText(self.format_data_value(data_value))
        self.encoded_value_label.setText(self.format_encoded_value(encoded_value))

    def reset_syndrome_panel(self):
        """Sendrom panelini başlangıç durumuna döndürür."""
        self.syndrome_word_label.setText("-")
        self.syndrome_decimal_label.setText("-")
        self.detected_bit_label.setText("-")
        self.injected_bit_label.setText("-")
        self.confirmation_label.setText("-")
        self.data_out_label.setText("-")
        self.error_signal_label.setText("-")

    def update_syndrome_panel(self, result, injected_position=None):
        """Hata tespiti sonucunu sendrom paneline yansıtır."""
        detected_position = result.get('error_position')
        data_out = self.format_data_value(result.get('original_data'))

        self.syndrome_word_label.setText(result.get('syndrome_bits', "-"))
        self.syndrome_decimal_label.setText(str(result.get('syndrome', "-")))
        self.detected_bit_label.setText(str(detected_position) if detected_position is not None else "-")
        self.injected_bit_label.setText(str(injected_position) if injected_position is not None else "-")
        self.data_out_label.setText(data_out)

        if result['error_type'] == 'none':
            self.error_signal_label.setText("0 - hata yok")
            self.confirmation_label.setText("Hata yok; Data Out, Data In ile aynı.")
        elif result['error_type'] == 'single':
            self.error_signal_label.setText("1 - tek bit hatası")
            if injected_position is None:
                self.confirmation_label.setText("Tek bit hatası tespit edildi ve düzeltildi.")
            elif injected_position == detected_position:
                self.confirmation_label.setText("Hata doğru tespit edildi.")
            else:
                self.confirmation_label.setText("Tespit edilen bit, yapay hata bitiyle uyuşmuyor.")
        else:
            self.error_signal_label.setText("1 - belirsiz hata")
            self.confirmation_label.setText("Sendrom geçerli bit aralığı dışında; düzeltme yapılmadı.")
    
    def update_memory_table(self):
        """Bellek tablosunu günceller"""
        # Tabloyu temizle
        self.memory_table.setRowCount(0)
        
        # Bellek içeriğini tabloya ekle
        for addr, data in sorted(self.memory.items()):
            row = self.memory_table.rowCount()
            self.memory_table.insertRow(row)
            
            # Adres
            self.memory_table.setItem(row, 0, QTableWidgetItem(str(addr)))
            
            data_bits = data.get('data_bits', self.bit_length)
            row_codec = HammingCodec(data_bits)

            self.memory_table.setItem(row, 1, QTableWidgetItem(bin(data['original'])[2:].zfill(data_bits)))
            self.memory_table.setItem(row, 2, QTableWidgetItem(row_codec.get_bit_string(data['encoded'])))
            self.memory_table.setItem(row, 3, QTableWidgetItem(f"{data_bits} bit"))
        
        # Son eklenen satıra kaydır
        if self.memory_table.rowCount() > 0:
            self.memory_table.scrollToBottom()
            
    def connect_signals(self):
        """Buton ve diğer kontroller için sinyal bağlantılarını oluşturur"""
        # Bit uzunluğu değiştiğinde
        self.bit_combo.currentIndexChanged.connect(self.bit_length_changed)
        
        # Butonlar için
        self.encode_button.clicked.connect(self.encode_and_write_memory)
        self.read_button.clicked.connect(self.read_from_memory)
        self.error_inject_button.clicked.connect(self.inject_error)
        self.error_correct_button.clicked.connect(self.detect_and_correct_error)
        self.faq_button.clicked.connect(self.show_faq)
    
    def bit_length_changed(self):
        """Bit uzunluğu değiştiğinde Hamming kodlayıcıyı günceller"""
        index = self.bit_combo.currentIndex()
        
        # Bit uzunluğunu ayarla
        if index == 0:
            self.bit_length = 8
        elif index == 1:
            self.bit_length = 16
        else:
            self.bit_length = 32
        
        # Codec'i yeniden oluştur
        self.codec = HammingCodec(self.bit_length)
        
        # Bit kutularını yeniden oluştur
        self.create_bit_boxes(self.codec.total_bits)
        
        # Sıfır değeri göster
        self.current_data = {
            'original': None,
            'encoded': None,
            'address': None,
            'error_position': None
        }
        self.update_bit_display(0)
        self.update_value_labels()
        self.reset_syndrome_panel()
        self.data_input.setPlaceholderText(
            f"{self.bit_length} bit ikili veri girin (örn. {'0' * self.bit_length})"
        )
            
    def parse_data_input(self):
        """Kullanıcının girdiği veriyi işler"""
        data_str = self.data_input.text().strip()

        if not data_str:
            QMessageBox.critical(self, "Hata", "Veri girişi boş olamaz.")
            return None
        
        try:
            # Hex girişi (0x ile başlıyorsa)
            if data_str.startswith("0x") or data_str.startswith("0X"):
                value = int(data_str, 16)
            # İkili giriş
            else:
                if any(c not in '01' for c in data_str):
                    raise ValueError("İkili veri yalnızca 0 ve 1 karakterlerinden oluşmalıdır.")
                if len(data_str) != self.codec.data_bits:
                    raise ValueError(
                        f"{self.codec.data_bits} bit seçiliyken tam {self.codec.data_bits} karakter girilmelidir."
                    )
                value = int(data_str, 2)
                
            # Veriyi bit sınırına göre kontrol et
            if value.bit_length() > self.codec.data_bits:
                raise ValueError(f"Veri {self.codec.data_bits} biti aşamaz.")
                
            return value
            
        except ValueError as e:
            QMessageBox.critical(self, "Hata", f"Veri dönüştürme hatası: {str(e)}")
            return None
    
    def encode_and_write_memory(self):
        """Veriyi Hamming koduna dönüştür ve belleğe yaz"""
        # Veriyi işle
        data = self.parse_data_input()
        if data is None:
            return
            
        # Bellek adresini al
        address = self.addr_input.value()
        
        # Hamming kodlaması yap
        try:
            encoded_data = self.codec.encode(data)
            
            # Mevcut veriyi güncelle
            self.current_data = {
                'original': data,
                'encoded': encoded_data,
                'address': address,
                'error_position': None
            }
            
            # Bit kutularını güncelle
            self.update_bit_display(encoded_data)
            
            # Belleğe yaz
            self.memory[address] = {
                'original': data,
                'encoded': encoded_data,
                'data_bits': self.bit_length
            }
            
            # Tabloları güncelle
            self.update_memory_table()
            
            # Değer etiketlerini güncelle
            self.update_value_labels(data, encoded_data)
            self.reset_syndrome_panel()
            
            # Geçmişe ekle
            self.add_history_item(
                f"{address} adresine yazma", 
                f"{self.format_data_value(data)} kodlandı: {self.format_encoded_value(encoded_data)}"
            )
            
            # Durum mesajı
            self.statusBar().showMessage(f"{address} adresine veri yazıldı")
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kodlama hatası: {str(e)}")
    
    def read_from_memory(self):
        """Bellekten veri okur"""
        address = self.addr_input.value()
        
        if address in self.memory:
            # Bellekteki veriyi al
            data = self.memory[address]

            data_bits = data.get('data_bits', self.bit_length)
            if data_bits != self.bit_length:
                combo_index = {8: 0, 16: 1, 32: 2}[data_bits]
                self.bit_combo.setCurrentIndex(combo_index)
            
            # Mevcut veriyi güncelle
            self.current_data = {
                'original': data['original'],
                'encoded': data['encoded'],
                'address': address,
                'error_position': None
            }
            
            # Bit kutularını güncelle
            self.update_bit_display(data['encoded'])
            
            # Değer etiketlerini güncelle
            self.update_value_labels(data['original'], data['encoded'])
            self.reset_syndrome_panel()
            
            # Geçmişe ekle
            self.add_history_item(
                f"{address} adresinden okuma", 
                f"Kodlanmış: {self.format_encoded_value(data['encoded'])}, Orijinal: {self.format_data_value(data['original'])}"
            )
            
            # Durum mesajı
            self.statusBar().showMessage(f"{address} adresinden veri okundu")
            
        else:
            QMessageBox.warning(self, "Uyarı", f"{address} adresinde veri yok!")
    
    def inject_error(self):
        """Kodlanmış veride bir bit hatası oluşturur"""
        if self.current_data['encoded'] is None:
            QMessageBox.warning(self, "Uyarı", "Önce bir veri kodlayın veya bellekten okuyun!")
            return

        if self.current_data['error_position'] is not None:
            QMessageBox.warning(
                self,
                "Uyarı",
                "Mevcut yapay hata düzeltilmeden yeni hata oluşturulamaz."
            )
            return
            
        # Hata enjekte etmek için bir bit seçim penceresi göster
        error_pos, ok = QInputBox.getInt(
            self, "Hata Oluştur", 
            f"Hata enjekte edilecek bit pozisyonunu girin (1-{self.codec.total_bits}).\n"
            "Bit 1 sağ uçtaki bittir.",
            1, 1, self.codec.total_bits, 1
        )
        
        if not ok:
            return
            
        # Hata enjekte et
        try:
            # Mevcut veriyi al
            encoded_data = self.current_data['encoded']
            address = self.current_data['address']
            
            # Hatayı enjekte et
            error_data = self.codec.inject_error(encoded_data, error_pos)
            
            # Mevcut veriyi güncelle
            self.current_data['encoded'] = error_data
            self.current_data['error_position'] = error_pos
            
            # Belleği güncelle
            if address in self.memory:
                self.memory[address]['encoded'] = error_data
            
            # Bit kutularını güncelle
            self.update_bit_display(error_data, error_pos)
            
            # Değer etiketini güncelle
            self.update_value_labels(self.current_data['original'], error_data)
            self.reset_syndrome_panel()
            self.injected_bit_label.setText(str(error_pos))
            self.error_signal_label.setText("Yapay hata oluşturuldu")
            self.confirmation_label.setText("Tespit bekleniyor")
            
            # Tabloları güncelle
            self.update_memory_table()
            
            # Geçmişe ekle
            self.add_history_item(
                f"Hata Enjekte Edildi", 
                f"Bit {error_pos} tersine döndürüldü"
            )
            
            # Durum mesajı
            self.statusBar().showMessage(f"Bit {error_pos} pozisyonunda hata oluşturuldu")
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Hata enjekte etme hatası: {str(e)}")
    
    def show_faq(self):
        """FAQ penceresini gösterir"""
        faq_dialog = FAQDialog(self)
        faq_dialog.exec_()
    
    def detect_and_correct_error(self):
        """Hamming kodu ile hataları tespit eder ve düzeltir"""
        if self.current_data['encoded'] is None:
            QMessageBox.warning(self, "Uyarı", "Önce bir veri kodlayın veya bellekten okuyun!")
            return
            
        # Mevcut veriyi al
        encoded_data = self.current_data['encoded']
        address = self.current_data['address']
        injected_position = self.current_data['error_position']
        
        # Hata tespiti ve düzeltmesi
        try:
            result = self.codec.detect_and_correct(encoded_data)
            self.update_syndrome_panel(result, injected_position)
            
            # Sonuçları göster
            message = f"Hata Tespiti Sonucu:\n"
            message += f"Sendrom Kelimesi: {result['syndrome_bits']}\n"
            message += f"Sendrom Ondalık: {result['syndrome']}\n"
            
            if result['error_position'] is not None:
                message += f"Tespit Edilen Hatalı Bit: {result['error_position']}\n"

            if injected_position is not None:
                message += f"Kullanıcının Bozduğu Bit: {injected_position}\n"
                if injected_position == result['error_position']:
                    message += "Sonuç: Hata doğru tespit edildi.\n"
                else:
                    message += "Sonuç: Tespit edilen bit, bozulan bitle uyuşmuyor.\n"
                
            if result['error_type'] == 'single':
                message += f"Düzeltilmiş Hamming Kodu: {self.format_encoded_value(result['corrected_data'])}\n"
                message += f"Data Out: {self.format_data_value(result['original_data'])}"
                
                # Belleği ve mevcut veriyi güncelle
                self.current_data['encoded'] = result['corrected_data']
                self.current_data['original'] = result['original_data']
                self.current_data['error_position'] = None
                
                if address in self.memory:
                    self.memory[address]['encoded'] = result['corrected_data']
                    self.memory[address]['original'] = result['original_data']
                    
                # Bit kutularını güncelle
                self.update_bit_display(result['corrected_data'])
                
                # Değer etiketlerini güncelle
                self.update_value_labels(result['original_data'], result['corrected_data'])
                
                # Tabloları güncelle
                self.update_memory_table()
                
                # Geçmişe ekle
                self.add_history_item(
                    "Hata Düzeltildi", 
                    f"Sendrom {result['syndrome_bits']} => bit {result['error_position']}, Data Out: {self.format_data_value(result['original_data'])}"
                )
                
            elif result['error_type'] == 'none':
                message += "Veri sağlıklı, hata yok."
                
                # Geçmişe ekle
                self.add_history_item(
                    "Hata Kontrolü", 
                    "Hata yok"
                )

            else:
                message += "Sendrom geçerli bit aralığı dışında; düzeltme yapılmadı."
                self.add_history_item(
                    "Belirsiz Hata",
                    f"Sendrom {result['syndrome_bits']} geçerli aralık dışında"
                )
                
            # Sonuç mesajını göster
            QMessageBox.information(self, "Hata Tespiti ve Düzeltme", message)
            
            # Durum mesajı
            if result['error_type'] == 'none':
                self.statusBar().showMessage("Veri sağlam, hata tespit edilmedi")
            elif result['error_type'] == 'single':
                self.statusBar().showMessage(f"Tek bit hatası düzeltildi: Pozisyon {result['error_position']}")
            else:
                self.statusBar().showMessage("Belirsiz hata tespit edildi.")
                
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Hata tespit ve düzeltme işlemi hatası: {str(e)}")

# QInputBox sınıfı (QInputDialog'u basitleştirir)
class QInputBox:
    @staticmethod
    def getInt(parent, title, label, value=0, min_val=0, max_val=100, step=1):
        from PyQt5.QtWidgets import QInputDialog
        value, ok = QInputDialog.getInt(parent, title, label, value, min_val, max_val, step)
        return value, ok

# Ana fonksiyon
def main():
    app = QApplication(sys.argv)
    window = HammingSimulatorUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
