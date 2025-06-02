#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hamming SEC-DED Simülatörü için PyQt5 tabanlı kullanıcı arayüzü
"""

import sys
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QGroupBox, QGridLayout,
                             QMessageBox, QSpinBox, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPalette, QFont

# Hamming kodlayıcı modülünü içe aktar
from hamming_codec import HammingCodec

# FAQ modülünü içe aktar
from faq import FAQDialog

# Ana pencere sınıfı
class HammingSimulatorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Ana pencere ayarları
        self.setWindowTitle("Hamming SEC-DED Simülatörü - Enes Babekoğlu")
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
        self.data_input.setPlaceholderText("İkili (1010...) veya Hex (0x...) olarak veri girin")
        
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
        global_bit_sample = QLabel("Genel Parite")
        global_bit_sample.setStyleSheet("background-color: #ffffa0; padding: 2px 8px; border-radius: 4px; font-weight: bold;")
        error_bit_sample = QLabel("Hatalı")
        error_bit_sample.setStyleSheet("background-color: #ff8080; padding: 2px 8px; border-radius: 4px; font-weight: bold;")
        
        info_layout.addWidget(bit_info)
        info_layout.addWidget(data_bit_sample)
        info_layout.addWidget(parity_bit_sample)
        info_layout.addWidget(global_bit_sample)
        info_layout.addWidget(error_bit_sample)
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
        
        data_label = QLabel("Orijinal Veri:")
        self.data_value_label = QLabel("0")
        data_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.data_value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        encoded_label = QLabel("Kodlanmış Veri:")
        self.encoded_value_label = QLabel("0")
        encoded_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.encoded_value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        labels_layout.addWidget(data_label)
        labels_layout.addWidget(self.data_value_label)
        labels_layout.addStretch()
        labels_layout.addWidget(encoded_label)
        labels_layout.addWidget(self.encoded_value_label)
        
        # Bellek tablosu
        self.memory_table = QTableWidget(0, 3)
        self.memory_table.setHorizontalHeaderLabels(["Adres", "Kodlanmış Veri", "Orijinal Veri"])
        self.memory_table.horizontalHeader().setStretchLastSection(True)
        self.memory_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        memory_layout.addLayout(labels_layout)
        memory_layout.addWidget(self.memory_table)
        memory_group.setLayout(memory_layout)
        self.main_layout.addWidget(memory_group)
        
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
        copyright_label = QLabel(" 2025 Enes Babekoğlu - Hamming SEC-DED Simülatörü")
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
        
        # Bit kutularını oluştur
        for i in range(total_bits):
            bit_frame = QFrame()
            bit_frame.setFrameShape(QFrame.NoFrame)
            bit_frame.setFixedSize(50, 70)  # Daha büyük kutular
            
            # Bit için düzen oluştur
            layout = QVBoxLayout(bit_frame)
            layout.setContentsMargins(2, 2, 2, 2)
            layout.setSpacing(0)
            
            # Bit pozisyon etiketi
            pos_label = QLabel(str(i))
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
            
            # Bit tipi etiketi
            if i == 0:
                bit_type = 'global_parity'
                type_text = "GP"
                bit_value_frame.setStyleSheet('background-color: #ffffa0; border-radius: 6px; border: 1px solid #e0e000;')  # Açık sarı
            elif i > 0 and self.codec.is_parity_bit(i):
                bit_type = 'parity'
                type_text = f"P{int(math.log2(i))}"
                bit_value_frame.setStyleSheet('background-color: #a0ffa0; border-radius: 6px; border: 1px solid #00c000;')  # Açık yeşil
            else:
                bit_type = 'data'
                type_text = "D"
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
                'position': i,
                'type': bit_type,
                'value': 0
            })
            
            # Bit kutusunu düzene ekle
            self.bit_layout.addWidget(bit_frame)
    
    def update_bit_display(self, bit_values=None, error_position=None):
        """Bit kutularını günceller"""
        if bit_values is None and not self.current_data['encoded']:
            return
        
        if bit_values is None:
            bit_values = self.current_data['encoded']
        
        # Her bit için değeri güncelle
        for i, bit_box in enumerate(self.bit_boxes):
            if i < len(bit_values):
                value = bit_values[i]
                bit_box['value'] = value
                bit_box['label'].setText(str(value))
                
                # Hata enjekte edilmiş biti kırmızı yap
                if error_position is not None and i == error_position:
                    bit_box['value_frame'].setStyleSheet('background-color: #ff8080; border-radius: 6px; border: 1px solid #d00000;')  # Kırmızı
                    bit_box['label'].setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
                else:
                    # Normal renkler
                    if bit_box['type'] == 'global_parity':
                        bit_box['value_frame'].setStyleSheet('background-color: #ffffa0; border-radius: 6px; border: 1px solid #e0e000;')  # Açık sarı
                        bit_box['label'].setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
                    elif bit_box['type'] == 'parity':
                        bit_box['value_frame'].setStyleSheet('background-color: #a0ffa0; border-radius: 6px; border: 1px solid #00c000;')  # Açık yeşil
                        bit_box['label'].setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
                    else:  # data
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
            
            # Kodlanmış veri
            encoded_hex = hex(data['encoded'])
            self.memory_table.setItem(row, 1, QTableWidgetItem(encoded_hex))
            
            # Orijinal veri
            original_hex = hex(data['original'])
            self.memory_table.setItem(row, 2, QTableWidgetItem(original_hex))
        
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
        bit_values = [0] * self.codec.total_bits
        self.update_bit_display(bit_values)
            
    def parse_data_input(self):
        """Kullanıcının girdiği veriyi işler"""
        data_str = self.data_input.text().strip()
        
        try:
            # Hex girişi (0x ile başlıyorsa)
            if data_str.startswith("0x") or data_str.startswith("0X"):
                value = int(data_str, 16)
            # İkili giriş
            else:
                # İkili sayıyı ondalığa çevir
                data_str = ''.join(c for c in data_str if c in '01')  # Sadece 0 ve 1'leri kabul et
                if not data_str:
                    raise ValueError("Geçersiz ikili veri girişi")
                value = int(data_str, 2)
                
            # Veriyi bit sınırına göre kontrol et
            if value.bit_length() > self.codec.data_bits:
                QMessageBox.warning(self, "Uyarı", f"Veri {self.codec.data_bits} biti aşıyor!"
                                     f"\nEn anlamlı bitler kesilecek.")
                # En anlamlı bitleri kes
                mask = (1 << self.codec.data_bits) - 1
                value &= mask
                
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
            positions = self.codec.get_data_and_parity_positions()
            self.update_bit_display([int(b) for b in bin(encoded_data)[2:].zfill(self.codec.total_bits)])
            
            # Belleğe yaz
            self.memory[address] = {
                'original': data,
                'encoded': encoded_data
            }
            
            # Tabloları güncelle
            self.update_memory_table()
            
            # Değer etiketlerini güncelle
            self.data_value_label.setText(hex(data))
            self.encoded_value_label.setText(hex(encoded_data))
            
            # Geçmişe ekle
            self.add_history_item(
                f"{address} adresine yazma", 
                f"{hex(data)} kodlandı: {hex(encoded_data)}"
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
            
            # Mevcut veriyi güncelle
            self.current_data = {
                'original': data['original'],
                'encoded': data['encoded'],
                'address': address,
                'error_position': None
            }
            
            # Bit kutularını güncelle
            positions = self.codec.get_data_and_parity_positions()
            self.update_bit_display([int(b) for b in bin(data['encoded'])[2:].zfill(self.codec.total_bits)])
            
            # Değer etiketlerini güncelle
            self.data_value_label.setText(hex(data['original']))
            self.encoded_value_label.setText(hex(data['encoded']))
            
            # Geçmişe ekle
            self.add_history_item(
                f"{address} adresinden okuma", 
                f"Kodlanmış: {hex(data['encoded'])}, Orijinal: {hex(data['original'])}"
            )
            
            # Durum mesajı
            self.statusBar().showMessage(f"{address} adresinden veri okundu")
            
        else:
            QMessageBox.warning(self, "Uyarı", f"{address} adresinde veri yok!")
    
    def inject_error(self):
        """Kodlanmış veride bir bit hatası oluşturur"""
        if not self.current_data['encoded']:
            QMessageBox.warning(self, "Uyarı", "Önce bir veri kodlayın veya bellekten okuyun!")
            return
            
        # Hata enjekte etmek için bir bit seçim penceresi göster
        error_pos, ok = QInputBox.getInt(
            self, "Hata Oluştur", 
            f"Hata enjekte edilecek bit pozisyonunu girin (0-{self.codec.total_bits-1}):",
            0, 0, self.codec.total_bits-1, 1
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
            self.update_bit_display([int(b) for b in bin(error_data)[2:].zfill(self.codec.total_bits)], error_pos)
            
            # Değer etiketini güncelle
            self.encoded_value_label.setText(hex(error_data))
            
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
        if not self.current_data['encoded']:
            QMessageBox.warning(self, "Uyarı", "Önce bir veri kodlayın veya bellekten okuyun!")
            return
            
        # Mevcut veriyi al
        encoded_data = self.current_data['encoded']
        address = self.current_data['address']
        
        # Hata tespiti ve düzeltmesi
        try:
            result = self.codec.detect_and_correct(encoded_data)
            
            # Sonuçları göster
            message = f"Hata Tespiti Sonucu:\n"
            message += f"Hata Türü: {result['error_type']}\n"
            
            if result['error_position'] is not None:
                message += f"Hata Pozisyonu: {result['error_position']}\n"
                
            if result['error_type'] == 'single':
                message += f"Düzeltilmiş Veri: {hex(result['corrected_data'])}\n"
                message += f"Orijinal Veri: {hex(result['original_data'])}"
                
                # Belleği ve mevcut veriyi güncelle
                self.current_data['encoded'] = result['corrected_data']
                self.current_data['original'] = result['original_data']
                self.current_data['error_position'] = None
                
                if address in self.memory:
                    self.memory[address]['encoded'] = result['corrected_data']
                    self.memory[address]['original'] = result['original_data']
                    
                # Bit kutularını güncelle
                self.update_bit_display([int(b) for b in bin(result['corrected_data'])[2:].zfill(self.codec.total_bits)])
                
                # Değer etiketlerini güncelle
                self.data_value_label.setText(hex(result['original_data']))
                self.encoded_value_label.setText(hex(result['corrected_data']))
                
                # Tabloları güncelle
                self.update_memory_table()
                
                # Geçmişe ekle
                self.add_history_item(
                    "Hata Düzeltildi", 
                    f"Pozisyon {result['error_position']}, Veri: {hex(result['original_data'])}"
                )
                
            elif result['error_type'] == 'double':
                message += "İki bitlik hata tespit edildi, düzeltilemiyor!"
                
                # Geçmişe ekle
                self.add_history_item(
                    "Çift Hata Tespiti", 
                    "Düzeltilemiyor"
                )
                
            else:  # Hata yok
                message += "Veri sağlıklı, hata yok."
                
                # Geçmişe ekle
                self.add_history_item(
                    "Hata Kontrolü", 
                    "Hata yok"
                )
                
            # Sonuç mesajını göster
            QMessageBox.information(self, "Hata Tespiti ve Düzeltme", message)
            
            # Durum mesajı
            if result['error_type'] == 'none':
                self.statusBar().showMessage("Veri sağlam, hata tespit edilmedi")
            elif result['error_type'] == 'single':
                self.statusBar().showMessage(f"Tek bit hatası düzeltildi: Pozisyon {result['error_position']}")
            elif result['error_type'] == 'double':
                self.statusBar().showMessage("Çift bit hatası tespit edildi! Düzeltilemiyor.")
                
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
