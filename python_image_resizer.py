"""
Python_Image_Resizer
A simple Tkinter-based application for resizing images to a specified maximum 
dimension, designed for use under Linux.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image

def resize_images():
    input_dir = input_dir_var.get()
    output_dir = output_dir_var.get()
    # TODO: Check if image size is a aceptable value
    # def validate_max_size_input(new_value):
    max_size = int(max_size_var.get())

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            with Image.open(input_path) as img:
                width, height = img.size
                if max(width, height) > max_size:
                    aspect_ratio = width / height
                    if width > height:
                        new_width = max_size
                        new_height = int(max_size / aspect_ratio)
                    else:
                        new_height = max_size
                        new_width = int(max_size * aspect_ratio)
                    resized_img = img.resize(
                        (new_width, new_height), Image.LANCZOS)
                    resized_img.save(output_path)
                else:
                    img.save(output_path)

    messagebox.showinfo("Complete", "Images resized successfully!")

# Create the main window
root = tk.Tk()
root.title("Python Image Resizer")

# Apply a modern theme
style = ttk.Style()
style.theme_use('clam')  # Use the 'clam' theme (clam, alt, default, classic)

# Configure styles for the widgets
style.configure('TButton', font=('Helvetica', 10), padding=5, 
                background='#0078d7', foreground='white')
style.configure('TLabel', font=('Helvetica', 10), background='#f0f0f0')
style.configure('TEntry', font=('Helvetica', 10), fieldbackground='#ffffff')

# Configure the main window background
root.configure(bg='#f0f0f0')

# Set default directories
# Default to the user's Pictures directory
default_input_dir = os.path.expanduser("~/Pictures")
# Default to a Resized subdirectory in Pictures
default_output_dir = os.path.expanduser("~/Pictures")

# Input directory selection
input_dir_label = ttk.Label(root, text="Input Directory:")
input_dir_label.grid(row=0, column=0, padx=5, pady=5)
input_dir_var = tk.StringVar()
input_dir_entry = ttk.Entry(root, textvariable=input_dir_var, width=50)
input_dir_entry.grid(row=0, column=1, padx=5, pady=5)
input_dir_button = ttk.Button(
    root, text="Browse", command=lambda: 
    input_dir_var.set(filedialog.askdirectory(initialdir=default_input_dir)))
input_dir_button.grid(row=0, column=2, padx=5, pady=5)

# Output directory selection
output_dir_label = ttk.Label(root, text="Output Directory:")
output_dir_label.grid(row=1, column=0, padx=5, pady=5)
output_dir_var = tk.StringVar()
output_dir_entry = ttk.Entry(root, textvariable=output_dir_var, width=50)
output_dir_entry.grid(row=1, column=1, padx=5, pady=5)
output_dir_button = ttk.Button(
    root, text="Browse", command=lambda: 
    output_dir_var.set(filedialog.askdirectory(initialdir=default_output_dir)))
output_dir_button.grid(row=1, column=2, padx=5, pady=5)

# Max size input
max_size_label = ttk.Label(root, text="Max Size (pixels):")
max_size_label.grid(row=2, column=0, padx=5, pady=5)
max_size_var = tk.StringVar(value="1080")
max_size_entry = ttk.Entry(root, textvariable=max_size_var, width=10)
max_size_entry.grid(row=2, column=1, padx=5, pady=5)

# Resize button
resize_button = ttk.Button(root, text="Resize Images", command=resize_images)
resize_button.grid(row=3, column=0, columnspan=3, pady=10)

# Run the application
root.mainloop()
