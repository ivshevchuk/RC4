import time
import docx

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def txt():
    with open("C:\\Users\\Device\\Desktop\\plaintext.txt", 'r', encoding="utf-8") as file:
        return file.read().strip()


def doc():
    doc = docx.Document("C:\\Users\\Device\\Desktop\\plaintext.docx")
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text

def ksa(key):
    s = list(range(256))
    len_key = len(key)
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len_key]) % 256
        s[i], s[j] = s[j], s[i]
    return s

def prga(s):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        k = s[(s[i] + s[j]) % 256]
        yield k

def ciphering(key, unicode_data):
    unicode_key = list(map(ord, key))
    stream_key = prga(ksa(unicode_key))
    result = list(map(lambda x, y: x ^ y, unicode_data, stream_key))
    return result

def encrypt(data, key):
    unicode_message = list(map(ord, data))
    result = ''
    for i in ciphering(key, unicode_message):
        result += "{:04d}".format(i)
    return result


def decrypt(key, data):
    unicode_message = [int(data[4 * _:4 * _ + 4]) for _ in
                       range(int(len(data) / 4))]
    result = ''
    for i in ciphering(key, unicode_message):
        result += chr(i)
    return result


def break_cipher(encoded_text, plaintext):
    processing_text = ""
    counter = 0
    key_list = [0] * len(plaintext)  # Створюємо список ключів

    while plaintext != processing_text:
        try:
            processing_text = decrypt("".join(map(str, key_list)), encoded_text)
        except UnicodeDecodeError:
            pass
        counter += 1
        update_keys(key_list)

    return processing_text, counter

def update_keys(key_list):
    # Збільшуємо останній ключ у списку на 1
    key_list[-1] += 1
    # Перевіряємо, чи потрібно збільшити інші ключі
    for i in range(len(key_list) - 1, 0, -1):
        if key_list[i] >= len(alphabet):
            key_list[i] = 0  # Скидаємо ключ на 0
            key_list[i - 1] += 1  # Збільшуємо попередній ключ на 1


plaintext = txt()
key = "key123"

print("Original text:", plaintext)

# Шифрування 
start_time = time.time()
encrypted = encrypt(plaintext, key)
encryption_time = time.time() - start_time
print("Encrypted text:", encrypted)
print("Encryption time:", encryption_time, "seconds")

# Дешифрування
start_time = time.time()
decrypted = decrypt(key, encrypted)
decryption_time = time.time() - start_time
print("Decrypted text:", decrypted)
print("Decryption time:", decryption_time, "seconds")

# Взлам
start_time = time.time()
hacked_text, iterations = break_cipher(encrypted, plaintext)
hacked_time = time.time() - start_time
print("Hacked text:", hacked_text)
print("Hacking time:", hacked_time, "seconds")