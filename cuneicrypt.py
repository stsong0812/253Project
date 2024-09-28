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
    mapped_dict = {key: value for key, value in zip(ascii, cuneiform)}

    return mapped_dict

mapped_dict = char_mapping(cuneiform_chars, ascii_chars)

def encrypt_file(mapping):
    with open("plaintext.txt", "r") as plaintext:
        content = plaintext.read()

    subbed_content = ''.join(mapping.get(char, char) for char in content)
    print(subbed_content)
    
    return subbed_content

encrypt_file(mapped_dict)