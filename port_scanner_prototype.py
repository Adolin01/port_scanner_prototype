#!/usr/bin/env python3

import socket
import concurrent.futures
import argparse
import logging
from tqdm import tqdm  # Import tqdm for a progress bar
from prettytable import PrettyTable  # Import PrettyTable for tabular output

# Setup logging configuration, specifying a log file and setting the logging level to INFO
logging.basicConfig(filename='port_scanner.log', level=logging.INFO)

# Function to scan an individual port on a target host
def scan_port(host, port, progress_bar, timeout):
    try:
        # Create a socket object and set the timeout based on the argument
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            
            # Try to connect to the specified host and port
            result = s.connect_ex((host, port))

            # Update the progress bar with the current port being scanned
            progress_bar.set_postfix(port=port)
            progress_bar.update(1)

            # If the connection was successful (result code is 0)
            if result == 0:
                # Get the service name associated with the port
                service_name = socket.getservbyport(port)

                # Attempt to retrieve banner information from the connected socket
                banner = get_banner(s)

                # Return a dictionary with details of the open port
                return {'port': port, 'service_name': service_name, 'banner': banner}
            else:
                # Return None to indicate that the port is closed
                return None
    except (socket.error, socket.herror, socket.gaierror, socket.timeout) as e:
        # Log any errors that occur during the scanning process
        logging.error(f"Error occurred while scanning port {port}: {e}")

        # Return None to indicate an error occurred
        return None

# Function to retrieve banner information from a connected socket
def get_banner(socket_obj):
    try:
        # Attempt to receive and decode banner information (up to 1024 bytes)
        banner = socket_obj.recv(1024).decode('utf-8').strip()

        # Return the decoded banner information
        return banner
    except socket.error:
        # Return None if an error occurs during banner retrieval
        return None

# Function to scan a range of ports on a target host using multithreading
def scan_ports(host, ports_list, timeout):
    # Initialize an empty list to store open ports
    open_ports = []

    # Print a message indicating that port scanning is starting
    print("\nScanning ports...\n")

    try:
        # Create a tqdm progress bar for the scanning process
        with tqdm(total=len(ports_list), desc="Scan Progress", unit="ports", dynamic_ncols=True) as progress_bar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Create a dictionary to store futures (results of concurrent tasks)
                futures = {executor.submit(scan_port, host, port, progress_bar, timeout): port for port in ports_list}

                # Iterate through completed futures
                for future in concurrent.futures.as_completed(futures):
                    # Get the result (open port details) from the completed future
                    result = future.result()

                    # If an open port is found, add it to the list of open ports
                    if result:
                        open_ports.append(result)

    except Exception as e:
        print(f"Error during port scanning {e}")

    finally:
        # Explicity shutdown the ThreadPoolExecutor to ensure all threads are completed
        executor.shutdown(wait=True)

    # Return the list of open ports
    return open_ports

# Main function to handle command-line arguments and initiate the scanning process
def main():
    # Set up the command-line argument parser with a description
    parser = argparse.ArgumentParser(description="Simple port scanner with enhanced features")

    # Define required command-line arguments for target host, ports, and timeout
    parser.add_argument("host", help="Target host IP address")
    parser.add_argument("ports", help="Target port(s) separated by commas or a range (e.g., 1-1000)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout duration for socket connections (default: 1.0)")

    # Parse the command-line arguments
    args = parser.parse_args()

    try:
        # Extract host and ports information from command-line arguments
        host = args.host

        # Parse the ports argument into a list of integers
        ports_list = parse_ports_argument(args.ports)

        # Call the function to scan specified ports on the target host with the specified timeout
        open_ports = scan_ports(host, ports_list, args.timeout)

        # Check if any open ports were found
        if open_ports:
            # Create a PrettyTable for tabular output
            table = PrettyTable()
            table.field_names = ["Port", "Service Name", "Status", "Banner"]

            # Add rows to the table
            for result in open_ports:
                port = result['port']
                service_name = result['service_name']
                status = "Open"
                banner = result['banner'] if result['banner'] else "-"

                # Add a row to the table
                table.add_row([port, service_name, status, banner])

            # Print the table
            print("\nScan completed. Open ports found:")
            print(table)
        else:
            # Print a message if no open ports were found
            print("\nNo open ports found.")

    except ValueError as e:
        # Print an error message if there is an issue with the provided values
        print(f"Error: {e}")

        # Exit the program
        exit()

# Function to parse the ports argument into a list of integers
def parse_ports_argument(ports_argument):
    # Check if the argument contains a range (e.g., "1-1000")
    if '-' in ports_argument:
        # Split the range into start and end values and create a list of integers
        start, end = map(int, ports_argument.split('-'))
        return list(range(start, end + 1))
    else:
        # If no range is present, create a list of integers from comma-separated values
        return [int(p.strip()) for p in ports_argument.split(',')]

# Entry point: Execute the main function when the script is run
if __name__ == "__main__":
    main()

