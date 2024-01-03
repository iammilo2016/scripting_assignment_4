import socket
import re
import os
 
def prepend_to_file(filename, data):
    # Check if the file exists and read its content
    if os.path.exists(filename): # If the file exists
        with open(filename, 'r') as file: # Open the file in read mode
            old_data = file.read() 
    else:
        old_data = ''
 
    # Write new data followed by old data
    with open(filename, 'w') as file:
        file.write(data)  # Write new data
        file.write(old_data) # Write old data
 
def receive_data(conn): # Receive data from the client
    data = b'' # Initialize the data to be empty
    while True: # Keep receiving data until it's empty
        packet = conn.recv(1024) # Receive 1024 bytes at a time
        if not packet: # If the data is empty, stop receiving
            break
        data += packet
    return data.decode() 
 
def display_login_message(data):
    match = re.search(r'(\w+) logged in on (\d{8} \d{2}:\d{2})', data) # Search for the login message
    if match: # If the login message is found
        user, login_time = match.groups() # Get the user and login time
        print(f"[{user}] login on {login_time}; Login information received!")       
    else:
        print("No login information found in the data.")
 
    # Now, analyze the disk usage
    lines = data.split('\n') # Split the data into lines
    for line in lines: # Iterate over the lines
        if '/dev/' in line and not '/dev/sr0' in line: # If the line contains a device
            parts = line.split() # Split the line into parts
            if len(parts) > 5:  
                filesystem, size, used, avail, use_percent, mounted_on = parts[:6]  # Get the relevant parts
                use_percent = int(use_percent.strip('%'))
                if use_percent > 60:
                    print(f"Warning: Disk usage over 60% on filesystem {filesystem} (Mounted on {mounted_on}, {use_percent}% used)")
def receive_file(filename, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Create a socket object
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow the socket to be reused immediately after it's closed
        s.bind(('', port)) # Bind to the port
        s.listen()
        while True:  # Keep listening for new connections
            print("Waiting for a connection...")
            conn, addr = s.accept() # Accept a connection
            with conn: 
                print(f"Connection from {addr} established.")
                data = receive_data(conn)
                prepend_to_file(filename, data)
                print(f"Data prepended to {filename}.")
                display_login_message(data)
 
def main():
    receive_file('received_sysadmin_report.txt', 8080)  # Use the same port as in Client.py
 
if __name__ == "__main__":
    main()