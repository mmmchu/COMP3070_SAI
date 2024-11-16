import os
from timeit import default_timer as timer
import re
import tkinter as tk

from readfile import read_file  # Import read_file from readfile.py
from constraints import solve  # Import solve from constraints.py


# Natural sort helper function
def natural_sort_key(s):
    """
    Helper function to generate a natural sorting key (i.e., handles numeric ordering in filenames).
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


# Function to write solutions to solutions.txt
def write_solution_to_file(solution_text):
    solutions_file = 'solutions.txt'

    # Title to be added at the top of the file
    title = "Exam Timetable Solutions\n"
    separator = "――――――――――――――――――――――――\n"

    # Check if the file exists, if not, create it and write the title
    if not os.path.exists(solutions_file):
        with open(solutions_file, 'w', encoding='utf-8') as f:
            f.write(title)  # Write the title at the top
            f.write(separator)  # Add a separator line after the title
            f.write(solution_text)  # Write the actual solution text
    else:
        with open(solutions_file, 'a', encoding='utf-8') as f:
            f.write(separator)  # Add a separator line to distinguish new entries
            f.write(solution_text)  # Write the solution text


# Display solutions for all instances in the specified format
def on_display_constraint_details():
    # Create a new window for displaying constraint details
    constraint_window = tk.Toplevel()  # Toplevel creates a new window
    constraint_window.title("Constraint Details")

    # Set the size of the window (larger than the default messagebox)
    constraint_window.geometry("500x400")  # You can adjust this size as needed

    # Add a title label for the window
    title_label = tk.Label(constraint_window, text="Constraint Details", font=("Helvetica", 14, "bold"))
    title_label.pack(pady=10)  # Padding to separate the title from the content
    # Add a label with the constraint details text
    constraint_details = """
    1. Each exam must be timetabled in exactly one room and exactly one slot.\n
    2.There can be, at most, one exam timetabled in a room within a specific 
       slot.\n
    3.The number of students taking an exam cannot exceed the capacity of 
       the room where the exam takes place.\n 
    4.A student cannot take exams in consecutive time slots. \n
    5.Each room in a given time slot is assigned an invigilator,and that the same
       invigilator is not assigned to multiple rooms in the same time slot.\n
    6.A student can take at most two exams in a day.\n
    7.An invigilator can supervise at most 2 exams\n
    """
    label = tk.Label(constraint_window, text=constraint_details, justify=tk.LEFT, font=("Helvetica", 8))
    label.pack(padx=20, pady=20)


# Display solutions for all instances in the specified format
def display_all_solutions(instances_dir):
    start = timer()
    file_list = [f for f in os.listdir(instances_dir) if f.endswith('.txt')]
    sorted_file_list = sorted(file_list, key=natural_sort_key)

    for test_file in sorted_file_list:
        test_file_path = instances_dir / test_file
        if test_file_path.is_file():
            try:
                instance = read_file(str(test_file_path))
                print(f"{test_file}: ", end="")

                # Call solve() once per file and store the result
                result = solve(instance)
                print(result)  # Print the result returned by solve()

                # Write the result to solutions.txt
                solution_text = f"{test_file}: {result}\n"
                write_solution_to_file(solution_text)

            except Exception as e:
                print(f"Failed to process {test_file}: {e}")

    end = timer()
    print('\nElapsed time:', int((end - start) * 1000), 'milliseconds')


# Display solution for a selected instance in the specified format
def display_solution_for_selected_instance(instances_dir, file_var):
    selected_instance = file_var.get()
    test_file_path = instances_dir / selected_instance

    if test_file_path.is_file():
        try:
            instance = read_file(str(test_file_path))
            print(f"{selected_instance}: ", end="")

            start = timer()  # Start timer
            # Call solve() once per file and store the result
            result = solve(instance)
            end = timer()  # End timer

            print(result)  # Print the result returned by solve()

            # Calculate and display elapsed time
            elapsed_time = int((end - start) * 1000)  # Elapsed time in milliseconds
            print(f"Elapsed time: {elapsed_time} milliseconds")

        except Exception as e:
            print(f"Failed to process {selected_instance}: {e}")
