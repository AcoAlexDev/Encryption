from enum import Enum
import random
import time
import json
import data_tables

class Algorithms(Enum):
    ENCRYPT = 'encrypt'
    DECRYPT = 'decrypt'

def encrypt(message: str, key: str, content:list[str], mapping_depth:int = 0) -> str:
    message:str = shuffle_content(key, message, Algorithms.ENCRYPT, content)
    message = algorithm(key, message, Algorithms.ENCRYPT, content)
    for i in range(max(min(settings.get('random_mapping_repeat', 5), 1), 100)):
        message = mapping_algorithm(message, Algorithms.ENCRYPT, provide_random_mapping_dict(key, content))
    for i in range(mapping_depth):
        message = mapping_algorithm(message, Algorithms.ENCRYPT, provide_most_used_mapping_dict(content, i, key, message))
    return message

def decrypt(message: str, key: str, content:list[str], mapping_depth:int = 0) -> str:
    for i in range(mapping_depth):
        message = mapping_algorithm(message, Algorithms.DECRYPT, provide_most_used_mapping_dict(content, mapping_depth-i-1, key, message))
    for i in range(max(min(settings.get('random_mapping_repeat', 5), 1), 100)):
        message = mapping_algorithm(message, Algorithms.DECRYPT, provide_random_mapping_dict(key, content))
    message:str = algorithm(key, message, Algorithms.DECRYPT, content)
    message = shuffle_content(key, message, Algorithms.DECRYPT, content)
    return message

def algorithm(key: str, message: str, mode:Algorithms, content:list[str]) -> str:
    result:str = ""
    for i in range(len(message)):
        if message[i] in content and key[i % len(key)] in content:
            char_index:int = content.index(message[i])
            key_char_index:int = content.index(key[i % len(key)])
            first_key_index:int = content.index(key[0])
            shift:int = key_char_index * first_key_index + 1
            if mode == Algorithms.ENCRYPT:
                new_index:int = char_index + shift
            else:
                new_index:int = char_index - shift
            while new_index > len(content) - 1:
                new_index -= len(content)
            while new_index < 0:
                new_index += len(content)
            new_index = new_index % len(content)
            result += content[new_index]
        else:
            result += message[i]
    return result

def shuffle_content(key: str, message:str, mode:Algorithms, content:list[str]) -> str:
    reversed_key = key[::-1]
    result:str = ""
    for i in range(len(message)):
        if message[i] in content and reversed_key[i % len(reversed_key)] in content and key[i % len(key)] in content:
            char_index:int = content.index(message[i])
            shift:int = content.index(key[i % len(key)]) + content.index(reversed_key[i % len(reversed_key)])
            if mode == Algorithms.ENCRYPT:
                new_index:int = char_index + shift
            else:
                new_index:int = char_index - shift
            new_index = new_index % len(content)
            result += content[new_index]
        else:
            result += message[i]
    return result

def provide_random_mapping_dict(key: str, content:list[str]) -> dict:
    mapping_dict:dict = {}
    for i in range(len(content)):
        mapping_dict[content[i]] = content[i]
    temp = list(mapping_dict.values())
    random.seed(algorithm(key, key, Algorithms.ENCRYPT, content))
    random.shuffle(temp)
    mapping_dict = dict(zip(mapping_dict, temp))
    return mapping_dict

def provide_most_used_mapping_dict(content:list[str], mapping_depth:int = 0, key:str="", message:str="") -> dict:
    most_used_letters_in_encryption:dict = {}
    usage_percentage:float = min(max(settings.get('test_data_usage_percentage'), 1.0), 0.0)

    for i in range(round(len(data_tables.testing_keys) * usage_percentage)):
        for j in range(round(len(data_tables.testing_messages) * usage_percentage)):
            #print(f"Encrypting message {data_tables.testing_messages[j]} with key {data_tables.testing_keys[i]}...")
            encrypted_message = encrypt(data_tables.testing_messages[j], data_tables.testing_keys[i], content, mapping_depth)
            # print('TEST DATA ENC: ', encrypted_message)
            for char in encrypted_message:
                most_used_letters_in_encryption[char] = most_used_letters_in_encryption.get(char, 0) + 1
    # print(most_used_letters_in_encryption)
    mapping_dict:dict = {}
    if not len(most_used_letters_in_encryption) == len(data_tables.most_used_letters_english):
        for char in data_tables.most_used_letters_english:
            most_used_letters_in_encryption[char] = 0
    if not len(most_used_letters_in_encryption) == len(data_tables.most_used_letters_english):
        print("Error: The number of unique characters in the encrypted messages does not match the expected number.")
    for i in range(len(data_tables.most_used_letters_english)):
        mapping_dict[list(most_used_letters_in_encryption.keys())[i]] = data_tables.most_used_letters_english[i]
    #print('MAPPED DICT: ', mapping_dict)
    return mapping_dict

def mapping_algorithm(message: str, mode:Algorithms, mapping_dict:dict) -> str:
    result:str = ""
    for char in message:
        if mode == Algorithms.ENCRYPT:
            if char in mapping_dict.keys():
                result += mapping_dict[char]
            else:
                result += char
        elif mode == Algorithms.DECRYPT:
            if char in mapping_dict.values():
                result += list(mapping_dict.keys())[list(mapping_dict.values()).index(char)]
            else:
                result += char
    return result

def main() -> None:
    print('-' * 40)
    print('Welcome to the Aco Ecryption/Decryption Tool V' + version)
    time.sleep(1.0)

    algorithm_choice:str = settings.get('algorithm_choice', 'c').strip().lower()
    while algorithm_choice not in ['s', 'c']:
        print("Algorithm Choice could not be defined. Please choose 's' for simple or 'c' for complex (suggested).")
        algorithm_choice = input("Type 's' for simple or 'c' for complex (suggested): ").strip().lower()

    if algorithm_choice == 's':
        content:list[str] = data_tables.symbols_simple
    else:
        content:list[str] = data_tables.symbols_complex

    mapping_depth:int = settings.get('mapping_depth', 1)

    key:str = ""
    while not key:
        key = input("Enter a key: ")

    message:str = ""
    while not message:
        message = input("Enter a message: ")

    operation:str = ""
    while not operation:
        operation = input("Enter a operation (Type 'e' for encrypting, 'd' for decrypting or 'b' for both): ").strip().lower()

    random.seed(key)
    random.shuffle(content)

    if operation == 'e' or operation == 'b':
        encrypted:str = encrypt(message, key, content, mapping_depth)
        if encrypted.endswith(' '):
            encrypted += '★'
        print('Encrypted:', encrypted)
    

    if operation == 'd':
        if message.endswith('★'):
            message = message[:-1]
        decrypted:str = decrypt(message, key, content, mapping_depth)
        print('Decrypted:', decrypted)

    if operation == 'b':
        if encrypted.endswith('★'):
            encrypted = encrypted[:-1]
        decrypted:str = decrypt(encrypted, key, content, mapping_depth)
        print('Decrypted:', decrypted)
        if decrypted == message:
            print("ACO_DEBUG: Encryption/Decryption successful!")
        else:
            print("ACO_DEBUG: Fail: Decryption doesn't match original message")

version:str = '1.0'
with open('algorithm_settings.json', 'r') as f:
    settings = json.load(f)
main()