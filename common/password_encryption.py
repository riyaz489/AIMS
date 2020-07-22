""" this file is used to perform data encryption and decryption operations."""

import yaml
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

f = ""
with open("aims/config.yaml", 'r') as ymlfile:
    """
    getting salt from yaml config file.
    """
    cfg = yaml.safe_load(ymlfile)
    salt = str(cfg['enc']['salt']).encode()
    enc_password = str(cfg['enc']['salt']).encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(enc_password))
    f = Fernet(key=key)


def encrypt_pass(password):
    """
    this method is used to encrypt data.
    :param password: string, password.
    :return: string, encrypted password.
    """
    return (f.encrypt(password.encode())).decode("utf-8")


def decrypt_pass(encoded_cipher):
    """
    this method is used to decrypt data.
    :param encoded_cipher: encoded data.
    :return: decrypted password.
    """
    return (f.decrypt(encoded_cipher)).decode("utf-8")

