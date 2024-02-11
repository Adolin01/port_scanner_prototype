# Port Scanner Prototype

## Overview

This is a simple port-scanning prototype script created for educational purposes. The script is designed to help students learn about network security concepts, socket programming, and ethical hacking techniques.

**Important Note:** The use of this script involves responsibilities and considerations outlined below. Please read this README carefully before using the script.

## Disclaimer

**Use at Your Own Risk:** This script is provided as an educational resource and is not intended for any malicious or unauthorized activities. The author is not responsible for any misuse or damage caused by the use of this script.

**Legal and Ethical Considerations:** Before using this script, ensure that you have explicit permission to scan any system or network. Unauthorized scanning is unethical and may be illegal. Always comply with the legal and ethical guidelines related to network scanning in your jurisdiction.

## Educational Purpose

This script is intended for educational purposes only. It aims to help students:

- Understand how port scanning works.
- Learn about socket programming in Python.
- Explore basic concepts of network security.
- Practice ethical hacking techniques in a controlled and legal environment.

## Usage Guidelines

To use this script responsibly:

1. **Permission:** Obtain explicit permission before scanning any system or network. Unauthorized scanning is against the law and can result in severe consequences.

2. **Legal Compliance:** Understand and comply with the legal and ethical guidelines related to network scanning in your jurisdiction.

3. **Responsible Use:** Use the script only in a controlled and legal environment. Avoid activities that could be perceived as aggressive or malicious.


Run the script with the target host and ports: 

    python3 port_scanner_prototype.py <target_host> <port, port>

    python3 port_scanner_prototype.py <target_host> <port-port>


## Getting Started 

Follow these steps to get started with the script: 

1. Clone the repository to your local machine: 

    git clone https://github.com/Adolin01/port_scanner_prototype.git 

2. Navigate to the project directory:

    cd port_scanner_prototype 

3. Run the script with the target host and ports:

    python3 port_scanner_prototype.py <target_host> <port, port> 

# Examples: 
# To scan individual ports, specify them separated by commas. For example:

    python3 port_scanner_prototype.py 10.0.2.15 80,443,8080 

# To scan a range of ports, use a hyphen between the start and end ports. For example: 

    python3 port_scanner_prototype.py 10.0.2.15 8000-8010

## Contributing

Contributions are welcome! If you have suggestions, improvements, or bug fixes, please open an issue or submit a pull request. However, please adhere to the educational and responsible use principles outlined in this README.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it in accordance with the terms of the license.

---

**Note:** By using this script, you acknowledge and accept the responsibilities outlined in the disclaimer and usage guidelines. Always prioritize legal and ethical considerations when using and sharing educational resources related to security.

