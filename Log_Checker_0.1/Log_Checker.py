import os
import shutil

log_dir = 'D:\Logs\Logs' # Directory containing the log files #P.S if there is an error change symbols '\' to '/'
broken_logs_dir = os.path.join(log_dir, 'broken_logs')  # Directory to store the 'broken' logs 

# Create the 'broken_logs' directory folder if it doesn't exist
if not os.path.exists(broken_logs_dir):
    os.makedirs(broken_logs_dir)
    print(f"Created directory: {broken_logs_dir}")

# List to store the names of all logs moved to 'broken_logs'
moved_logs = []

# Walk through the directory to search for .log files
for root, dirs, files in os.walk(log_dir):
    for file in files:
        if file.endswith(".log"):
            file_path = os.path.join(root, file)
            print(f"Checking file: {file_path}")

            # Open each log file and check its content
            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                    # If the log file does NOT contain both "LogExit: Exiting" and "Log file closed"
                    if not ("LogExit: Exiting" in content and "Log file closed" in content):
                        # Move the file to the broken_logs folder
                        destination_path = os.path.join(broken_logs_dir, file)
                        shutil.move(file_path, destination_path)
                        moved_logs.append(file)  # Add the moved file name to the list
                        print(f"Moved broken log: {file_path} to {destination_path}")
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

# Debug print after moving logs
if moved_logs:
    print(f"\nAll 'broken' logs have been moved to {broken_logs_dir}:")
    for log in moved_logs:
        print(f"- {log}")
else:
    print(f"No 'broken' logs found. All logs contain both 'LogExit: Exiting' and 'Log file closed', check the 'broken_logs' folder.")