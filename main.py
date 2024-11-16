import tkinter as tk
from pathlib import Path
import os
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow for image manipulation
import customtkinter as ctk

from solutiondisplay import display_all_solutions, natural_sort_key, display_solution_for_selected_instance, \
    on_display_constraint_details

# Main GUI setup
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Exam Scheduling Solver")

    # Set the initial dimensions for the window
    window_width = 500
    window_height = 500
    root.geometry(f"{window_width}x{window_height}")  # You can adjust this as per your design

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the position to place the window on the right side of the screen
    x_position = screen_width - window_width  # Position the window at the far right
    y_position = (screen_height - window_height) // 2  # Center vertically

    # Set the position of the window
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Set the background color of the main window to white
    root.config(bg="white")

    # Path to the directory containing instances
    instances_dir = Path("C:/Users/mabel/PycharmProjects/SAI CW 1/test instances")

    # Define file_var globally, so it can be accessed in the on_select function
    file_var = tk.StringVar()

    def on_display_all_solutions():
        # Show message box indicating loading
        messagebox.showinfo("Loading", "Loading the solutions, please check the run terminal.")
        display_all_solutions(instances_dir)

    def on_display_solution_for_selected_instance():
        file_list = [f for f in os.listdir(instances_dir) if f.endswith('.txt')]
        sorted_file_list = sorted(file_list, key=natural_sort_key)

        def on_select():
            selected_instance = file_var.get()
            if not selected_instance:
                tk.messagebox.showerror("Error", "No instance selected.")
                return
            display_solution_for_selected_instance(instances_dir, file_var)

        # Hide the main menu and show the instance selection frame
        main_menu_frame.pack_forget()
        instance_window_frame.pack(fill="both", expand=True)

        # Clear existing widgets in instance_window_frame
        for widget in instance_window_frame.winfo_children():
            widget.destroy()

        # Add the logo to the top of the frame
        # noinspection PyTypeChecker
        labellogo = tk.Label(instance_window_frame, image=logo_photo, bg="white")
        labellogo.image = logo_photo  # Keep a reference to avoid garbage collection
        labellogo.pack(pady=10)

        # Add dropdown menu for instance selection
        dropdown_label = ctk.CTkLabel(instance_window_frame, text="Select an Instance:", text_color="black",
                                      font=("Helvetica", 14))
        dropdown_label.pack(pady=10)

        file_var.set(sorted_file_list[0] if sorted_file_list else "")
        dropdown = ctk.CTkOptionMenu(instance_window_frame, variable=file_var, values=sorted_file_list,
                                     font=("Helvetica", 12),
                                     fg_color="black",
                                     dropdown_hover_color="#00008B",
                                     text_color="white")
        dropdown.pack(pady=10)

        # Add Solve button
        solve_button = ctk.CTkButton(instance_window_frame, text="Solve", command=on_select,
                                     corner_radius=32,
                                     text_color="black",
                                     fg_color=fg_color,
                                     hover_color=hover_color,
                                     border_color=border_color,
                                     border_width=2)
        solve_button.pack(pady=20)

        # Add Back button
        back_button = ctk.CTkButton(instance_window_frame, text="Back", command=go_back_to_main_menu,
                                    corner_radius=32,
                                    text_color="black",
                                    fg_color=fg_color,
                                    hover_color=hover_color,
                                    border_color=border_color,
                                    border_width=2)
        back_button.pack(pady=10)

    def go_back_to_main_menu():
        # Hide instance selection frame and show main menu
        instance_window_frame.pack_forget()  # Hide instance selection frame
        main_menu_frame.pack(fill="both", expand=True)  # Show main menu

    # Main menu frame
    main_menu_frame = tk.Frame(root, bg="white")  # Set background of main menu frame to white
    main_menu_frame.pack(fill="both", expand=True)

    # Add logo above the label
    logo_image = Image.open("C:/Users/mabel/PycharmProjects/SAI CW 1/UON.png")  # Open the image using PIL
    logo_image = logo_image.resize((150, 50))  # Resize image to fit the UI (Adjust size as needed)

    # Convert the image to a format Tkinter can use
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Create a label for the logo, and ensure the reference to the image is stored in the label
    # noinspection PyTypeChecker
    logo_label = tk.Label(main_menu_frame, image=logo_photo, bg="white")  # Create a label for the logo
    logo_label.image = logo_photo  # Keep a reference to the image to prevent garbage collection

    # Place the logo label with padding
    logo_label.pack(pady=10)

    # Add welcome message above "Select an Option"
    welcome_label = ctk.CTkLabel(main_menu_frame,
                                 text="Welcome to the Exam Timetabling Scheduler!",
                                 text_color="black",
                                 font=("Helvetica", 16, "bold"))
    welcome_label.pack(pady=10)  # Add padding for better spacing

    # Ensure "Select an Option" is also visible
    select_label = ctk.CTkLabel(main_menu_frame,
                                text="Select an Option:",
                                text_color="black",
                                font=("Helvetica", 14))
    select_label.pack(pady=10)  # Add padding for better spacing

    # Buttons
    fg_color = "transparent"  # Foreground color (button color)
    hover_color = "#ADD8E6"  # Hover color (when mouse hovers)
    border_color = "black"  # Border color

    # Display Solutions for All Instances Button
    all_solutions_button = ctk.CTkButton(main_menu_frame, text="Display Solutions for All Instances",
                                         command=on_display_all_solutions,
                                         corner_radius=32,
                                         text_color="black",
                                         fg_color=fg_color,
                                         hover_color=hover_color,
                                         border_color=border_color,
                                         border_width=2)
    all_solutions_button.pack(pady=20)

    # Display Solution for Specific Instance Button
    specific_instance_button = ctk.CTkButton(main_menu_frame, text="Display Solution for a Specific Instance",
                                             text_color="black",
                                             command=on_display_solution_for_selected_instance,
                                             corner_radius=32,
                                             fg_color=fg_color,
                                             hover_color=hover_color,
                                             border_color=border_color,
                                             border_width=2)
    specific_instance_button.pack(pady=20)

    # Display Constraint Details Button
    constraint_details_button = ctk.CTkButton(main_menu_frame,
                                              text="Display Constraint Details",
                                              command=on_display_constraint_details,
                                              corner_radius=32,
                                              text_color="black",
                                              fg_color=fg_color,  # Apply foreground color
                                              hover_color=hover_color,  # Apply hover color
                                              border_color=border_color,
                                              border_width=2)  # Set border width for visibility
    constraint_details_button.pack(pady=20)

    # Exit Button
    exit_button = ctk.CTkButton(main_menu_frame, text="Exit", command=root.quit,
                                corner_radius=32,
                                text_color="black",
                                fg_color=fg_color,
                                hover_color=hover_color,
                                border_color=border_color,
                                border_width=2)
    exit_button.pack(pady=20)

    # Instance selection frame (hidden by default)
    instance_window_frame = tk.Frame(root, bg="white")

    # Start the main GUI loop
    root.mainloop()
