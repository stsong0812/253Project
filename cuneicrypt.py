def read_key(filename):
    """Function to read the key obtained from user input"""
    with open(filename, "r") as key_text:
        content = key_text.read().strip()
    return content

def char_initialization():
    """Function to initialize both Cuneiform and ASCII characters"""
    cuneiform_chars = [chr(i) for i in range(0x12000, 0x12255)]
    ascii_chars = [chr(i) for i in range(0, 255)]
    return cuneiform_chars, ascii_chars

def char_mapping(cuneiform, ascii):
    """Map Cuneiform characters to corresponding ASCII character"""
    mapped_dict = {key: value for key, value in zip(ascii, cuneiform)}
    return mapped_dict

def encrypt_file(mapping, plaintext_file, key):
    """Function to encrypt plaintext using provided key and character mapping"""
    with open(plaintext_file, "r") as plaintext:
        content = plaintext.read()
    
    key_length = len(key)
    subbed_content = []

    # Main encryption loop
    for i, char in enumerate(content):
        mapped_char = mapping.get(char, char)  # Map the character
        key_char = key[i % key_length]  # Cycle through the key
        encrypted_char = chr(ord(mapped_char) ^ ord(key_char))  # Simple XOR operation
        subbed_content.append(encrypted_char)

    subbed_content_str = ''.join(subbed_content)

    with open("encrypted.txt", "w") as enc_text:
        enc_text.write(subbed_content_str)
    
    print("Encryption complete. Encrypted file created as 'encrypted.txt'.")
    return subbed_content_str

def decrypt_file(mapping, encrypted_file, key):
    """Function to decrypt Cuneicrypt string obtained from user input file"""
    reverse_mapping = {v: k for k, v in mapping.items()}
    
    with open(encrypted_file, "r") as encrypted_text:
        content = encrypted_text.read()
    
    decrypted_text = []
    key_length = len(key)
    
    # Main decryption loop
    for i, char in enumerate(content):
        key_char = key[i % key_length]  # Cycle through the key
        decrypted_char = chr(ord(char) ^ ord(key_char))  # Reverse XOR operation
        original_char = reverse_mapping.get(decrypted_char, decrypted_char) # Reverse map
        decrypted_text.append(original_char)

    decrypted_text_str = ''.join(decrypted_text)

    with open("decrypted.txt", "w") as dec_text:
        dec_text.write(decrypted_text_str)
    
    print("Decryption complete. Decrypted file created as 'decrypted.txt'.")
    return decrypted_text_str

def cuneicrypt_menu():
    """Display the menu for the Cuneicrypt application."""
    cuneiform_chars, ascii_chars = char_initialization()  # Initialize character sets
    mapped_dict = char_mapping(cuneiform_chars, ascii_chars)  # Create the mapping

    menu = int(input('Welcome to Cuneicrypt! Choose an option:\n'
                     '1. Encrypt a file \n'
                     '2. Decrypt a file \n'
                     ))

    if menu == 1:
        key_input = input('Would you like to utilize a key file? (y/n): ').strip().lower()
        key_bool = key_input == 'y'

        if key_bool:
            key_file_name = input("Enter the key file name: ").strip()  # Ask for key file name
            user_key = read_key(key_file_name)  # Read the key from the file
            plaintext_file = input("Enter the file to encrypt: ")
            encrypt_file(mapped_dict, plaintext_file, user_key)  # Encrypt the file with the mapping and key
        else:
            plaintext_file = input("Enter the file to encrypt: ")
            encrypt_file(mapped_dict, plaintext_file, "")  # Encrypt without key

    elif menu == 2:
        key_input = input('Would you like to utilize a key file? (y/n): ').strip().lower()
        key_bool = key_input == 'y'

        if key_bool:
            key_file_name = input("Enter the key file name: ").strip()  # Ask for key file name
            user_key = read_key(key_file_name)  # Read the key from the file
            encrypted_file = input("Enter the file to decrypt: ")
            decrypt_file(mapped_dict, encrypted_file, user_key)  # Decrypt the file with the mapping and key
        else:
            encrypted_file = input("Enter the file to decrypt: ")
            decrypt_file(mapped_dict, encrypted_file, "")  # Decrypt without key
    else:
        print("Invalid option. Please choose 1 or 2.")

# Run the menu
cuneicrypt_menu()