import tkinter as tk
from tkinter import filedialog, messagebox
import os

def read_key(filename):
    """Function to read key from user input file"""
    with open(filename, "r") as key_text:
        content = key_text.read().strip()
    return content

def char_initialization():
    """Function to initialize both sets of ASCII and Cuneiform characters by their unicode"""
    cuneiform_chars = [chr(i) for i in range(0x12000, 0x12255)]
    ascii_chars = [chr(i) for i in range(0, 255)]
    return cuneiform_chars, ascii_chars

def char_mapping(cuneiform, ascii):
    """Function to map ASCII and Cuneiform characters in a dictionary"""
    mapped_dict = {key: value for key, value in zip(ascii, cuneiform)}
    return mapped_dict

def encrypt_file(mapping, plaintext_file, key, output_file="encrypted.txt"):
    """Function to encrypt to a file using user input plaintext and key"""
    with open(plaintext_file, "r") as plaintext:
        content = plaintext.read()

    key_length = len(key)
    subbed_content = []

    # For loop to map plaintext characters to respective Cuneiform character
    for i, char in enumerate(content):
        mapped_char = mapping.get(char, char)

        # Using key to perform a bitwise XOR between ASCII values and the key character
        if key_length > 0:
            key_char = key[i % key_length]
            encrypted_char = chr(ord(mapped_char) ^ ord(key_char))
        else:
            encrypted_char = mapped_char    # No key, no changes

        subbed_content.append(encrypted_char)   # Append encrypted characters to subbed content

    subbed_content_str = ''.join(subbed_content)[::-1]  # Perform a reversal of the string

    # Write the encrypted data to encrypted.txt
    with open(output_file, "w+") as enc_text:
        enc_text.write(subbed_content_str)

    messagebox.showinfo("Success", f"Encryption complete. Encrypted file created as {output_file}.")

def decrypt_file(mapping, encrypted_file, key, output_file="decrypted.txt"):
    """Function to decrypt user input encrypted file using key"""
    reverse_mapping = {v: k for k, v in mapping.items()}    # Initialize reverse map for decryption

    # Read content of user input encrypted file
    with open(encrypted_file, "r") as encrypted_text:
        content = encrypted_text.read()

    content = content[::-1]     # Reverse the contents of encrypted file

    key_length = len(key)
    decrypted_text = []
    
    # For loop to reverse bitwise XOR operation on data
    for i, char in enumerate(content):
        if key_length > 0:
            key_char = key[i % key_length]
            decrypted_char = chr(ord(char) ^ ord(key_char))
        else:
            decrypted_char = char

        original_char = reverse_mapping.get(decrypted_char, decrypted_char)     # Map back to original characters
        decrypted_text.append(original_char)    # Append original characters to decrypted string

    decrypted_text_str = ''.join(decrypted_text)    # Join decrypted characters

    # Write decrypted content to decrypted.txt
    with open(output_file, "w+") as dec_text:
        dec_text.write(decrypted_text_str)

    messagebox.showinfo("Success", f"Decryption complete. Decrypted file created as {output_file}.")

def select_file(label, var):
    """Function to prompt user for plaintext/encrypted file"""
    filename = filedialog.askopenfilename()
    if filename:
        var.set(filename)
        label.config(text=f"Selected File: {os.path.basename(filename)}")

def select_key_file(label, var):
    """Function to prompt user for key file"""
    filename = filedialog.askopenfilename()
    if filename:
        var.set(filename)
        label.config(text=f"Selected Key File: {os.path.basename(filename)}")

def start_encryption(mapping, file_var, key_var):
    """Function to initiate encryption process"""
    key = ""
    if key_var.get():
        key = read_key(key_var.get())
    
    encrypt_file(mapping, file_var.get(), key)

def start_decryption(mapping, file_var, key_var):
    """Function to initiate decryption process"""
    key = ""
    if key_var.get():
        key = read_key(key_var.get())

    decrypt_file(mapping, file_var.get(), key)
    
def create_gui():
    """Function to create GUI elements"""
    root = tk.Tk()
    root.title("Cuneicrypt")
    root.geometry("600x400")
    
    cuneiform_chars, ascii_chars = char_initialization()
    mapped_dict = char_mapping(cuneiform_chars, ascii_chars)
    
    file_var = tk.StringVar()
    key_var = tk.StringVar()
    
    tk.Label(root, text="Cuneicrypt", font=("Helvetica", 16)).pack(pady=10)

    file_label = tk.Label(root, text="No file selected")
    file_label.pack(pady=(35, 5))
    
    tk.Button(root, text="Select File", command=lambda: select_file(file_label, file_var)).pack(pady=5)

    key_label = tk.Label(root, text="No key file selected (Optional)")
    key_label.pack(pady=5)
    tk.Button(root, text="Select Key File", command=lambda: select_key_file(key_label, key_var)).pack(pady=5)

    tk.Label(root, text="").pack(pady=20)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Encrypt", command=lambda: start_encryption(mapped_dict, file_var, key_var)).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Decrypt", command=lambda: start_decryption(mapped_dict, file_var, key_var)).grid(row=0, column=1, padx=10)

    root.mainloop()

create_gui()