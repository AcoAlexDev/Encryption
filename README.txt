This is all the information and documentation for the project.

Info: This was created to try out encrypting and decrypting.
I am a beginner in this field and this was my first time writing such an algorithm and was only made in about 3 afternoons.
Educational, not for production. No security guarantees.

Requirements: Python 3.10+; no external dependencies.

Why python?
With some parameters this algorithm can get very slow but I choose python because of easy readability, simple terminal execution
and fast writing. Tradeoff is slow speed.

There are two files you can execute in python terminal:
- python encryption.py: Uses settings from algorithm_settings.json and an operation mode
- python encryption_simple.py: Runs with predefined settings and encrypts/decrypts the same given message using a keyword.

encryption_simple.py inputs:
    message: The message that will be encrypted (then printed) and will then be decrypted again (then printed)
    key: The keyword is needed to encrypt the message in a complex way

encryption.py inputs:
    operation: Choose if message should be encrypted ('e'), decrypted ('d') or both ('b').

algorithm_settings.json (used for encryption.py only):

    IMPORTANT NOTE: These settings change the outcome of the algorithm changing these between encrypting and decrypting will print wrong outcome

    algorithm_choice: "s" = simple (using letters and numbers for encryption only. Symbols will not be encrypted and stay the same at the same postion.), "c" = complex (suggested, default),
    random_mapping_repeat: [int] how often 'random mapping' (Explanation in provide_random_mapping_dict() in encryption_simple.py) is repeated (default: 5). In the algorithm this is limited at 100 because it doesn't make it more secure
    but introduces long waiting times instead. Simple version uses length of key for this.
    mapping_depth: Remaps the message to more readable letters using test data from data_tables.py and the most used letters in english, making the encrypted message use more common letters:
                    0 = No Mapping,
                    1 = Mapping Once (default),
                    2 = Mapping already mapped again. Processes data_keys * data_messages = 1824 times.
                    2+ = Needs a lot of process power. Encrypted message should appear very readable.
    test_data_usage_percentage: How much Test Data is used for letter-mapping. Max: 1.0 (default), Min: 0.0. The higher the more performance is needed.
                                When the algorithm takes too long, try decreasing / halving this value first


Algorithm Explaination can be found in encryption_simple.py for each step.

TODOs:
Print an approx. duration how long the encryption/decryption with the current parameters will take

© Alexander Eckstein, 11.08.2025