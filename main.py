from pathlib import Path
from timeit import default_timer as timer
from readfile import read_file  # Import read_file from readfile.py
from constraints import solve  # Import solve from constraints.py

# Start the timer
start = timer()

# Main code execution
if __name__ == "__main__":
    tests_dir = Path("C:/Users/mabel/PycharmProjects/SAI CW 1/test instances")  # Update this path
    instances_dir = tests_dir  # Since 'test instances' is the main folder now, no need for subdirectory

    # Iterate through files in the "test instances" directory
    for test_file in instances_dir.iterdir():
        if test_file.is_file() and test_file.name not in [".idea"]:  # Skip irrelevant files
            try:
                instance = read_file(str(test_file))
                print(f"{test_file.name}: ", end="")
                solve(instance)  # Call solve from constraints.py
            except Exception as e:
                print(f"Failed to process {test_file.name}: {e}")

# End the timer
end = timer()
print('\nElapsed time:', int((end - start) * 1000), 'milliseconds')
