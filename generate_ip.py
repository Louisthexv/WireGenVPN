import random
import string
import subprocess

# Function to generate WireGuard Keys
def generate_wireguard_keys():
    # Generate server private key
    server_private_key = subprocess.check_output(['wg', 'genkey']).strip().decode('utf-8')

    # Generate server public key
    server_public_key = subprocess.check_output(['wg', 'pubkey'], input=server_private_key.encode()).strip().decode('utf-8')

    return server_private_key, server_public_key

# Function to generate a random pre-shared key
def generate_psk(length=32):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to generate peer configurations
def generate_peer_configurations(num_peers, use_psk, server_ip, server_endpoint):
    peer_configs = []

    server_ip_parts = server_ip.split('.')
    server_class = server_ip_parts[0]

    for i in range(num_peers):
        peer_private_key, peer_public_key = generate_wireguard_keys()

        if use_psk:
            peer_psk = generate_psk()
            print(f"Generated pre-shared key for Peer {i + 1}: {peer_psk}")
        else:
            peer_psk = ""

        # Peer-specific settings
        peer_ip = f"{server_class}.{server_ip_parts[1]}.{server_ip_parts[2]}.{i + 2}"  # Increment last octet for peers
        allowed_ips = "0.0.0.0/0, ::/0"  # Default AllowedIPs (can be changed manually)

        peer_config = f"Peer {i + 1}:\n" \
                      f"  IP Address: {peer_ip}/24\n" \
                      f"  Public Key: {peer_public_key} | wg pubkey\n" \
                      f"  Private Key: {peer_private_key}\n" \
                      f"  Pre-Shared Key: {peer_psk}\n" \
                      f"  AllowedIPs: {allowed_ips}\n" \
                      f"  Endpoint: {server_endpoint}\n"

        peer_configs.append(peer_config)

    return peer_configs

if __name__ == "__main__":
    # Ask the user for the server IP address
    server_ip = input("Enter the IP address for the server (e.g., x.x.x.1): ").strip()

    # Prompt for server settings
    server_endpoint = input("Enter server endpoint (IPv4 or DDNS): ").strip()
    server_port = "51820"  # Default WireGuard port for the server
    server_dns = input("Enter server DNS (optional): ").strip()

    # Generate server keys
    server_private_key, server_public_key = generate_wireguard_keys()
    server_psk = generate_psk()  # Generate pre-shared key for the server

    # Prompt for peer settings
    num_peers = int(input("How many peers do you want to add? "))
    use_psk_for_peers = input("Do you want to use a pre-shared key for the peers (y/n)? ").strip().lower()
    if use_psk_for_peers == 'y':
        use_psk = True
    else:
        use_psk = False

    # Generate server configuration
    server_config = f"WireGuard Server\n\nInterface\n  IP Address: {server_ip}/24\n  Server Public Key: {server_public_key} | wg pubkey\n  Server Private Key: {server_private_key}\n  Pre-Shared Key for Server: {server_psk}\n  Endpoint: {server_endpoint}\n  Port: {server_port}\n  DNS: {server_dns}\n\n"

    peer_configs = generate_peer_configurations(num_peers, use_psk, server_ip, server_endpoint)

    # Save server and peer configurations to the same text file
    filename = "wireguard_config.txt"
    data_to_save = server_config + "\n".join(peer_configs)
    with open(filename, 'w') as file:
        file.write(data_to_save)

    print(f"Data saved to {filename}")
