import os
import shutil
from colorama import Fore, Style, init

init()

# Directory containing the log files
log_dir = r'D:/Your_Folder_With_Logs'  # Put your path to folder with logs instead of 'D:/Your_Folder_With_Logs'
broken_logs_dir = os.path.join(log_dir, 'broken_logs')

# Dictionary to hold the broken logs for each subfolder
broken_logs_per_subfolder = {}

# List to track files that could not be processed due to errors
error_logs = []

# Flag to check if there are any log files
has_logs = False

# Walk through the directory to search for .log files, but exclude the 'broken_logs' folder
for root, dirs, files in os.walk(log_dir):
    dirs[:] = [d for d in dirs if d != 'broken_logs']  # Exclude the 'broken_logs' folder from the search

    # Initialize tracking for the current subfolder
    relative_folder = os.path.relpath(root, log_dir)
    broken_logs_per_subfolder[relative_folder] = {'project': [], 'monitor': []}

    for file in files:
        if file.endswith(".log"):
            has_logs = True
            file_path = os.path.join(root, file)
            print(f"Checking file: {file_path}")

            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                    # Case 1: Check "project" logs
                    if 'project' in file.lower():
                        # If the log file does NOT contain both "LogExit: Exiting" and "Log file closed"
                        if not ("LogExit: Exiting" in content and "Log file closed" in content):
                            # Add to broken 'project' logs for this subfolder
                            broken_logs_per_subfolder[relative_folder]['project'].append(file_path)
                            print(f"Broken 'project' log: {file_path}")

                    # Case 2: Check "monitor" logs
                    elif 'monitor' in file.lower():
                        # If the log file does NOT contain "Normal exit"
                        if "Normal exit" not in content:
                            # Add to broken 'monitor' logs for this subfolder
                            broken_logs_per_subfolder[relative_folder]['monitor'].append(file_path)
                            print(f"Broken 'monitor' log: {file_path}")

            except Exception as e:
                error_logs.append(file)
                print(f"Error reading file {file_path}: {e}")

# Now copy the broken logs for each subfolder
logs_copied = False  # Flag to check if any logs were copied
for subfolder, logs in broken_logs_per_subfolder.items():
    project_logs = logs['project']
    monitor_logs = logs['monitor']

    if project_logs or monitor_logs:
        logs_copied = True  # Mark that some logs were copied
        # Create appropriate folder inside 'broken_logs'
        if project_logs and monitor_logs:
            # Both types of logs found, create 'broken_logs_with_monitor' folder
            destination_folder = os.path.join(broken_logs_dir, 'broken_logs_with_monitor', subfolder)
        else:
            # Only one type of log found, use the regular 'broken_logs' folder
            destination_folder = os.path.join(broken_logs_dir, subfolder)

        # Create the destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            print(f"{Fore.BLUE}Created Folder: {destination_folder}{Style.RESET_ALL}")

        # Copy 'project' logs (with red text)
        for log_path in project_logs:
            destination_path = os.path.join(destination_folder, os.path.basename(log_path))
            shutil.copy(log_path, destination_path)
            print(f"{Fore.RED}Copied broken 'project' log: {log_path} to {destination_path}{Style.RESET_ALL}")

        # Copy 'monitor' logs (with red text)
        for log_path in monitor_logs:
            destination_path = os.path.join(destination_folder, os.path.basename(log_path))
            shutil.copy(log_path, destination_path)
            print(f"{Fore.RED}Copied broken 'monitor' log: {log_path} to {destination_path}{Style.RESET_ALL}")

# Debug print for correctly processed files (green) if no logs were copied
if not logs_copied and has_logs:
    print(f"{Fore.GREEN}All files are correct, and contain 'LogExit: Exiting' 'Log file closed' for 'Project .logs' and 'Normal exit' for 'monitor .logs'.{Style.RESET_ALL}")

# Red text for broken files or errors
if error_logs:
    print(f"{Fore.RED}\nThe following files encountered errors during processing:{Style.RESET_ALL}")
    for log in error_logs:
        print(f"- {log}")

# Debug print if no .log files were found in your path
if not has_logs:
    print(f"{Fore.YELLOW}No '.log' files found in the directory: {log_dir}{Style.RESET_ALL}")