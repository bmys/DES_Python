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

    def test_first_round(self):
        plain = des.text_to_arr('0010100111011000001000110011011100111100010101100100100111111011')
        key = des.text_to_arr('1101000111010100101000110101110010101010000100011101010010101010')
        result = des.encrypt(plain, key)
        desired = des.text_to_arr('1000001010011101110100111010110001101111011011000110111010010010')

        self.assertEqual(desired, result)




if __name__ == '__main__':
    unittest.main()
