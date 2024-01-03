import socket
import glob
import os

def find_latest_report(pattern):
    try:
        list_of_files = glob.glob(pattern)  # List all files matching the pattern
        if not list_of_files:  # No files found
            return None
        latest_file = max(list_of_files, key=os.path.getctime)  # Find the latest file
        return latest_file
    except Exception as e:
        print(f"Error finding the latest report: {e}")
        return None

def send_file_to_server(filename, server_ip, server_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))  # Connect to the server
            with open(filename, 'rb') as file:
                s.sendfile(file)
    except socket.error as e:
        print(f"Socket error: {e}")
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    report_pattern = 'sysadmin_report*.txt'  # Pattern to match report files
    latest_report = find_latest_report(report_pattern)  # Find the latest report file
    if latest_report:
        send_file_to_server(latest_report, "10.10.10.1", 8080)  # Replace SERVER_IP with the actual IP of the server
    else:
        print("No report file found.")

if __name__ == "__main__":
    main()