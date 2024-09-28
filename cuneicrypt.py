def char_initilization():
    cuneiform_chars = []
    ascii_chars = []

    for i in range(0x12000, 0x12255):
        cuneiform_chars.append(chr(i))

    for i in range(0, 255):
        ascii_chars.append(chr(i))

    return cuneiform_chars, ascii_chars

cuneiform_chars, ascii_chars = char_initilization()

def char_mapping(cuneiform, ascii):
    mapped_dict = {key: value for key, value in zip(cuneiform, ascii)}

    return mapped_dict

char_mapping(cuneiform_chars, ascii_chars)