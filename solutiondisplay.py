import os  # Import the 'os' module to work with the file system.
from timeit import default_timer as timer  # Import 'timer' for measuring execution time.
import re  # Import the 're' module for regular expressions.
import tkinter as tk  # Import the 'tkinter' module for GUI functionality.

from readfile import read_file  # Import the 'read_file' function from the 'readfile.py' module.
from constraints import solve  # Import the 'solve' function from the 'constraints.py' module.


# Natural sort helper function
def natural_sort_key(s):
    """
    Helper function to generate a natural sorting key (i.e., handles numeric ordering in filenames).
    """
    return [int(text) if text.isdigit() else text.lower() for text in
            re.split('([0-9]+)', s)]  # Split strings into text and numeric parts for natural sorting.


# Function to write solutions to solutions.txt
def write_solution_to_file(solution_text):
    solutions_file = 'solutions.txt'  # Define the output file for solutions.

    # Title to be added at the top of the file.
    title = "Exam Timetable Solutions\n"
    separator = "――――――――――――――――――――――――\n"  # Define a separator line.

    # Check if the file exists, if not, create it and write the title.
    if not os.path.exists(solutions_file):  # Check if the file does not exist.
        with open(solutions_file, 'w', encoding='utf-8') as f:  # Open the file in write mode.
            f.write(title)  # Write the title at the top.
            f.write(separator)  # Add a separator line after the title.
            f.write(solution_text)  # Write the actual solution text.
    else:  # If the file exists.
        with open(solutions_file, 'a', encoding='utf-8') as f:  # Open the file in append mode.
            f.write(separator)  # Add a separator line to distinguish new entries.
            f.write(solution_text)  # Write the solution text.


# Function to display constraint details in a new window.
def on_display_constraint_details():
    # Create a new window for displaying constraint details.
    constraint_window = tk.Toplevel()  # Create a new top-level window.
    constraint_window.title("Constraint Details")  # Set the title of the window.

    # Set the size of the window (larger than the default messagebox).
    constraint_window.geometry("500x400")  # Set the window dimensions (width x height).

    # Add a title label for the window.
    title_label = tk.Label(constraint_window, text="Constraint Details",
                           font=("Helvetica", 14, "bold"))  # Create a bold title label.
    title_label.pack(pady=10)  # Add padding to the label.

    # Add a label with the constraint details text.
    constraint_details = """
    1. Each exam must be timetabled in exactly one room and exactly one slot.\n
    2. There can be, at most, one exam timetabled in a room within a specific 
       slot.\n
    3. The number of students taking an exam cannot exceed the capacity of 
       the room where the exam takes place.\n 
    4. A student cannot take exams in consecutive time slots.\n
    5. Each room in a given time slot is assigned an invigilator, and the same
       invigilator is not assigned to multiple rooms in the same time slot.\n
    6. A student can take at most two exams in a day.\n
    7. An invigilator can supervise at most 2 exams.\n
    8. An invigilator must have at least one time slot gap between two exams they supervise.\n
    """
    label = tk.Label(constraint_window, text=constraint_details, justify=tk.LEFT,
                     font=("Helvetica", 8))  # Create a label for the details.
    label.pack(padx=20, pady=20)  # Add padding to the label.


# Function to display solutions for all instances in the specified format.
def display_all_solutions(instances_dir):
    start = timer()  # Start the timer to measure elapsed time.

    # Get a list of all text files in the instances directory.
    file_list = [f for f in os.listdir(instances_dir) if f.endswith('.txt')]  # Filter for files ending with '.txt'.

    # Sort the file list using natural sorting.
    sorted_file_list = sorted(file_list, key=natural_sort_key)

    # Loop through each file in the sorted list.
    for test_file in sorted_file_list:
        test_file_path = instances_dir / test_file  # Get the full path of the file.
        if test_file_path.is_file():  # Check if the path is a valid file.
            try:
                # Read and parse the file into an instance object.
                instance = read_file(str(test_file_path))
                print(f"{test_file}: ", end="")  # Print the filename.

                # Call the solve function to get the solution.
                result = solve(instance)
                print(result)  # Print the result returned by solve.

                # Write the result to solutions.txt.
                solution_text = f"{test_file}: {result}\n"
                write_solution_to_file(solution_text)

            except Exception as e:  # Catch and handle any exceptions during processing.
                print(f"Failed to process {test_file}: {e}")

    end = timer()  # End the timer.
    # Print the elapsed time in milliseconds.
    print('\nElapsed time:', int((end - start) * 1000), 'milliseconds')


# Function to display a solution for a selected instance.
def display_solution_for_selected_instance(instances_dir, file_var):
    selected_instance = file_var.get()  # Get the selected filename from the tkinter variable.
    test_file_path = instances_dir / selected_instance  # Get the full path of the selected file.

    if test_file_path.is_file():  # Check if the path is a valid file.
        try:
            # Read and parse the file into an instance object.
            instance = read_file(str(test_file_path))
            print(f"{selected_instance}: ", end="")  # Print the filename.

            start = timer()  # Start the timer.
            # Call the solve function to get the solution.
            result = solve(instance)
            end = timer()  # End the timer.

            print(result)  # Print the result returned by solve.

            # Calculate and display elapsed time.
            elapsed_time = int((end - start) * 1000)  # Convert elapsed time to milliseconds.
            print(f"Elapsed time: {elapsed_time} milliseconds")

        except Exception as e:  # Catch and handle any exceptions during processing.
            print(f"Failed to process {selected_instance}: {e}")
