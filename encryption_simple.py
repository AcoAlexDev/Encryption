from enum import Enum
import random
import time
import data_tables

## I like to use enum parameters for readability and to avoid string typos.
class Algorithms(Enum):
    ENCRYPT = 'encrypt'
    DECRYPT = 'decrypt'

## Performs a full encryption process
def encrypt(message: str, key: str, content:list[str], mapping_depth:int = 0) -> str:
    message:str = shuffle_content(key, message, Algorithms.ENCRYPT, content)
    message = algorithm(key, message, Algorithms.ENCRYPT, content)
    for i in range(len(key)):
        message = mapping_algorithm(message, Algorithms.ENCRYPT, provide_random_mapping_dict(key, content))
    for i in range(mapping_depth):
        message = mapping_algorithm(message, Algorithms.ENCRYPT, provide_most_used_mapping_dict(content, i, key, message))
    return message

## Performs a full decryption process
def decrypt(message: str, key: str, content:list[str], mapping_depth:int = 0) -> str:
    for i in range(mapping_depth):
        message = mapping_algorithm(message, Algorithms.DECRYPT, provide_most_used_mapping_dict(content, mapping_depth-i-1, key, message))
    for i in range(len(key)):
        message = mapping_algorithm(message, Algorithms.DECRYPT, provide_random_mapping_dict(key, content))
    message:str = algorithm(key, message, Algorithms.DECRYPT, content)
    message = shuffle_content(key, message, Algorithms.DECRYPT, content)
    return message

## Shifts the characters in the message using content (=approx. a list of the alphabet you can see in data_tables.py)
## based on the key and the reversed key.
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
            ## Note: If the character is unrecognised (not in the content alphabet), it is added unchanged.
            ## This applies for all algorithms.
            result += message[i]
    return result

## Shifts the characters in the message using content (=approx. a list of the alphabet you can see in data_tables.py)
## based on the key and a multiplier of the first character in the key.
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
            
            new_index = new_index % len(content)

            result += content[new_index]
        else:
            result += message[i]
    return result

## Returns a mapping_dict for mapping_algorithm() that maps characters randomly based on the key.
## In encrypt() and decrypt() you can see this step is repeated for the amount of characters in the key,
## in encryption.py this is a setting in alorithm_settings.json. 
def provide_random_mapping_dict(key: str, content:list[str]) -> dict:
    mapping_dict:dict = {}
    for i in range(len(content)):
        mapping_dict[content[i]] = content[i]
    temp = list(mapping_dict.values())
    random.seed(algorithm(key, key, Algorithms.ENCRYPT, content))
    random.shuffle(temp)
    mapping_dict = dict(zip(mapping_dict, temp))
    return mapping_dict

## Returns a mapping_dict for mapping_algorithm() that maps the most used characters that occur in encrypted messages of the test data using all other algorithms so far.
## These are mapped to the most used letters in the (English/German) language to make the encryption appear more natural/readable. To really see a effect of this,
## you need to use a higher mapping_depth but processing all encryptions before is what takes the most time here.
def provide_most_used_mapping_dict(content:list[str], mapping_depth:int = 0, key:str="", message:str="") -> dict:
    most_used_letters_in_encryption:dict = {}

    for i in range(round(len(data_tables.testing_keys) * 0.5)):
        for j in range(round(len(data_tables.testing_messages) * 0.5)):
            encrypted_message = encrypt(data_tables.testing_messages[j], data_tables.testing_keys[i], content, mapping_depth)
            for char in encrypted_message:
                most_used_letters_in_encryption[char] = most_used_letters_in_encryption.get(char, 0) + 1
    
    mapping_dict:dict = {}
    if not len(most_used_letters_in_encryption) == len(data_tables.most_used_letters_english):
        for char in data_tables.most_used_letters_english:
            most_used_letters_in_encryption[char] = 0
    if not len(most_used_letters_in_encryption) == len(data_tables.most_used_letters_english):
        print("Error: The number of unique characters in the encrypted messages does not match the expected number.")
    for i in range(len(data_tables.most_used_letters_english)):
        mapping_dict[list(most_used_letters_in_encryption.keys())[i]] = data_tables.most_used_letters_english[i]
    return mapping_dict

## Remaps all characters in the message to another character based on the mapping_dict (functions on top).
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

## Main sets up all variables, handles user input, runs the encryption/decryption process and prints output.
def main() -> None:
    print('-' * 40)
    print('Welcome to the Aco Ecryption/Decryption Tool (SIMPLIFIED OPTIONS VERSION) V' + version)
    time.sleep(1.0)

    ## These are the variables that are automatically setup in the simple version.
    ## Also in encryption.py you can choose a operation (encrypt, decrypt), here it will always encrypt your message,
    ## and then decrypt the same message back. 
    content:list[str] = data_tables.symbols_complex
    mapping_depth:int = 1
    # english mapping dict uses only half of the data_tables.testing_keys and testing_messages

    ## The key (also: keyword / password) is needed from both users to encrypt and decrypt the same message.
    key:str = input("Enter a key: ")
    while not key:
        key = input("Key can't be empty. Please enter a key: ")

    ## The message is the text that will be encrypted and decrypted.
    message:str = input("Enter a message: ")
    while not message:
        message = input("Message can't be empty. Please enter a message: ")

    ## The content (alphabet/symbol list) is also randomised with the key to make it more secure.
    random.seed(key)
    random.shuffle(content)
    
    encrypted:str = encrypt(message, key, content, mapping_depth)
    ## To avoid problems when copying/pasting/decrypting, the last character of the encrypted message is replaced with a star (★) if it is a space.
    if encrypted.endswith(' '):
        encrypted += '★'
    print('Encrypted:', encrypted)

    if encrypted.endswith('★'):
        encrypted = encrypted[:-1]
    
    decrypted:str = decrypt(encrypted, key, content, mapping_depth)
    print('Decrypted:', decrypted)

    if decrypted == message:
        print("✓ Encryption/Decryption successful!")
    else:
        print("✗ Fail: Decryption doesn't match original message")

version:str = '1.0'
main()