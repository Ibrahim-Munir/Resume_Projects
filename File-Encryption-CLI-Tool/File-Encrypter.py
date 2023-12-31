import argparse
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def generate_symmetric_key():
    return os.urandom(32)


def generate_asymmetric_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def encrypt_file_symmetric(input_file, output_file, key):
    with open(input_file, 'rb') as file:
        plaintext = file.read()

    iv = b'\x00' * 16  # Initialization vector for AES
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    with open(output_file, 'wb') as file:
        file.write(ciphertext)


def decrypt_file_symmetric(input_file, output_file, key):
    with open(input_file, 'rb') as file:
        ciphertext = file.read()

    iv = b'\x00' * 16  # Initialization vector for AES
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    with open(output_file, 'wb') as file:
        file.write(plaintext)


def encrypt_file_asymmetric(input_file, output_file, public_key):
    with open(input_file, 'rb') as file:
        plaintext = file.read()

    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(output_file, 'wb') as file:
        file.write(ciphertext)


def decrypt_file_asymmetric(input_file, output_file, private_key):
    with open(input_file, 'rb') as file:
        ciphertext = file.read()

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(output_file, 'wb') as file:
        file.write(plaintext)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Encryption Tool")
    parser.add_argument("input_file", help="Input file to encrypt/decrypt")
    parser.add_argument("output_file", help="Output file after encryption/decryption")
    parser.add_argument("encryption_type", choices=["symmetric_encrypt", "symmetric_decrypt", "asymmetric_encrypt", "asymmetric_decrypt"],
                        help="Type of encryption/decryption")

    args = parser.parse_args()

    if args.encryption_type == "symmetric_encrypt":
        key = generate_symmetric_key()
        encrypt_file_symmetric(args.input_file, args.output_file, key)
        print(f"File encrypted using symmetric encryption and saved to {args.output_file}")

    elif args.encryption_type == "symmetric_decrypt":
        # For demonstration purposes only
        key = generate_symmetric_key()
        decrypt_file_symmetric(args.input_file, args.output_file, key)
        print(f"File decrypted using symmetric decryption and saved to {args.output_file}")

    elif args.encryption_type == "asymmetric_encrypt":
        private_key, public_key = generate_asymmetric_keys()
        encrypt_file_asymmetric(args.input_file, args.output_file, public_key)
        print(f"File encrypted using asymmetric encryption and saved to {args.output_file}")

    elif args.encryption_type == "asymmetric_decrypt":
        # For demonstration purposes only
        private_key, _ = generate_asymmetric_keys()
        decrypt_file_asymmetric(args.input_file, args.output_file, private_key)
        print(f"File decrypted using asymmetric decryption and saved to {args.output_file}")

_
