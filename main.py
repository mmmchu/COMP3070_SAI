# Import necessary libraries for GUI creation and file handling
import tkinter as tk  # Core library for GUI development in Python
from pathlib import Path  # For handling file system paths
import os  # To interact with the operating system
from tkinter import messagebox  # For displaying message boxes
from PIL import Image, ImageTk  # Import Pillow for image manipulation
import customtkinter as ctk  # Custom Tkinter module for enhanced widgets

# Import custom functions from the solution display module
from solutiondisplay import (
    display_all_solutions,  # Function to display solutions for all instances
    natural_sort_key,  # Utility for natural sorting of filenames
    display_solution_for_selected_instance,  # Function to display solution for a selected instance
    on_display_constraint_details  # Function to display details of constraints
)

# Main GUI setup
if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    root.title("Exam Scheduling Solver")  # Set the title of the window

    # Set the initial dimensions for the window
    window_width = 500
    window_height = 500
    root.geometry(f"{window_width}x{window_height}")  # Adjust the size of the window

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the position to place the window on the right side of the screen
    x_position = screen_width - window_width  # Position the window at the far right
    y_position = (screen_height - window_height) // 2  # Center the window vertically

    # Set the position of the window
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Set the background color of the main window to white
    root.config(bg="white")

    # Path to the directory containing the instances
    instances_dir = Path("C:/Users/mabel/PycharmProjects/SAI CW 1/test instances")

    # Define a StringVar to hold the selected file name globally
    file_var = tk.StringVar()

    # Function to display solutions for all instances
    def on_display_all_solutions():
        # Show a message box indicating that solutions are being loaded
        messagebox.showinfo("Loading", "Loading the solutions, please check the run terminal.")
        display_all_solutions(instances_dir)  # Call the function to display all solutions

    # Function to handle solution display for a selected instance
    def on_display_solution_for_selected_instance():
        # Get all .txt files in the directory and sort them
        file_list = [f for f in os.listdir(instances_dir) if f.endswith('.txt')]
        sorted_file_list = sorted(file_list, key=natural_sort_key)

        # Nested function to handle the selection of an instance
        def on_select():
            selected_instance = file_var.get()  # Get the selected file name
            if not selected_instance:  # Check if no file is selected
                tk.messagebox.showerror("Error", "No instance selected.")
                return
            display_solution_for_selected_instance(instances_dir, file_var)  # Display the selected solution

        # Hide the main menu and show the instance selection frame
        main_menu_frame.pack_forget()
        instance_window_frame.pack(fill="both", expand=True)

        # Clear existing widgets in the instance selection frame
        for widget in instance_window_frame.winfo_children():
            widget.destroy()

        # Add the logo to the top of the frame
        # noinspection PyTypeChecker
        labellogo = tk.Label(instance_window_frame, image=logo_photo, bg="white")
        labellogo.image = logo_photo  # Keep a reference to avoid garbage collection
        labellogo.pack(pady=10)

        # Add a dropdown menu for instance selection
        dropdown_label = ctk.CTkLabel(instance_window_frame, text="Select an Instance:", text_color="black",
                                      font=("Helvetica", 14))
        dropdown_label.pack(pady=10)

        file_var.set(sorted_file_list[0] if sorted_file_list else "")  # Set the first file as the default selection
        dropdown = ctk.CTkOptionMenu(instance_window_frame, variable=file_var, values=sorted_file_list,
                                     font=("Helvetica", 12),
                                     fg_color="black",
                                     dropdown_hover_color="#00008B",
                                     text_color="white")
        dropdown.pack(pady=10)

        # Add a "Solve" button
        solve_button = ctk.CTkButton(instance_window_frame, text="Solve", command=on_select,
                                     corner_radius=32,
                                     text_color="black",
                                     fg_color=fg_color,
                                     hover_color=hover_color,
                                     border_color=border_color,
                                     border_width=2)
        solve_button.pack(pady=20)

        # Add a "Back" button to return to the main menu
        back_button = ctk.CTkButton(instance_window_frame, text="Back", command=go_back_to_main_menu,
                                    corner_radius=32,
                                    text_color="black",
                                    fg_color=fg_color,
                                    hover_color=hover_color,
                                    border_color=border_color,
                                    border_width=2)
        back_button.pack(pady=10)

    # Function to return to the main menu
    def go_back_to_main_menu():
        instance_window_frame.pack_forget()  # Hide the instance selection frame
        main_menu_frame.pack(fill="both", expand=True)  # Show the main menu

    # Main menu frame
    main_menu_frame = tk.Frame(root, bg="white")  # Set the background of the main menu frame to white
    main_menu_frame.pack(fill="both", expand=True)

    # Add the logo above the label
    logo_image = Image.open("C:/Users/mabel/PycharmProjects/SAI CW 1/UON.png")  # Open the logo image using PIL
    logo_image = logo_image.resize((150, 50))  # Resize the logo to fit the UI

    # Convert the image to a format that Tkinter can use
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Create a label for the logo and store the reference to the image
    # noinspection PyTypeChecker
    logo_label = tk.Label(main_menu_frame, image=logo_photo, bg="white")  # Create the logo label
    logo_label.image = logo_photo  # Prevent the image from being garbage collected
    logo_label.pack(pady=10)  # Add padding to the label

    # Add a welcome message
    welcome_label = ctk.CTkLabel(main_menu_frame,
                                 text="Welcome to the Exam Timetabling Scheduler!",
                                 text_color="black",
                                 font=("Helvetica", 16, "bold"))
    welcome_label.pack(pady=10)

    # Add a label prompting the user to select an option
    select_label = ctk.CTkLabel(main_menu_frame,
                                text="Select an Option:",
                                text_color="black",
                                font=("Helvetica", 14))
    select_label.pack(pady=10)

    # Define button appearance properties
    fg_color = "transparent"  # Button foreground color
    hover_color = "#ADD8E6"  # Button hover color
    border_color = "black"  # Button border color

    # Add a button to display solutions for all instances
    all_solutions_button = ctk.CTkButton(main_menu_frame, text="Display Solutions for All Instances",
                                         command=on_display_all_solutions,
                                         corner_radius=32,
                                         text_color="black",
                                         fg_color=fg_color,
                                         hover_color=hover_color,
                                         border_color=border_color,
                                         border_width=2)
    all_solutions_button.pack(pady=20)

    # Add a button to display a solution for a specific instance
    specific_instance_button = ctk.CTkButton(main_menu_frame, text="Display Solution for a Specific Instance",
                                             text_color="black",
                                             command=on_display_solution_for_selected_instance,
                                             corner_radius=32,
                                             fg_color=fg_color,
                                             hover_color=hover_color,
                                             border_color=border_color,
                                             border_width=2)
    specific_instance_button.pack(pady=20)

    # Add a button to display constraint details
    constraint_details_button = ctk.CTkButton(main_menu_frame,
                                              text="Display Constraint Details",
                                              command=on_display_constraint_details,
                                              corner_radius=32,
                                              text_color="black",
                                              fg_color=fg_color,
                                              hover_color=hover_color,
                                              border_color=border_color,
                                              border_width=2)
    constraint_details_button.pack(pady=20)

    # Add an exit button to quit the application
    exit_button = ctk.CTkButton(main_menu_frame, text="Exit", command=root.quit,
                                corner_radius=32,
                                text_color="black",
                                fg_color=fg_color,
                                hover_color=hover_color,
                                border_color=border_color,
                                border_width=2)
    exit_button.pack(pady=20)

    # Create a hidden frame for instance selection
    instance_window_frame = tk.Frame(root, bg="white")

    # Start the main GUI loop
    root.mainloop()
