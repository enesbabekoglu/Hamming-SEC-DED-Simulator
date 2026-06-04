import unittest

from hamming_codec import HammingCodec


class HammingCodecTest(unittest.TestCase):
    def test_standard_hamming_lengths(self):
        expected = {
            8: (4, 12),
            16: (5, 21),
            32: (6, 38),
        }

        for data_bits, (parity_bits, total_bits) in expected.items():
            with self.subTest(data_bits=data_bits):
                codec = HammingCodec(data_bits)

                self.assertEqual(codec.parity_bits, parity_bits)
                self.assertEqual(codec.total_bits, total_bits)

    def test_rejects_unsupported_data_length(self):
        with self.assertRaises(ValueError):
            HammingCodec(24)

    def test_roundtrip_without_error(self):
        values = {
            8: [0, 1, 0b10110010, 0xFF],
            16: [0, 1, 0b1011001010110010, 0xFFFF],
            32: [0, 1, 0xA5A55A5A, 0xFFFFFFFF],
        }

        for data_bits, samples in values.items():
            codec = HammingCodec(data_bits)

            for data in samples:
                with self.subTest(data_bits=data_bits, data=data):
                    encoded = codec.encode(data)
                    result = codec.detect_and_correct(encoded)

                    self.assertEqual(result["error_type"], "none")
                    self.assertEqual(result["syndrome"], 0)
                    self.assertEqual(result["syndrome_bits"], "0" * codec.parity_bits)
                    self.assertEqual(result["corrected_data"], encoded)
                    self.assertEqual(result["original_data"], data)

    def test_every_single_bit_error_is_corrected(self):
        samples = {
            8: 0b10110010,
            16: 0b1011001010110010,
            32: 0xA5A55A5A,
        }

        for data_bits, data in samples.items():
            codec = HammingCodec(data_bits)
            encoded = codec.encode(data)

            for position in range(1, codec.total_bits + 1):
                with self.subTest(data_bits=data_bits, position=position):
                    corrupted = codec.inject_error(encoded, position)
                    result = codec.detect_and_correct(corrupted)

                    self.assertEqual(result["error_type"], "single")
                    self.assertEqual(result["error_position"], position)
                    self.assertEqual(result["syndrome"], position)
                    self.assertEqual(result["corrected_data"], encoded)
                    self.assertEqual(result["original_data"], data)

    def test_assignment_style_syndrome_for_bit_six(self):
        codec = HammingCodec(8)
        data = int("10110010", 2)
        encoded = codec.encode(data)
        corrupted = codec.inject_error(encoded, 6)
        result = codec.detect_and_correct(corrupted)

        self.assertEqual(result["syndrome_bits"], "0110")
        self.assertEqual(result["syndrome"], 6)
        self.assertEqual(result["error_position"], 6)
        self.assertEqual(codec.get_bit_string(result["corrected_data"]), codec.get_bit_string(encoded))
        self.assertEqual(bin(result["original_data"])[2:].zfill(8), "10110010")

    def test_position_lists_cover_all_hamming_bits(self):
        for data_bits in (8, 16, 32):
            codec = HammingCodec(data_bits)
            positions = codec.get_data_and_parity_positions()
            all_positions = set(positions["data_positions"]) | set(positions["parity_positions"])

            self.assertEqual(len(positions["data_positions"]), data_bits)
            self.assertEqual(len(positions["parity_positions"]), codec.parity_bits)
            self.assertEqual(all_positions, set(range(codec.total_bits)))

    def test_inject_error_rejects_out_of_range_position(self):
        codec = HammingCodec(8)
        encoded = codec.encode(0b10110010)

        with self.assertRaises(ValueError):
            codec.inject_error(encoded, 0)

        with self.assertRaises(ValueError):
            codec.inject_error(encoded, codec.total_bits + 1)


if __name__ == "__main__":
    unittest.main()
