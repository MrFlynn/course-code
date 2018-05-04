# CS111 Homework #2, Problem #2
# Nick Pleatsikas
#
# Simple RSA Ciphertext Decryptor

# Define the alphabet from which to source from.
ALPHABET = 'abcdefghijklmnopqrstuvwxyz '

# Component of public key (N) and secret key (D)
N = 77
SECRET = 37

def main():
    # Store message and ciphertext
    message = []
    cipher = []

    # Open and read by line.
    with open('cipher.txt', 'r') as f:
        for line in f:
            cipher.append(int(line))

    # Convert cipher to plaintext by calculating index using standard decrypt
    # operation.
    for c in cipher:
        index = (c**SECRET) % N
        message.append(ALPHABET[index - 2])

    print(''.join(message))

if __name__ == '__main__':
    main()
