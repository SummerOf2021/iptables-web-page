from cryptography.fernet import Fernet


def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)



def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()

def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
        # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open("encrypted_iptables.txt", "wb") as file:
        file.write(encrypted_data)

def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open("decrypted_iptables.txt", "wb") as file:
        file.write(decrypted_data)

# generate and write a new key
write_key()
# load the previously generated key
key = load_key()
'''
file = "iptables_Save.txt"

encrypt(file, key)
# decrypt the file
decrypt("encrypted_iptables.txt", key)

'''

