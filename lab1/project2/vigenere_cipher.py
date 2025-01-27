def generate_key(msg, key):
    key = list(key)
    full_key = []
    key_index = 0

    for char in msg:
        if char.isalpha():  # Only extend the key for alphabetic characters
            full_key.append(key[key_index % len(key)])
            key_index += 1
        else:
            full_key.append(char)  # Retain non-alphabetic characters as-is

    return "".join(full_key)

class VigenereCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, msg):
        encrypted_text = []
        key = generate_key(msg, self.key.lower())  # Normalize key to lowercase
        for i in range(len(msg)):
            char = msg[i]
            if char.isupper():
                encrypted_char = chr((ord(char) + ord(key[i].upper()) - 2 * ord('A')) % 26 + ord('A'))
            elif char.islower():
                encrypted_char = chr((ord(char) + ord(key[i]) - 2 * ord('a')) % 26 + ord('a'))
            else:
                encrypted_char = char
            encrypted_text.append(encrypted_char)
        return "".join(encrypted_text)

    def decrypt(self, msg):
        decrypted_text = []
        key = generate_key(msg, self.key.lower())  # Normalize key to lowercase
        for i in range(len(msg)):
            char = msg[i]
            if char.isupper():
                decrypted_char = chr((ord(char) - ord(key[i].upper()) + 26) % 26 + ord('A'))
            elif char.islower():
                decrypted_char = chr((ord(char) - ord(key[i]) + 26) % 26 + ord('a'))
            else:
                decrypted_char = char
            decrypted_text.append(decrypted_char)
        return "".join(decrypted_text)
