from pathlib import Path
from timeit import default_timer as timer
from readfile import read_file  # Import read_file from readfile.py
from constraints import solve  # Import solve from constraints.py
import re
import os


# Natural sort helper function
def natural_sort_key(s):
    """
    Helper function to generate a natural sorting key (i.e., handles numeric ordering in filenames).
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


# Start the timer
start = timer()

# Main code execution
if __name__ == "__main__":
    tests_dir = Path("C:/Users/mabel/PycharmProjects/SAI CW 1/test instances")  # Update this path
    instances_dir = tests_dir  # Since 'test instances' is the main folder now, no need for subdirectory

    # List all files in the directory and filter for the desired .txt files
    file_list = [f for f in os.listdir(instances_dir) if f.endswith('.txt')]

    # Sort the file list in natural order
    sorted_file_list = sorted(file_list, key=natural_sort_key)

    # Iterate through the sorted files
    for test_file in sorted_file_list:
        test_file_path = instances_dir / test_file  # Get the full file path
        if test_file_path.is_file():  # Make sure it's a valid file
            try:
                instance = read_file(str(test_file_path))  # Read the instance from the file
                print(f"{test_file}: ", end="")
                solve(instance)  # Call solve from constraints.py
            except Exception as e:
                print(f"Failed to process {test_file}: {e}")

# End the timer
end = timer()
print('\nElapsed time:', int((end - start) * 1000), 'milliseconds')
