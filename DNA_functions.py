def to_binary_string(s):
    """Convert a string to a binary string."""
    return ''.join(format(ord(c), '08b') for c in s)

def binary_to_dna(binary_str):
    """Convert a binary string to a DNA sequence."""
    dna_mapping = {'00': 'T', '01': 'G', '10': 'C', '11': 'A'}
    return ''.join(dna_mapping[binary_str[i:i + 2]] for i in range(0, len(binary_str), 2))

def dna_to_binary(dna_str):
    """Convert a DNA sequence back to a binary string."""
    binary_mapping = {'T': '00', 'G': '01', 'C': '10', 'A': '11'}
    return ''.join(binary_mapping[c] for c in dna_str)

def binary_to_string(binary_str):
    """Convert a binary string back to the original string."""
    chars = []
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i + 8]
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def dna_encrypt(username, secret_code):
    """Encrypt username and secret_code into a DNA sequence."""
    username_bin = to_binary_string(username)
    secret_code_bin = to_binary_string(secret_code)

    # Pad the shorter binary string with zeros
    max_length = max(len(username_bin), len(secret_code_bin))
    username_bin = username_bin.zfill(max_length)
    secret_code_bin = secret_code_bin.zfill(max_length)

    # Perform bitwise XOR
    xor_result = int(username_bin, 2) ^ int(secret_code_bin, 2)
    xor_bin_str = format(xor_result, '0{}b'.format(max_length))

    # Convert to DNA sequence
    dna_sequence = binary_to_dna(xor_bin_str)
    return dna_sequence

def dna_decrypt(dna_sequence, username):
    """Decrypt the DNA sequence to get the secret_code."""
    # Convert DNA sequence back to binary
    xor_bin_str = dna_to_binary(dna_sequence)

    # Convert username to binary
    username_bin = to_binary_string(username)

    # Pad the username binary to match the XOR result
    max_length = len(xor_bin_str)
    username_bin = username_bin.zfill(max_length)

    # Calculate the secret_code binary using XOR
    secret_code_bin = int(xor_bin_str, 2) ^ int(username_bin, 2)
    secret_code_bin_str = format(secret_code_bin, '0{}b'.format(max_length))

    # Convert the binary string back to the secret_code
    secret_code = binary_to_string(secret_code_bin_str)
    return secret_code

# Example usage
# username = "user123"
# secret_code = "pass456"
# dna_sequence = dna_encrypt(username, secret_code)
# print(f"DNA Sequence: {dna_sequence}")

# To decrypt
# dna_sequence = "TTGGTGTCTGGCTTTGTTGGTTGATTGG"
# decrypted_secret_code = dna_decrypt(dna_sequence, username)
# print(f"Decrypted Secret Code: {decrypted_secret_code}")
