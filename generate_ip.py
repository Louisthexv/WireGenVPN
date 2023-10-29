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

# Function to save data to a text file
def save_data_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

# Function to generate a random pre-shared key
def generate_psk(length=32):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to generate peer configurations
def generate_peer_configurations(num_peers, use_psk):
    peer_configs = []
    for i in range(num_peers):
        peer_private_key, peer_public_key = generate_wireguard_keys()
        
        if use_psk:
            peer_psk = generate_psk()
            print(f"Generated pre-shared key for Peer {i + 1}: {peer_psk}")
        else:
            peer_psk = ""
        
        # Peer-specific settings
        peer_config = f"Peer {i + 1}:\n" \
                      f"  Public Key: {peer_public_key}\n" \
                      f"  Private Key: {peer_private_key}\n" \
                      f"  Pre-Shared Key: {peer_psk}\n"
        peer_configs.append(peer_config)

    return peer_configs

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
    
    # peer section and prompts

    num_peers = int(input("How many peers do you want to add? "))
    use_psk_for_peers = input("Do you want to use a pre-shared key for the peers (y/n)? ").strip().lower()
    if use_psk_for_peers == 'y':
        use_psk = True
    else:
        use_psk = False

    # Ask for server settings
    server_endpoint = input("Enter server endpoint (IPv4 or DDNS): ").strip()
    server_port = input("Enter server port (optional): ").strip()
    server_dns = input("Enter server DNS (optional): ").strip()

    # Generate server configuration
    server_config = f"Server:\n" \
                    f"  Server Public Key: {server_public_key}\n" \
                    f"  Server Private Key: {server_private_key}\n" \
                    f"  Pre-Shared Key for Server: {server_psk}\n" \
                    f"  Endpoint: {server_endpoint}\n" \
                    f"  Port: {server_port}\n" \
                    f"  DNS: {server_dns}\n"

    peer_configs = generate_peer_configurations(num_peers, use_psk)

    # Save server and peer configurations to the same text file
    filename = "wireguard_config.txt"
    data_to_save = server_config + "\n" + "\n".join(peer_configs)
    with open(filename, 'w') as file:
        file.write(data_to_save)

    print(f"Data saved to {filename}")