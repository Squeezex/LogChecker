import os
import shutil
from colorama import Fore, Style, init

init()

# Directory containing the log files
log_dir = r'D:/Logs' #Put your path to folder with logs instead of 'D:/Your_Folder_With_Logs', for example 'D:/Master/Logs'
broken_logs_dir = os.path.join(log_dir, 'broken_logs')

# List to store the names of all logs moved to 'broken_logs'
moved_logs = []

# List to track files that could not be processed due to errors
error_logs = []

# Walk through the directory to search for .log files, but exclude the 'broken_logs' folder
for root, dirs, files in os.walk(log_dir):
    dirs[:] = [d for d in dirs if d != 'broken_logs'] # Exclude the 'broken_logs' folder from the search
    
    for file in files:
        if file.endswith(".log"):
            file_path = os.path.join(root, file)
            print(f"Checking file: {file_path}")

            try: # Open each log file and check its content
                with open(file_path, 'r') as f:
                    content = f.read()

                    if not ("LogExit: Exiting" in content and "Log file closed" in content): # If the log file does NOT contain both "LogExit: Exiting" and "Log file closed"
                        if not os.path.exists(broken_logs_dir): # Create the 'broken_logs' directory if it doesn't exist
                            os.makedirs(broken_logs_dir)
                            print(f"Created directory: {broken_logs_dir}")
                        
                        destination_path = os.path.join(broken_logs_dir, file) # Move the file to the broken_logs folder
                        shutil.move(file_path, destination_path)
                        moved_logs.append(file) # Add the moved file name to the list
                        print(f"Moved broken log: {file_path} to {destination_path}")
            except Exception as e:
                error_logs.append(file) # Add the file to the error log list
                print(f"Error reading file {file_path}: {e}")

# Green text for correct files
if moved_logs:
    print(f"\nAll 'broken' logs have been moved to {broken_logs_dir}:")
    for log in moved_logs:
        print(f"- {log}")
else:
    print(f"{Fore.GREEN}All files above are correct and contain 'LogExit: Exiting' 'Log file closed.{Style.RESET_ALL}")  

# Red text for broken files
if error_logs:
    print(f"{Fore.RED}\nThe following files are broken and don't contain 'LogExit: Exiting' and 'Log file closed', check the 'broken_logs' folder:{Style.RESET_ALL}")
    for log in error_logs:
        print(f"- {log}")