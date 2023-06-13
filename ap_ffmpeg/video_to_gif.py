import re
import anchorpoint as ap
import apsync as aps
import sys
import subprocess
import os
import random
import string
import mimetypes
import platform
import glob
import time

import ffmpeg_helper
import subprocess


ctx = ap.get_context()


def run_batch_script_with_file(file_path, batch_script_path):
    try:
        # Run the batch script with the file as an argument and capture output
        result = subprocess.run([batch_script_path, file_path], capture_output=True)
        if result.returncode == 0:
            print("Batch script executed successfully.")
        else:
            print("Batch script returned a non-zero exit status:", result.returncode)
            print("Error output:\n", result.stderr.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error executing batch script: {e}")

# Usage example


def run_batch_script_with_file(file_path, batch_script_path):
    # Execute the batch file without opening a command prompt window
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.Popen([batch_script_path, file_path], startupinfo=startup_info)



file_path = ctx.path
batch_script_path = "C:/Program Files/SendTo_FFmpeg/anchorpoint_togif.bat"
run_batch_script_with_file(file_path, batch_script_path)

# Define the directory where the files are located
directory = file_path

# Define the pattern to match files containing "palette" in the name
pattern = "*palette*"

# Get a list of file paths matching the pattern
file_paths = glob.glob(os.path.join(directory, pattern))

# Delete each file
for file_path in file_paths:
    try:
        os.remove(file_path)
        print(f"File {file_path} deleted successfully.")
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")