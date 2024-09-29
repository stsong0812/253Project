def read_key(filename):
    """Read the key from the specified key file."""
    with open(filename, "r") as key_text:
        content = key_text.read().strip()  # Strip to remove any extra whitespace
    return content  # Return the key content

def char_initialization():
    """Initialize Cuneiform and ASCII character sets."""
    cuneiform_chars = [chr(i) for i in range(0x12000, 0x12255)]
    ascii_chars = [chr(i) for i in range(0, 255)]
    return cuneiform_chars, ascii_chars

cuneiform_chars, ascii_chars = char_initialization()

def char_mapping(cuneiform, ascii):
    """Create a mapping dictionary from ASCII to Cuneiform."""
    mapped_dict = {key: value for key, value in zip(ascii, cuneiform)}
    return mapped_dict

mapped_dict = char_mapping(cuneiform_chars, ascii_chars)

def encrypt_file(mapping, plaintext_file):
    """Encrypt the contents of the specified plaintext file."""
    with open(plaintext_file, "r") as plaintext:
        content = plaintext.read()
    
    subbed_content = ''.join(mapping.get(char, char) for char in content)
    
    with open("encrypted.txt", "w") as enc_text:
        enc_text.write(subbed_content)
    
    print("Encryption complete. Encrypted file created as 'encrypted.txt'.")
    return subbed_content

def decrypt_file(mapping, encrypted_file):
    """Decrypt the contents of the specified encrypted file."""
    reverse_mapping = {v: k for k, v in mapping.items()}
    
    with open(encrypted_file, "r") as encrypted_text:
        content = encrypted_text.read()
    
    decrypted_text = ''.join(reverse_mapping.get(char, char) for char in content)

    with open("decrypted.txt", "w") as dec_text:
        dec_text.write(decrypted_text)
    
    print("Decryption complete. Decrypted file created as 'decrypted.txt'.")
    return decrypted_text

def cuneicrypt_menu():
    """Display the menu for the Cuneicrypt application."""
    menu = int(input('Welcome to Cuneicrypt! Choose an option:\n'
                     '1. Encrypt a file \n'
                     '2. Decrypt a file \n'
                     ))

    if menu == 1:
        key_input = input('Would you like to utilize a key file? (y/n): ').strip().lower()
        key_bool = key_input == 'y'

        if key_bool:
            key_file_name = input("Enter the key file name: ").strip()  # Ask for key file name
            print("Calling Key Function")
            user_key = read_key(key_file_name)  # Pass the key file name to the read function
            plaintext_file = input("Enter the file to encrypt: ")
            encrypt_file(mapped_dict, plaintext_file)  # Encrypt the file with the mapping
        else:
            print("Continuing encryption")
            plaintext_file = input("Enter the file to encrypt: ")
            encrypt_file(mapped_dict, plaintext_file)  # Encrypt the file with the mapping

    elif menu == 2:
        key_input = input('Would you like to utilize a key file? (y/n): ').strip().lower()
        key_bool = key_input == 'y'

        if key_bool:
            key_file_name = input("Enter the key file name: ").strip()  # Ask for key file name
            print("Calling Key Function")
            user_key = read_key(key_file_name)  # Pass the key file name to the read function
            encrypted_file = input("Enter the file to decrypt: ")
            decrypt_file(mapped_dict, encrypted_file)  # Decrypt the file with the mapping
        else:
            print("Continuing decryption")
            encrypted_file = input("Enter the file to decrypt: ")
            decrypt_file(mapped_dict, encrypted_file)  # Decrypt the file with the mapping
    else:
        print("Invalid option. Please choose 1 or 2.")

cuneicrypt_menu()