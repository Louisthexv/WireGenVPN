import random
import string
import subprocess

# Function to create network address
def generate_random_ip(class_type):
    if class_type == 'A':
        first_octect = random.randint(1, 126)
    elif class_type == 'B':
        first_octect = random.randint(128, 191)
    elif class_type == 'C':
        first_octect = random.randint(192, 223)
    else:
        return "Invalid Class Type"

    last_octec = random.randint(2, 254) # Avoid 0 and 1 for potential server devices
    return f"{first_octect}.0.0.{last_octec}"

# Function to generate WireGuard Keys
def generate_wireguard_keys():
    # generate server private key
    server_private_key = subprocess.check_output(['wg', 'genkey']).strip().decode('utf-8')

    # generate server public key
    server_public_key = subprocess.check_output(['echo', f'{server_private_key}','|', 'wg', 'pubkey']).strip().decode('utf-8')

    return server_private_key, server_public_key

# Function to generate a random pre-shared key
def generate_psk(length=32):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

if __name__ == "__main__":
    class_type = input("Choose a network class (A/B/C): ").strip().upper() # allows the user to input their choice for class.
    random_ip = generate_random_ip(class_type)
    print(f"Random IP address in Class {class_type}: {random_ip}")

    generate_psk_option = input("Do you want to generate a pre-shared key for the server (y/n)? ").strip().lower()
    if generate_psk_option == 'y':
        server_psk = generate_psk()
        print(f"Generated server pre-shared key: {server_psk}")
    else:
        server_psk = ""

    server_private_key, server_public_key = generate_wireguard_keys()
    
    print(f"Random IP address in Class {class_type}: {random_ip}")
    print(f"Server Private Key: {server_private_key}")
    print(f"Server Public Key: {server_public_key}")