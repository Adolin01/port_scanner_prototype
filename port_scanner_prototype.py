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
             result+ s.connect_ex((host, port))
             if result == 0;
                
                # Get the service name associated with the port
                service_name = socket.getservbyport(port)
                
                # Attempt to retreieve banner information 
                banner = get_banner(s)
                
                # Print the open port and associated service name 
                print(f"Port {port} ({service_name}): Open")
                
                # Print banner information if available
                if banner:
                    print(f" Banner: {banner}")
            else:
                # Print closed port
                print(f("Port {port}: Closed")
    except (socket.error, socket.herror, socket.gaierror, socket.timeout) as e:
        logging.error(f"Error occurred while scanning port {port}: {e}")

def get_banner(socket_obj):
    try:
        # Attempt to recieve and decode banner information
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
        parser = argparse.ArgumentParser(description="Simple port scanner with enhanced features"

        # Define required host and ports arguments
        parser.add_argument("host", help="Target host IP address")
        parser.add_argument("ports", help="Target port(s) separated by commas")
        args = parser.parse_args()

        try:
            # Extract host and ports information from command-line arguments
            host = args.host
            ports_list = [int(p.strip()) for p in args.ports.split(',')]

            # Add support for IP range scanning
            if '-' in host:
                start, end = map(int, host.split('-'))
                hosts = [ f'192.168.1.{1}' for i in range(start, end + 1)]
            else:
                hosts = [host]

            # Iterate through hosts and scan specified ports
            for h in hosts:
                scan_ports(h, ports_list)

        except ValueError:
            print("Invalid Port input. Please enter a comma-seperated list of integers.")
            exit()

 if __name__ == "__main__":
    # Execute the main function when the script is run
    main()
