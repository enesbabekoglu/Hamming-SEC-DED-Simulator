#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hamming SEC-DED (Single Error Correction - Double Error Detection) kodlaması 
ve hata düzeltme işlemleri için modül
"""

class HammingCodec:
    def __init__(self, data_bits=16):
        """
        Hamming kodlayıcı/kod çözücü sınıfı
        
        Args:
            data_bits (int): Veri bit uzunluğu (8, 16 veya 32 olabilir)
        """
        self.data_bits = data_bits
        self.parity_bits = self._calculate_parity_bits()
        self.total_bits = self.data_bits + self.parity_bits + 1  # +1 genel parite biti için
        
    def _calculate_parity_bits(self):
        """Gerekli parite bit sayısını hesaplar: 2^r >= m + r + 1"""
        r = 0
        while (2**r) < (self.data_bits + r + 1):
            r += 1
        return r
        
    def _is_power_of_two(self, num):
        """Bir sayının 2'nin kuvveti olup olmadığını kontrol eder"""
        return num != 0 and (num & (num - 1)) == 0
        
    def encode(self, data):
        """
        Verilen veriyi Hamming SEC-DED kodu ile kodlar
        
        Args:
            data (int): Kodlanacak veri
            
        Returns:
            int: Kodlanmış veri (Hamming SEC-DED)
        """
        # Veri bit sayısını kontrol et
        if data.bit_length() > self.data_bits:
            raise ValueError(f"Veri {self.data_bits} bitten büyük olamaz")
        
        # Kodlanmış veri için yeterli uzunlukta bir dizi oluştur
        encoded = 0
        
        # Veri bitlerini yerleştir
        data_idx = 0
        for i in range(1, self.total_bits):
            # Parite biti pozisyonlarını atla (2'nin kuvvetleri)
            if not self._is_power_of_two(i):
                # Veri bitini uygun pozisyona yerleştir
                if data & (1 << data_idx):
                    encoded |= (1 << (i - 1))
                data_idx += 1
                
        # Parite bitlerini hesapla ve yerleştir
        for i in range(self.parity_bits):
            parity_pos = 2**i
            parity_val = 0
            
            # Bu parite bitinin kontrol ettiği bitleri topla
            for j in range(1, self.total_bits):
                if j & parity_pos:
                    if encoded & (1 << (j - 1)):
                        parity_val ^= 1
            
            # Parite bitini yerleştir
            if parity_val:
                encoded |= (1 << (parity_pos - 1))
                
        # Genel parite bitini hesapla (even parity - çift parite)
        overall_parity = 0
        for i in range(self.total_bits - 1):
            if encoded & (1 << i):
                overall_parity ^= 1
        
        # Genel parite biti en yüksek birimli konuma yerleştirilir
        if overall_parity:
            encoded |= (1 << (self.total_bits - 1))
            
        return encoded
        
    def detect_and_correct(self, encoded_data):
        """
        Kodlanmış veriyi kontrol eder ve varsa hataları tespit edip düzeltir
        
        Args:
            encoded_data (int): Kodlanmış veri
            
        Returns:
            dict: Hata bilgisi içeren sözlük:
                {
                    'error_detected': Bool, 
                    'error_type': 'none|single|double|unknown',
                    'error_position': int | None,  # Hata varsa pozisyonu (0'dan başlar)
                    'corrected_data': int,  # Düzeltilmiş veri
                    'original_data': int    # Orijinal veri (düzeltmeden sonra)
                }
        """
        result = {
            'error_detected': False,
            'error_type': 'none',
            'error_position': None,
            'corrected_data': encoded_data,
            'original_data': None
        }
        
        # Genel parite kontrolü
        overall_parity = 0
        for i in range(self.total_bits):
            if encoded_data & (1 << i):
                overall_parity ^= 1
        
        # Sendrom hesaplama (parite bitleri kontrol edilir)
        syndrome = 0
        for i in range(self.parity_bits):
            parity_pos = 2**i
            parity_check = 0
            
            # Parite biti için tüm bitleri kontrol et
            for j in range(1, self.total_bits):
                if j & parity_pos:
                    if encoded_data & (1 << (j - 1)):
                        parity_check ^= 1
            
            # Parite uyuşmazlığı varsa, sendroma ekle
            if parity_check != ((encoded_data & (1 << (parity_pos - 1))) != 0):
                syndrome |= parity_pos
        
        # Hata tespiti ve düzeltme
        if syndrome == 0 and overall_parity == 0:
            # Hata yok
            result['error_type'] = 'none'
            
        elif syndrome != 0 and overall_parity != 0:
            # Tek hata - düzeltilebilir
            result['error_detected'] = True
            result['error_type'] = 'single'
            result['error_position'] = syndrome - 1
            
            # Hatalı biti tersle
            result['corrected_data'] = encoded_data ^ (1 << (syndrome - 1))
            
        elif syndrome != 0 and overall_parity == 0:
            # Çift hata - tespit edilebilir ancak düzeltilemez
            result['error_detected'] = True
            result['error_type'] = 'double'
            
        elif syndrome == 0 and overall_parity != 0:
            # Genel parite bitinde hata var
            result['error_detected'] = True
            result['error_type'] = 'single'
            result['error_position'] = self.total_bits - 1
            result['corrected_data'] = encoded_data ^ (1 << (self.total_bits - 1))
            
        # Düzeltilmiş veriden orijinal veriyi çıkar
        corrected = result['corrected_data']
        original = 0
        data_idx = 0
        
        for i in range(1, self.total_bits):
            if not self._is_power_of_two(i) and i < self.total_bits - 1:  # Genel parite hariç
                if corrected & (1 << (i - 1)):
                    original |= (1 << data_idx)
                data_idx += 1
        
        result['original_data'] = original
        return result
    
    def inject_error(self, encoded_data, position):
        """
        Belirtilen pozisyonda bir bit hatasını simüle eder
        
        Args:
            encoded_data (int): Kodlanmış veri
            position (int): Hata enjekte edilecek bit pozisyonu (0'dan başlayarak)
            
        Returns:
            int: Hata enjekte edilmiş veri
        """
        if position < 0 or position >= self.total_bits:
            raise ValueError(f"Bit pozisyonu 0 ile {self.total_bits-1} arasında olmalıdır")
        
        # Belirtilen pozisyondaki biti tersle
        return encoded_data ^ (1 << position)
    
    def get_bit_string(self, value, total_bits=None):
        """
        Tam sayıyı bit dizisi olarak döndürür
        
        Args:
            value (int): Bit dizisine dönüştürülecek tam sayı
            total_bits (int, optional): Toplam bit sayısı, None ise self.total_bits kullanılır
            
        Returns:
            str: Bit dizisi
        """
        if total_bits is None:
            total_bits = self.total_bits
            
        return bin(value)[2:].zfill(total_bits)
    
    def is_parity_bit(self, position):
        """
        Belirtilen pozisyonun bir parite biti olup olmadığını kontrol eder
        
        Args:
            position (int): Kontrol edilecek bit pozisyonu (0'dan başlayarak)
            
        Returns:
            bool: Eğer pozisyon bir parite biti ise True, değilse False
        """
        # Genel parite biti (en son bit) kontrolü
        if position == self.total_bits - 1:
            return False
            
        # 1'den başlayan pozisyon (indeks+1)
        pos_from_one = position + 1
        
        # Parite bitleri 2'nin kuvvetleri olan pozisyonlardadır (1, 2, 4, 8, ...)
        return self._is_power_of_two(pos_from_one)
    
    def get_data_and_parity_positions(self):
        """
        Veri ve parite bit pozisyonlarını döndürür
        
        Returns:
            dict: Pozisyon bilgisi içeren sözlük:
                {
                    'data_positions': [int, ...],  # Veri bit pozisyonları
                    'parity_positions': [int, ...],  # Parite bit pozisyonları
                    'overall_parity_position': int   # Genel parite bit pozisyonu
                }
        """
        parity_positions = []
        data_positions = []
        
        for i in range(self.parity_bits):
            parity_positions.append(2**i - 1)  # 0-indexed
            
        for i in range(1, self.total_bits):
            if not self._is_power_of_two(i) and i < 2**(self.parity_bits):
                data_positions.append(i - 1)  # 0-indexed
        
        return {
            'data_positions': data_positions,
            'parity_positions': parity_positions,
            'overall_parity_position': self.total_bits - 1
        }
