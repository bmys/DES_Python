import tables


def ascii_to_bytes_arr(text):
    a = [bin(ord(x)).lstrip('0b') for x in text]
    b = []

    for byte in a:
        bits_to_add = 8 - len(byte)
        b.append('0' * bits_to_add + byte)
    return b


def bytes_to_bits(arr):
    res = []
    for byte in arr:
        for bit in byte:
            res.append(0) if bit == '0' else res.append(1)
    return res


def bit_arr_to_str(arr):
    return ''.join([str(x) for x in arr])


def text_to_arr(arr):
    return [int(x) for x in arr]


def arr_to_int(arr):
    k = 0
    counter = 1
    arr.reverse()
    for x in arr:
        k += x * counter
        counter *= 2
    return k


def rearrange(arr, idx_arr):
    res = []
    for idx in idx_arr:
        res.append(arr[idx-1])
    return res


def shift_bits(bits, num):
    beg = bits[:num]
    return bits[num:] + beg


def generate_sub_key(key, num):
    l_side, r_side = split_half(key)

    shift = tables.keyShiftTable[num]
    l_side, r_side = shift_bits(l_side, shift), shift_bits(r_side, shift)
    r = l_side + r_side
    return r


def split_half(arr):
    mid = len(arr) // 2
    return arr[:mid], arr[mid:]


def xor_arr(arr1, arr2):
    return [x ^ y for x, y in zip(arr1, arr2)]


def get_s_box(arr, s_box_num):
    s_box = tables.sBlocks[s_box_num]

    row = [arr[0], arr[-1]]
    row = arr_to_int(row)

    col = arr[1:-1]
    col = arr_to_int(col)
    res = s_box[row][col]

    res = [int(x) for x in list('{0:0b}'.format(res))]

    padding = 4 - len(res)
    for x in range(padding):
        res.insert(0, 0)

    return res


def split_arr_to_chunks(arr, n):
    new_arr = []
    for i in range(0, len(arr), n):
        new_arr.append(arr[i:i + n])
    return new_arr


def s_box_substitution(arr):
    spl_arr = split_arr_to_chunks(arr, 6)
    res = []
    for idx, s_box in enumerate(spl_arr):
        val = get_s_box(s_box, idx)
        res.extend(val)
    return res


def p_box_substitution(arr):
    return rearrange(arr, tables.pBlockPermutationTable)


def final_permutation(arr):
    return rearrange(arr, tables.finalPermutationTable)


def generate_sub_keys(key):
    sub_keys = []
    previous_key = key
    for i in range(16):
        previous_key = generate_sub_key(previous_key, i)
        sub_keys.append(previous_key)
    return sub_keys

def compress_keys():
    pass

def encrypt(arr, key, encrypt=True):
    ip = rearrange(arr, tables.initialPermutationTable)
    key = rearrange(key, tables.keyPermutationTable)

    l_block, r_block = split_half(ip)
    new_left = r_block

    sub_key = generate_sub_key(key, 0)
    sub_key = rearrange(sub_key, tables.compressionPermutationTable)
    r_block = rearrange(r_block, tables.extensionPermutationTable)
    r_block = xor_arr(r_block, sub_key)
    r_block = s_box_substitution(r_block)
    r_block = rearrange(r_block, tables.pBlockPermutationTable)
    r_block = xor_arr(r_block, l_block)

    return new_left + r_block


def encrypt1(arr, key, encrypt=True):
    ip = rearrange(arr, tables.initialPermutationTable)
    key = rearrange(key, tables.keyPermutationTable)

    # generate sub keys
    sub_keys = generate_sub_keys(key)
    sub_keys = list(map(lambda x: rearrange(x, tables.compressionPermutationTable), sub_keys))

    current_block = ip
    for sub_key in sub_keys:

        l_block, r_block = split_half(current_block)
        new_left = r_block

        r_block = rearrange(r_block, tables.extensionPermutationTable)
        r_block = xor_arr(r_block, sub_key)
        r_block = s_box_substitution(r_block)
        r_block = rearrange(r_block, tables.pBlockPermutationTable)
        r_block = xor_arr(r_block, l_block)

        current_block = new_left + r_block

    return final_permutation(current_block)


def decrypt1(arr, key, encrypt=True):
    ip = rearrange(arr, tables.initialPermutationTable)
    key = rearrange(key, tables.keyPermutationTable)

    # generate sub keys
    sub_keys = generate_sub_keys(key)
    sub_keys = list(map(lambda x: rearrange(x, tables.compressionPermutationTable), sub_keys))
    sub_keys.reverse()

    current_block = ip
    for sub_key in sub_keys:

        l_block, r_block = split_half(current_block)
        new_left = r_block

        r_block = rearrange(r_block, tables.extensionPermutationTable)
        r_block = xor_arr(r_block, sub_key)
        r_block = s_box_substitution(r_block)
        r_block = rearrange(r_block, tables.pBlockPermutationTable)
        r_block = xor_arr(r_block, l_block)

        current_block = new_left + r_block

    return final_permutation(current_block)


def decrypt2(arr, key, encrypt=True):
    ip = rearrange(arr, tables.initialPermutationTable)
    key = rearrange(key, tables.keyPermutationTable)

    # generate sub keys
    sub_keys = generate_sub_keys(key)
    sub_keys = list(map(lambda x: rearrange(x, tables.compressionPermutationTable), sub_keys))
    sub_keys.reverse()

    current_block = ip
    for sub_key in sub_keys:

        l_block, r_block = split_half(current_block)
        new_left = r_block

        r_block = rearrange(r_block, tables.extensionPermutationTable)
        r_block = xor_arr(r_block, sub_key)
        r_block = s_box_substitution(r_block)
        r_block = rearrange(r_block, tables.pBlockPermutationTable)
        r_block = xor_arr(r_block, l_block)

        current_block = new_left + r_block

    return final_permutation(current_block)

