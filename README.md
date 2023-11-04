# WireGenVPN

WireGenVPN is a Python tool designed to simplify the process of setting up WireGuard VPN servers and clients for OpenWRT routers. It was created to address the challenges of configuring WireGuard interfaces and peers, especially dealing with issues like subnet conflicts. This tool streamlines the configuration process by prompting users for input regarding the desired subnet and the number of clients they wish to add to the server.

## Features

- **Subnet Configuration:** WireGenVPN prompts users to specify the subnet for their WireGuard VPN, making it easier to avoid conflicts and ensure proper routing.

- **Client Configuration:** Users can specify the number of clients they want to create, and the tool generates corresponding configuration files for each client.

- **Export Configurations:** The tool creates two types of configuration files. The first is the server configuration file, and the second set comprises individual client configuration files. These files can be saved for later use, exported for travel routers (e.g., GL.iNet), or stored in the cloud for easy access.

## Usage

To get started with WireGenVPN, follow these simple steps:

1. Clone the repository to your local machine.
2. Run the Python script on a computer that can execute Python.
3. Follow the prompts to configure the WireGuard server and client parameters.
4. The tool will generate configuration files for the server and all specified clients.

## Compatibility

While WireGenVPN was initially created for OpenWRT routers, it can be used in various environments where WireGuard is needed. Whether you're working with a virtual machine, a Linux container, or a Docker setup, WireGenVPN provides an accessible solution for generating WireGuard configurations.

## Configuration Note

While WireGenVPN automates much of the configuration process, you may still need to manually copy and paste certain data, such as private and pre-shared keys, into your OpenWRT router's configuration. However, this process is significantly simplified and can be completed quickly.

## Example Use Case

With WireGenVPN, you can set up a fully configured OpenWRT server with 10 or more client peers in less than 20 minutes. The generated configuration files can be saved for later use, shared as QR codes, or stored in the cloud for future reference.

WireGenVPN is a powerful tool for streamlining the deployment of WireGuard VPNs and is not limited to OpenWRT. It's a versatile solution that simplifies WireGuard configuration for anyone with access to a Python-capable computer.

Feel free to contribute to the project or reach out if you have any questions or need assistance.

**Note**: Be sure to consult the documentation and any updates in the repository for the most current information and usage guidelines.

Happy VPN setup with WireGenVPN! 🚀
