import os
import secrets
import base64

# Function to generate a WireGuard private key
def generate_private_key():
    private_key = secrets.token_bytes(32)
    return base64.b64encode(private_key).decode('utf-8')

# Function to generate a PSK
def generate_preshared_key():
    psk = secrets.token_bytes(32)
    return base64.b64encode(psk).decode('utf-8')

# Function to generate a WireGuard public key from a private key
def generate_public_key(private_key):
    return os.popen(f"echo '{private_key}' | wg pubkey").read().strip()

# Function to generate a WireGuard configuration file for the server
def generate_server_config(private_key, server_address, listen_port, use_psk, num_peers):
    config = f"[Interface]\n"
    # Add an extra blank line between for better parsing [Interface] sections
    config += "\n"
    config += f"Address = {server_address}/24\n"
    # Add an extra blank line between for better parsing [Interface] sections
    config += "\n"
    config += f"ListenPort = {listen_port}\n"
    # Add an extra blank line between for better parsing [Interface] sections
    config += "\n"
    config += f"PrivateKey = {private_key}\n\n"
    config += "\n"
    config += "\n"
    
    if use_psk:
        server_octets = server_address.split('.')  # Split the server address into octets
        for i in range(num_peers):
            psk = generate_preshared_key()
            client_octet = i + 2  # Start from 2 and increment for each peer
            client_address = f"{server_octets[0]}.{server_octets[1]}.{server_octets[2]}.{client_octet}/32"
            
            config += f"[Peer]\n"
            # Add an extra blank line between for better parsing  [Peer] sections
            config += "\n"
            config += f"PublicKey = {generate_public_key(private_key)}\n"
            # Add an extra blank line between for better parsing [Peer] sections
            config += "\n"
            config += f"PresharedKey = {psk}\n"
            # Add an extra blank line between for better parsing  [Peer] sections
            config += "\n"
            config += f"AllowedIPs = {client_address}\n"
            
            # Add an extra blank line between for better parsing  [Peer] sections
            config += "\n"
            config += "\n"

    return config

# Function to generate a WireGuard configuration file for a peer
def generate_peer_config(private_key, client_address, listen_port, server_public_key, use_psk, server_endpoint):
    config = f"[Interface]\n"
    # Add an extra blank line between for better parsing [Interface] sections
    config += "\n"
    config += f"Address = {client_address}\n"
    # Add an extra blank line between for better parsing [Interface] sections
    config += "\n"
    config += f"ListenPort = {listen_port}\n"
    # Add an extra blank line between for better parsing [Interface] sections
    config += "\n"
    config += f"PrivateKey = {private_key}\n\n"
    # Add an extra blank line between for better parsing [Interface] sections
    config += "\n"
    config += "\n"
    config += f"[Peer]\n"
    # Add an extra blank line between for better parsing [Interface] sections
    config += "\n"
    config += f"PublicKey = {server_public_key}\n"
    config += "\n"
    
    if use_psk:
        psk = generate_preshared_key()
        config += f"PresharedKey = {psk}\n"
        # Add an extra blank line between for better parsing [Interface] sections
        config += "\n"
        config += f"AllowedIPs = 0.0.0.0/0, ::/0\n"
        # Add an extra blank line between for better parsing [Interface] sections
        config += "\n"
        config += f"Endpoint = {server_endpoint}:{listen_port}\n"

    return config

# Gather user input for network settings
server_private_key = generate_private_key()

# Gather user input for server settings
server_address = input("Enter the server's network address CIDR (e.g., X.X.X.1): ")
server_listen_port = input("Enter the server's listen port (default 51820): ")
use_psk = input("Add an extra layer of security with a PSK (yes/no): ").lower() == "yes"
server_endpoint = input("Enter the server's external address (IPV4) or DDNS: ")
num_clients = int(input("Enter the number of clients: "))

# Generate server public key
server_public_key = generate_public_key(server_private_key)

# Generate server configuration
server_config = generate_server_config(server_private_key, server_address, server_listen_port, use_psk, num_clients)

# Gather user input for client settings
# Initialize the clients list with the first client using the server address
clients = []
for i in range(1, num_clients + 1):  # Start at 1 and end at num_clients
    client_private_key = generate_private_key()
    use_psk_for_client = use_psk  # Use the same PSK for all clients
    client_octet = i + 1  # Increment the octet
    client_address = f"{server_address.rsplit('.', 1)[0]}.{client_octet}/24"
    clients.append({
        "private_key": client_private_key,
        "address": client_address,
        "use_psk": use_psk_for_client
    })

# Generate client configurations
for i, client in enumerate(clients):
    client_config = generate_peer_config(
        client["private_key"],
        client["address"],
        server_listen_port,
        server_public_key,
        client["use_psk"],
        server_endpoint
    )
    
    # Save the client configuration to a file
    with open(f"client{i + 1}.conf", "w") as client_file:
        client_file.write(client_config)

# Save the server configuration to a file
with open("server.conf", "w") as server_file:
    server_file.write(server_config + '\n\n')

print("Configuration files generated.")
