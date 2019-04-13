import unittest

import des
import tables


class TestByteOperations(unittest.TestCase):

    def test_text_to_bytes_arr(self):
        self.assertEqual(des.ascii_to_bytes_arr('hello'), ['01101000', '01100101', '01101100', '01101100', '01101111'])

    def test_bytes_to_bits(self):
        self.assertEqual(
            des.bytes_to_bits(des.ascii_to_bytes_arr('hello')),
            [0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0,
             1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1])

    def test_bit_arr_to_str(self):
        self.assertEqual(
            des.bit_arr_to_str([0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0,
                                1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1]),
            '0110100001100101011011000110110001101111')

    def test_rearrange(self):
        arr1 = [1, 2, 3, 4, 5]
        arr2 = [0, 1, 0, 1, 1]

        idx_arr = [5, 4, 3, 2, 1]
        idx_arr2 = [1, 2, 2, 2, 3]

        self.assertEqual(des.rearrange(arr1, idx_arr), idx_arr)
        self.assertEqual(des.rearrange(arr1, idx_arr2), [1, 2, 2, 2, 3])
        self.assertEqual(des.rearrange(arr2, idx_arr2), [0, 1, 1, 1, 0])

    def test_shift_bits(self):
        arr1 = [1, 2, 3, 4, 5]
        res = des.shift_bits(arr1, 1)

        self.assertEqual(res, [2, 3, 4, 5, 1])

        res = des.shift_bits(arr1, 2)
        self.assertEqual(res, [3, 4, 5, 1, 2])
        # self.assertEqual()

    def test_arr_to_int(self):
        arr1 = [0, 1, 0, 1]
        res = des.arr_to_int(arr1)
        self.assertEqual(res, 5)

        arr1 = [1, 1, 0, 1]
        res = des.arr_to_int(arr1)
        self.assertEqual(res, 13)

        # self.assertEqual()

class TestPermutation(unittest.TestCase):

    def test_initial_permutation(self):
        plain = ['0', '0', '1', '0', '1', '0', '0', '1', '1', '1', '0', '1', '1', '0', '0', '0', '0', '0', '1', '0',
                 '0',
                 '0', '1', '1', '0', '0', '1', '1', '0', '1', '1', '1', '0', '0', '1', '1', '1', '1', '0', '0', '0',
                 '1',
                 '0', '1', '0', '1', '1', '0', '0', '1', '0', '0', '1', '0', '0', '1', '1', '1', '1', '1', '1', '0',
                 '1', '1']
        result = des.rearrange(plain, tables.initialPermutationTable)
        result = ''.join(result)
        self.assertEqual(result, '1110001010111010001110001100110110000010100111011101001110101100')

    def test_initial_key_permutation(self):
        key = ['1', '1', '0', '1', '0', '0', '0', '1', '1', '1', '0', '1', '0', '1', '0', '0', '1', '0', '1', '0', '0',
               '0', '1', '1', '0', '1', '0', '1', '1', '1', '0', '0', '1', '0', '1', '0', '1', '0', '1', '0', '0', '0',
               '0', '1', '0', '0', '0', '1', '1', '1', '0', '1', '0', '1', '0', '0', '1', '0', '1', '0', '1', '0', '1',
               '0']
        result = des.rearrange(key, tables.keyPermutationTable)
        # print(result)
        result = ''.join(result)
        self.assertEqual(result, '11010111010010111001010001101001010001001010100110001011')

    # def test_shift_key(self):
    #     key = ['1', '1', '0', '1', '0', '1', '1', '1', '0', '1', '0', '0', '1', '0', '1', '1', '1', '0', '0', '1', '0', '1', '0', '0', '0', '1', '1', '0', '1', '0', '0', '1', '0', '1', '0', '0', '0', '1', '0', '0', '1', '0', '1', '0', '1', '0', '0', '1', '1', '0', '0', '0', '1', '0', '1', '1']
    #
    #     result = des.shift_bits(key, 1)
    #     result = ''.join(result)
    #     self.assertEqual(result, '10101110100101110010100011010010100010010101001100010111')

    def test_generate_sub_key(self):
        key = des.text_to_arr('11010111010010111001010001101001010001001010100110001011')

        result = des.generate_sub_key(key, 0)
        result = des.bit_arr_to_str(result)
        self.assertEqual(result, '10101110100101110010100011010010100010010101001100010111')

    def test_compression_key(self):
        sub_key = des.text_to_arr('10101110100101110010100011010010100010010101001100010111')

        result = des.rearrange(sub_key, tables.compressionPermutationTable)
        result = des.bit_arr_to_str(result)
        self.assertEqual(result, '100011111110011010110000011111010011100100010000')

    def test_expansion_block(self):
        sub_key = des.text_to_arr('10000010100111011101001110101100')

        result = des.rearrange(sub_key, tables.extensionPermutationTable)
        result = des.bit_arr_to_str(result)
        self.assertEqual(result, '010000000101010011111011111010100111110101011001')

    def test_xor_arr(self):
        exp_block = des.text_to_arr('010000000101010011111011111010100111110101011001')
        sub_key = des.text_to_arr('100011111110011010110000011111010011100100010000')

        result = des.xor_arr(exp_block, sub_key)
        result = des.bit_arr_to_str(result)

        self.assertEqual(result, '110011111011001001001011100101110100010001001001')

    def test_s_box(self):
        self.assertEqual(des.get_s_box([0, 1, 1, 0, 1, 0], 0), [1, 0, 0, 1])
        self.assertEqual(des.get_s_box([1, 1, 0, 0, 1, 0], 0), [1, 1, 0, 0])
        self.assertEqual(des.get_s_box([1, 1, 0, 0, 1, 0], 0), [1, 1, 0, 0])
        self.assertEqual(des.get_s_box([0, 0, 0, 0, 1, 1], 0), [1, 1, 1, 1])

    def split_arr_8(self):
        arr = des.text_to_arr('110011111011001001001011100101110100010001001001')
        arr = des.split_arr_to_chunks(arr, 6)
        self.assertEqual(len(arr), 8)
        self.assertEqual(arr[0], [1, 1, 0, 0])
        self.assertEqual(arr[1], [1, 1, 1, 1])
        self.assertEqual(arr[-1], [1, 0, 0, 1])

    def test_s_box_substitution(self):
        xor = des.text_to_arr('110011111011001001001011100101110100010001001001')
        desired = des.text_to_arr('10110101001111111100010011101010')
        result = des.s_box_substitution(xor)
        self.assertEqual(desired, result)

    def test_p_box_substitution(self):
        sbox_output = des.text_to_arr('10110101001111111100010011101010')
        desired = des.text_to_arr('10001101110101100101011001011111')

        result = des.p_box_substitution(sbox_output)
        self.assertEqual(desired, result)

    def test_sub_keys_generation(self):
        sub_keys = des.generate_sub_keys('11110000110011001010101011110101010101100110011110001111')

    def test_compression_keys(self):
        cd = des.rearrange(des.text_to_arr('11100001100110010101010111111010101011001100111100011110'), tables.compressionPermutationTable)
        desired = des.text_to_arr('000110110000001011101111111111000111000001110010')
        self.assertEqual(cd, desired)

        key = des.text_to_arr('11110000110011001010101011110101010101100110011110001111')
        sub_keys = des.generate_sub_keys(key)

        compressed_keys = list(map(lambda x: des.rearrange(x, tables.compressionPermutationTable), sub_keys))

        compressed_arr = [
            '000110110000001011101111111111000111000001110010',
            '011110011010111011011001110110111100100111100101',
            '010101011111110010001010010000101100111110011001',
            '011100101010110111010110110110110011010100011101',
            '011111001110110000000111111010110101001110101000',
            '011000111010010100111110010100000111101100101111',
            '111011001000010010110111111101100001100010111100',
            '111101111000101000111010110000010011101111111011',
           '111000001101101111101011111011011110011110000001',
           '101100011111001101000111101110100100011001001111',
           '001000010101111111010011110111101101001110000110',
           '011101010111000111110101100101000110011111101001',
           '100101111100010111010001111110101011101001000001',
           '010111110100001110110111111100101110011100111010',
           '101111111001000110001101001111010011111100001010',
           '110010110011110110001011000011100001011111110101'
        ]

        for ck, ca in zip(compressed_keys, compressed_arr):
            d = des.text_to_arr(ca)
            self.assertEqual(ck, d)






    def test_all(self):
        plain = [  0,1,1,0,1,0,0,0,
                   0,1,1,0,0,1,0,1,
                   0,1,0,0,1,1,0,0,
                   0,0,1,0,1,1,0,0,

                   0,1,1,0,1,1,0,1,
                   0,0,1,0,0,1,0,0,
                   0,0,1,1,1,0,1,0,
                   0,0,1,0,1,0,0,1]

        key = [0, 1, 0, 0, 0, 0, 0, 1,
                        0, 0, 0, 1, 0, 1, 0, 0,
                        0, 1, 0, 0, 0, 0, 0, 1,
                        0, 0, 0, 1, 0, 1, 0, 1,

                        0, 1, 0, 0, 0, 1, 0, 1,
                        0, 0, 0, 1, 0, 0, 0, 0,
                        0, 1, 0, 0, 0, 1, 0, 1,
                        0, 0, 0, 1, 0, 0, 1, 0]

        encrypted = des.encrypt(plain, key)
        decrypted = des.decrypt(encrypted, key)
        print('ENCRYPTED: ' + ''.join(str(i) for i in encrypted))
        print('DECRYPTED: ' + ''.join(str(i) for i in decrypted))
        print('PLAIN:     ' + ''.join(str(i) for i in plain))

        self.assertEqual(decrypted, plain)


    # def test_all(self):
    #
    #     self.assertEqual(encrypted, des.ascii_to_bytes_arr('0000000000000000'))




if __name__ == '__main__':
    unittest.main()
