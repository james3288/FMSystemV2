from cryptography.fernet import Fernet
import random
import string

def generate_random_letters(length):
    letters = string.ascii_letters  # Contains all uppercase and lowercase letters
    random_letters = ''.join(random.choice(letters) for _ in range(length))
    return random_letters


def encrypt_number(number):
    # Generate a random key for encryption
    key = Fernet.generate_key()

    # Initialize the Fernet cipher with the key
    cipher = Fernet(key)

    # Convert the number to bytes (for AES encryption, it's common to use byte representation)
    number_bytes = number.to_bytes((number.bit_length() + 7) // 8, byteorder='big')
    
    # Encrypt the number bytes
    encrypted_bytes = cipher.encrypt(number_bytes)
    
    # Return the encrypted bytes
    return encrypted_bytes

def decrypt_number(encrypted_bytes):
    # Generate a random key for encryption
    key = Fernet.generate_key()

    # Initialize the Fernet cipher with the key
    cipher = Fernet(key)

    # Decrypt the encrypted bytes
    decrypted_bytes = cipher.decrypt(encrypted_bytes)
    
    # Convert the decrypted bytes back to an integer
    decrypted_number = int.from_bytes(decrypted_bytes, byteorder='big')
    
    # Return the decrypted number
    return decrypted_number