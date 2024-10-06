import os
from cryptography.fernet import Fernet

def decryption(files, KEY_FILE, EXTENSION):
    HEADER = b'encrypted::'
    decrypted_files = []

    # Read the decryption key
    try:
        with open(KEY_FILE, "rb") as theKey:
            key = theKey.read()
    except FileNotFoundError:
        print(f"Key file {KEY_FILE} not found.")
        return decrypted_files
    except Exception as e:
        print(f"An error occurred while reading the key file: {e}")
        return decrypted_files

    # Initialize the Fernet object with the key
    try:
        fernet = Fernet(key)
    except Exception as e:
        print(f"An error occurred while initializing the Fernet object: {e}")
        return decrypted_files

    for file in files:
        if not file.endswith(EXTENSION):
            continue

        # Read the file contents
        try:
            with open(file, "rb") as thefile:
                contents = thefile.read()
        except Exception as e:
            print(f"An error occurred while reading the file {file}: {e}")
            continue

        # Check if the file is already encrypted
        if not contents.startswith(HEADER):
            print(f"File {file} does not start with the expected header.")
            continue

        # Decrypt the file contents
        try:
            decrypted_content = fernet.decrypt(contents[len(HEADER):])
        except Exception as e:
            print(f"An error occurred while decrypting the file {file}: {e}")
            continue

        # Write the decrypted content back to the file
        try:
            with open(file, "wb") as thefile:
                thefile.write(decrypted_content)
        except Exception as e:
            print(f"An error occurred while writing the decrypted content to {file}: {e}")
            continue

        # Rename the file to remove the extension
        new_file_path = file.replace(EXTENSION, '')
        try:
            os.rename(file, new_file_path)
        except Exception as e:
            print(f"An error occurred while renaming the file {file}: {e}")
            continue

        decrypted_files.append(new_file_path)
        
    return decrypted_files
