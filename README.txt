This is all the information and documentation for the project.

© Alexander Eckstein, 11.08.2025

Info: This was created to try out encrypting and decrypting.
I am a beginner in this field and this was my first time writing such an algorithm and was only made in about 3 afternoons.
It should be bug-free and working but no warranty

There are two files you can execute in python terminal:
- encryption.py
- encryption_simple.py

They use the same algorithms but encryption_simple.py has pre-defined 'settings' and just encrypts and decrypts the same given message using a keyword.

encryption_simple.py inputs:
    message: The message that will be encrypted (then printed) and will then be decrypted again (then printed)
    key: The keyword is needed to encrypt the message in a safe, complex way

encryption.py inputs:
    operation: Choose if message should be encrypted, decrypted or both.

algorithm_settings.json (used for encryption.py only):

    iMPORTANT NOTE: These settings change the outcome of the algorithm changing these between encrypting and decrypting will print wrong outcome

    algorithm_choice: "s" = simple (using letters and numbers for encryption only. Symbols stay the same.), "c" = complex (suggested, default),
    random_mapping_repeat: [int] how often random mapping is repeated (default: 5), simple version uses length of key for this
    mapping_depth: Remaps the password to more readable letters using test data and the most used letters in english:
                    0 = No Mapping,
                    1 = Mapping Once (default),
                    2 = Mapping already mapped again. Processes data_keys * data_messages = 1824 times.
    test_data_usage_percentage: How much Test Data is used for letter-mapping. Max: 1.0 (default), Min: 0.0. The higher the more performance is needed.
                                When the algorithm takes too long, try decreasing / halfing this value first


Algorithm Explaination can be found in encryption_simple.py for each step.