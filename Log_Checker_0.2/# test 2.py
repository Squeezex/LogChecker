# test 2 (trying to make put both files in a separate folders)
import os
import shutil
from colorama import Fore, Style, init

init()

# Directory containing the log files
log_dir = r'D:/Logs'  # Put your path to folder with logs instead of 'D:/Your_Folder_With_Logs'
broken_logs_dir = os.path.join(log_dir, 'broken_logs')
broken_logs_with_monitor_dir = os.path.join(broken_logs_dir, 'broken_logs_with_monitor')

# List to store the names of all logs moved to 'broken_logs'
moved_logs = []

# List to track files that could not be processed due to errors
error_logs = []

# Track if both 'project' and 'monitor' logs are in the same folder
project_log_found = False
monitor_log_found = False

# Walk through the directory to search for .log files, but exclude the 'broken_logs' folder
for root, dirs, files in os.walk(log_dir):
    dirs[:] = [d for d in dirs if d != 'broken_logs']  # Exclude the 'broken_logs' folder from the search

    project_log_found = False  # Reset flags for each directory
    monitor_log_found = False

    for file in files:
        if file.endswith(".log"):
            file_path = os.path.join(root, file)
            print(f"Checking file: {file_path}")

            try:  # Open each log file and check its content
                with open(file_path, 'r') as f:
                    content = f.read()

                    # Case 1: For log files with 'project' in the name
                    if 'project' in file.lower():
                        project_log_found = True  # Set flag if 'project' file found
                        # If the file does NOT contain both "LogExit: Exiting" and "Log file closed"
                        if not ("LogExit: Exiting" in content and "Log file closed" in content):
                            # Create 'broken_logs' folder if it doesn't exist
                            if not os.path.exists(broken_logs_dir):
                                os.makedirs(broken_logs_dir)
                                print(f"Created directory: {broken_logs_dir}")

                            # Move the file to the appropriate folder (check if both project and monitor are found)
                            if project_log_found and monitor_log_found:
                                # Create the 'broken_logs_with_monitor' folder if it doesn't exist
                                if not os.path.exists(broken_logs_with_monitor_dir):
                                    os.makedirs(broken_logs_with_monitor_dir)
                                    print(f"Created directory: {broken_logs_with_monitor_dir}")

                                destination_path = os.path.join(broken_logs_with_monitor_dir, file)
                            else:
                                destination_path = os.path.join(broken_logs_dir, file)

                            shutil.move(file_path, destination_path)
                            moved_logs.append(file)  # Add the moved file name to the list
                            print(f"Moved broken 'project' log: {file_path} to {destination_path}")

                    # Case 2: For log files with 'monitor' in the name
                    elif 'monitor' in file.lower():
                        monitor_log_found = True  # Set flag if 'monitor' file found
                        # If the file does NOT contain "Normal exit"
                        if "Normal exit" not in content:
                            # Create 'broken_logs' folder if it doesn't exist
                            if not os.path.exists(broken_logs_dir):
                                os.makedirs(broken_logs_dir)
                                print(f"Created directory: {broken_logs_dir}")

                            # Move the file to the appropriate folder (check if both project and monitor are found)
                            if project_log_found and monitor_log_found:
                                # Create the 'broken_logs_with_monitor' folder if it doesn't exist
                                if not os.path.exists(broken_logs_with_monitor_dir):
                                    os.makedirs(broken_logs_with_monitor_dir)
                                    print(f"Created directory: {broken_logs_with_monitor_dir}")

                                destination_path = os.path.join(broken_logs_with_monitor_dir, file)
                            else:
                                destination_path = os.path.join(broken_logs_dir, file)

                            shutil.move(file_path, destination_path)
                            moved_logs.append(file)  # Add the moved file name to the list
                            print(f"Moved broken 'monitor' log: {file_path} to {destination_path}")

            except Exception as e:
                error_logs.append(file)  # Add the file to the error log list
                print(f"Error reading file {file_path}: {e}")

# Green text for correct files
if moved_logs:
    print(f"\nAll 'broken' logs have been moved to {broken_logs_dir}:")
    for log in moved_logs:
        print(f"- {log}")
else:
    print(f"{Fore.GREEN}All files above are correct and contain 'LogExit: Exiting' 'Log file closed' or 'Normal exit'.{Style.RESET_ALL}")

# Red text for broken files
if error_logs:
    print(f"{Fore.RED}\nThe following files encountered errors during processing:{Style.RESET_ALL}")
    for log in error_logs:
        print(f"- {log}")
