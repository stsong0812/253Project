import tkinter as tk
from tkinter import filedialog, messagebox
import os

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

def encrypt_file(mapping, plaintext_file, key, output_label):
    """Function to encrypt plaintext using provided key and character mapping"""
    try:
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

        output_label.config(text="Encryption complete. Encrypted file saved as 'encrypted.txt'.")
    except Exception as e:
        output_label.config(text=f"Encryption failed: {str(e)}")

def decrypt_file(mapping, encrypted_file, key, output_label):
    """Function to decrypt Cuneicrypt string obtained from user input file"""
    try:
        reverse_mapping = {v: k for k, v in mapping.items()}
        
        with open(encrypted_file, "r") as encrypted_text:
            content = encrypted_text.read()

        decrypted_text = []
        key_length = len(key)

        # Main decryption loop
        for i, char in enumerate(content):
            key_char = key[i % key_length]  # Cycle through the key
            decrypted_char = chr(ord(char) ^ ord(key_char))  # Reverse XOR operation
            original_char = reverse_mapping.get(decrypted_char, decrypted_char)  # Reverse map
            decrypted_text.append(original_char)

        decrypted_text_str = ''.join(decrypted_text)

        with open("decrypted.txt", "w") as dec_text:
            dec_text.write(decrypted_text_str)

        output_label.config(text="Decryption complete. Decrypted file saved as 'decrypted.txt'.")
    except Exception as e:
        output_label.config(text=f"Decryption failed: {str(e)}")

def select_file(entry):
    """Open file dialog to select a file and populate the entry"""
    file_path = filedialog.askopenfilename()
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def cuneicrypt_gui():
    """Main GUI for Cuneicrypt"""
    cuneiform_chars, ascii_chars = char_initialization()
    mapped_dict = char_mapping(cuneiform_chars, ascii_chars)

    def perform_encryption():
        key_file = key_entry.get().strip()
        plaintext_file = plaintext_entry.get().strip()

        if not os.path.exists(plaintext_file):
            messagebox.showerror("Error", "Plaintext file does not exist.")
            return

        if os.path.exists(key_file):
            user_key = read_key(key_file)
        else:
            user_key = key_file

        encrypt_file(mapped_dict, plaintext_file, user_key, status_label)

    def perform_decryption():
        key_file = key_entry.get().strip()
        encrypted_file = encrypted_entry.get().strip()

        if not os.path.exists(encrypted_file):
            messagebox.showerror("Error", "Encrypted file does not exist.")
            return

        if os.path.exists(key_file):
            user_key = read_key(key_file)
        else:
            user_key = key_file

        decrypt_file(mapped_dict, encrypted_file, user_key, status_label)

    # Create the main window
    root = tk.Tk()
    root.title("Cuneicrypt")

    # File selection section
    tk.Label(root, text="Key File / Key Input:").grid(row=0, column=0, padx=10, pady=5)
    key_entry = tk.Entry(root, width=50)
    key_entry.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: select_file(key_entry)).grid(row=0, column=2, padx=10, pady=5)

    tk.Label(root, text="Plaintext File (for Encryption):").grid(row=1, column=0, padx=10, pady=5)
    plaintext_entry = tk.Entry(root, width=50)
    plaintext_entry.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: select_file(plaintext_entry)).grid(row=1, column=2, padx=10, pady=5)

    tk.Label(root, text="Encrypted File (for Decryption):").grid(row=2, column=0, padx=10, pady=5)
    encrypted_entry = tk.Entry(root, width=50)
    encrypted_entry.grid(row=2, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: select_file(encrypted_entry)).grid(row=2, column=2, padx=10, pady=5)

    # Action buttons
    tk.Button(root, text="Encrypt", command=perform_encryption).grid(row=3, column=0, padx=10, pady=10)
    tk.Button(root, text="Decrypt", command=perform_decryption).grid(row=3, column=1, padx=10, pady=10)

    # Status label
    status_label = tk.Label(root, text="", fg="blue")
    status_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    # Start the GUI
    root.mainloop()

# Run the GUI
cuneicrypt_gui()
