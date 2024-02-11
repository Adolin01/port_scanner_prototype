#!/usr/bin/env python3

import socket
import concurrent.futures
import argparse
import logging

# Setup logging
logging.basicConfig(filename='port_scanner.log', level=logging.INFO)

def scan_port(host, port):
    try:
        # Create a socket object and set a timeout
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
             
            # Try to connect to the specified host and port
            result = s.connect_ex((host, port))
            if result == 0:
                # Get the service name associated with the port
                service_name = socket.getservbyport(port)
                
                # Attempt to retrieve banner information 
                banner = get_banner(s)
                
                # Print the open port and associated service name 
                print(f"Port {port} ({service_name}): Open")
                
                # Print banner information if available
                if banner:
                    print(f" Banner: {banner}")
            else:
                # Print closed port
                print(f"Port {port}: Closed")
    except (socket.error, socket.herror, socket.gaierror, socket.timeout) as e:
        logging.error(f"Error occurred while scanning port {port}: {e}")

def get_banner(socket_obj):
    try:
        # Attempt to receive and decode banner information
        banner = socket_obj.recv(1024).decode('utf-8').strip()
        return banner
    except socket.error:
        return None

def scan_ports(host, ports_list):
    print("\nScanning ports...\n")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use multithreading to scan ports concurrently
        executor.map(lambda port: scan_port(host, port), ports_list)
    print("\nScan completed.")

def main():
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description="Simple port scanner with enhanced features")

    # Define required host and ports arguments
    parser.add_argument("host", help="Target host IP address")
    parser.add_argument("ports", help="Target port(s) separated by commas or a range (e.g., 1-1000)")
    args = parser.parse_args()

    try:
        # Extract host and ports information from command-line arguments
        host = args.host

        # Parse the ports argument
        ports_list = parse_ports_argument(args.ports)

        # Iterate through hosts and scan specified ports
        scan_ports(host, ports_list)

    except ValueError as e:
        print(f"Error: {e}")
        exit()

def parse_ports_argument(ports_argument):
    # Parse the ports argument and return a list of integers
    if '-' in ports_argument:
        start, end = map(int, ports_argument.split('-'))
        return list(range(start, end + 1))
    else:
        return [int(p.strip()) for p in ports_argument.split(',')]

if __name__ == "__main__":
    # Execute the main function when the script is run
    main()

