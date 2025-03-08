
# Command & Control Framework

This repository contains a Command and Control (C2) implementation written in Python, consisting of a server and client component for remote system administration and management.

## Overview

This C2 framework establishes a TCP socket connection between a server and client, allowing the server operator to execute various commands on the client machine, gather system information, transfer files, capture screenshots, and enumerate running services. The framework supports Windows, Linux, and macOS operating systems.

## Components

### Server (command_control_server.py)

The server component:
- Opens a TCP socket on port 7777, listening for incoming connections
- Displays a banner using pyfiglet upon startup
- Handles user input through a menu-driven interface
- Displays geolocation information about connected clients
- Implements various remote administration capabilities

### Client (command_control_client.py)

The client component:
- Connects to a specified server IP (default: 192.168.0.109) on port 7777
- Gathers and transmits system information including:
  - Geographic location (using ipinfo.io)
  - Operating system details
  - User privileges
- Executes commands received from the server
- Supports file transfers, screenshot capture, and service enumeration

## Features

1. **Remote Command Execution**: Execute shell commands on the client system
2. **System Information Gathering**: Collect detailed system information based on the client's OS
3. **File Operations**:
   - Download files from the client
   - Upload files to the client
4. **Screenshot Capture**: Take screenshots of the client's display
5. **Service Enumeration**: List running services on the client system
6. **Directory Navigation**: Navigate the client's file system with CD commands
7. **Cross-platform Support**: Works on Windows, Linux, and macOS

## Requirements

### Server Dependencies
```
socket
os
sys
time
threading
pyfiglet
colorama
cryptography
termcolor
signal
shutil
platform
datetime
subprocess
```

### Client Dependencies
```
subprocess
socket
sys
time
os
platform
threading
colorama
pyautogui
requests
json
psutil
```

## Usage

1. **Starting the Server**:
   ```
   python command_control_server.py
   ```
   The server will listen on port 7777 for incoming connections.

2. **Running the Client**:
   ```
   python command_control_client.py
   ```
   By default, the client attempts to connect to 192.168.0.109:7777. Edit the `server_ip` variable in the client script to change this.

3. **Server Menu Options**:
   - **A**: Execute shell commands on the client
   - **B**: Gather system information
   - **C**: Download a file from the client
   - **D**: Upload a file to the client
   - **E**: Capture a screenshot from the client
   - **F**: Enumerate running services on the client
   - **exit/quit**: Close the connection and terminate the server

## Security Notes

- This tool includes functionality that could be misused. Use it only on systems you own or have explicit permission to test.
- The server binds to 0.0.0.0, making it accessible from any network interface.
- Communication is not encrypted (except for the unused Fernet implementation).
- A hardcoded encryption key is present in the code but not used.
- Commands are executed with shell=True, which poses security risks if input isn't properly sanitized.

## Limitations

- Error handling could be improved in several areas
- Some features have OS-specific implementations that may not work as expected
- Screenshot functionality on Linux and macOS has file handling issues (using 'r' mode instead of 'rb')
- File transfer logic has inconsistencies between upload and download functions

## Legal Disclaimer

This tool is provided for educational purposes only. Users are responsible for complying with all applicable laws and regulations when using this software.