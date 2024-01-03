import subprocess
import os
import datetime

def check_disk_usage():
    try:
        result = subprocess.run(['df', '-h'], capture_output=True, text=True)   # Run the command and capture the output
        return result.stdout # Return the output of the command
    except subprocess.SubprocessError as e:
        return f"Error in disk usage check: {e}"

def get_login_info():
    try:
        user = os.getlogin() # Get the username of the user who ran the script
        login_time = datetime.datetime.now().strftime("%d%m%Y %H:%M") # Get the current date and time
        return f"{user} logged in on {login_time}"
    except Exception as e:
        return f"Error getting login info: {e}"

def get_filename():
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.realpath(__file__))
 
        base_filename = 'sysadmin_report'
        extension = '.txt'
        date_str = datetime.datetime.now().strftime("%d%m%Y")
        counter = 1
 
        # Construct the file path with the directory
        filename = os.path.join(script_dir, f"{base_filename}_{date_str}_{counter}{extension}")
 
        while os.path.exists(filename):
            counter += 1
            filename = os.path.join(script_dir, f"{base_filename}_{date_str}_{counter}{extension}")
 
        return filename
    except Exception as e:
        return f"Error generating filename: {e}"

def main():
    try:
        filename = get_filename() # Get the filename
        with open(filename, 'w') as file: # Open the file in write mode
            file.write(get_login_info() + '\n') # Write the login information
            file.write(check_disk_usage())  # Write the disk usage information
    except IOError as e:
        print(f"File operation error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
