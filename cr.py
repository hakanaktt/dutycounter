def encryptDB():
    from cryptography.fernet import Fernet

    # Generate a key and save it to a file
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)

    # Load the key
    with open('key.key', 'rb') as key_file:
        key = key_file.read()

    cipher_suite = Fernet(key)

    # Encrypt the database
    with open('db.db', 'rb') as db_file:
        encrypted_data = cipher_suite.encrypt(db_file.read())

    with open('db.db', 'wb') as db_file:
        db_file.write(encrypted_data)

def decryptDB():
    from cryptography.fernet import Fernet

    # Load the key
    with open('key.key', 'rb') as key_file:
        key = key_file.read()

    cipher_suite = Fernet(key)

    # Decrypt the database
    with open('db.db', 'rb') as db_file:
        decrypted_data = cipher_suite.decrypt(db_file.read())

    with open('db.db', 'wb') as db_file:
        db_file.write(decrypted_data)

decryptDB()