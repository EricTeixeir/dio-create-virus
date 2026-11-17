from cryptography.fernet import Fernet
import os

#1 load_key function to load the encryption key
def load_key():
    return open("chave.key", "rb").read()

#2 Decrypt files
def decrypt_file(file_path, key):
    f = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

#3 find_files function to find files in a directory
def find_files(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file not in ["Ransomware.py", "descrypt.py", "readme.txt"] and not file.endswith(".key"):
                file_paths.append(file_path)
    return file_paths

#4 exclude the key file from decryption
def exclude_key_file():
    if os.path.exists("chave.key"):
        os.remove("chave.key")

def main():
    if not os.path.exists("chave.key"):
        print("No encryption key found. Please ensure that the 'chave.key' file is present in the current directory.\n")
        return

    key = load_key()
    directory = os.getcwd()
    file_paths = find_files(directory)

    for file_path in file_paths:
        decrypt_file(file_path, key)
    print("All files have been decrypted successfully. Be careful!")   
    exclude_key_file()

if __name__ == "__main__":
    main()