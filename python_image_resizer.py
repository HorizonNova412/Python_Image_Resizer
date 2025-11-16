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

    # Check if input and output path exist.
    if not os.path.exists(input_dir):
        messagebox.showinfo("Error", "The specified path does not exist. " \
        "Please enter a valid input path.")
    if not os.path.exists(output_dir):
        messagebox.showinfo("Error", "The specified path does not exist. " \
        "Please enter a valid output path.")

    # Check if entered max_size is a number
    try:
        max_size = int(max_size_var.get())
    except ValueError:
        messagebox.showinfo("Error", "Invalid input:\nSize must be a number.")

    # check if entered max_size is inbetween valid numbers.
    if max_size <= 0 or max_size > 10_000:
        messagebox.showinfo("Error", "Invalid input:\n" \
        "Size must be between\n1 and 10'000 pixels.")
        return  # Exit the function early
  
    print("INPUT DIR =", input_dir)
    print("OUTPUT DIR =", output_dir)
    print("LISTING:", os.listdir(input_dir) if os.path.isdir(input_dir) 
          else "NOT A DIRECTORY")

    # List of supported image formats
    supported_formats = (
        '.jpg', '.jpeg', '.bmp', '.png', '.gif', '.tiff', '.webp'
        )

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_formats):
            # Split the file name and extension
            name, ext = os.path.splitext(filename)

            # Specify the input path
            input_path = os.path.join(input_dir, filename)
            
            print(input_path)

            with Image.open(input_path) as img:
                width, height = img.size
                if min(width, height) > max_size:
                    aspect_ratio = width / height
                    if width < height:
                        new_width = max_size
                        new_height = int(max_size / aspect_ratio)
                    else:
                        new_height = max_size
                        new_width = int(max_size * aspect_ratio)
                    # Resize image
                    resized_img = img.resize(
                        (new_width, new_height), Image.LANCZOS)
                    # Add the suffix to the file name
                    output_filename = f"{name}_{new_width}x{new_height}{ext}"
                    # Specify the input path
                    output_path = os.path.join(output_dir, output_filename)
                    # Afe file to new location
                    print(output_path)
                    resized_img.save(output_path)
                    print(f"image {filename} resized")
                else:
                    output_filename = f"{name}_{width}x{height}{ext}"
                    output_path = os.path.join(output_dir, output_filename)
                    img.save(output_path)
                    print(f"image {filename} not resized")

    messagebox.showinfo("Complete", "Images resized successfully!")

# Create the main window
root = tk.Tk()
root.title("Python Image Resizer")

# Apply a theme
style = ttk.Style()
style.theme_use('clam')  # Use the 'clam' theme (clam, alt, default, classic)

# Configure styles for the widgets
style.configure('TButton', font=('Helvetica', 11), padding=5, 
                background='#5a4e8d', foreground='white')
style.configure('TLabel', font=('Helvetica', 11), background='#a797c0')
style.configure('TEntry', font=('Helvetica', 11), fieldbackground='#e6e0f0')

# Configure the main window background
root.configure(bg='#a797c0')

# Add an information box at the top with custom font and size
info_text = (
    "Welcome to the Image Resizer App!\n\n"
    "Here's how to use it:\n\n"
    "1. Select the folder containing your images (Input Directory).\n"
    "2. Choose a folder to save the resized images (Output Directory).\n"
    "3. Enter the desired maximum size for the shortest side of the images "\
        "(in pixels).\n"
    "4. Click 'Resize Images' to resize all images in the input folder.\n\n"
    "Note:\n"
    "- All images in the input folder will be resized to the specified size.\n"
    "- Your original files will remain unchanged."
)

info_label = ttk.Label(
    root,
    text=info_text,
    wraplength=1000,
    justify='left',
    font=('Helvetica', 11)
)
info_label.grid(row=0, column=0, columnspan=3, padx=5, pady=20)

# Set default directories
# Default to the user's download directory
default_input_dir = os.path.expanduser("~/Downloads/image_resizer_input")
# Default to the user's download directory
default_output_dir = os.path.expanduser("~/Downloads/image_resizer_output")

# Input directory selection
input_dir_label = ttk.Label(root, text="Input Directory:")
input_dir_label.grid(row=1, column=0, padx=5, pady=5)

input_dir_var = tk.StringVar(value=default_input_dir)
input_dir_entry = ttk.Entry(root, textvariable=input_dir_var, width=50)
input_dir_entry.grid(row=1, column=1, padx=5, pady=5)

input_dir_button = ttk.Button(
    root, text="Browse", command=lambda: 
    input_dir_var.set(filedialog.askdirectory(initialdir=default_input_dir)))
input_dir_button.grid(row=1, column=2, padx=5, pady=5)

# Output directory selection
output_dir_label = ttk.Label(root, text="Output Directory:")
output_dir_label.grid(row=2, column=0, padx=5, pady=5)

output_dir_var = tk.StringVar(value=default_output_dir)
output_dir_entry = ttk.Entry(root, textvariable=output_dir_var, width=50)
output_dir_entry.grid(row=2, column=1, padx=5, pady=5)

output_dir_button = ttk.Button(
    root, text="Browse", command=lambda: 
    output_dir_var.set(filedialog.askdirectory(initialdir=default_output_dir)))
output_dir_button.grid(row=2, column=2, padx=5, pady=5)

# Max size input
max_size_label = ttk.Label(root, text="Max Size (pixels):")
max_size_label.grid(row=3, column=0, padx=5, pady=5)

max_size_var = tk.StringVar(value="1080")
max_size_entry = ttk.Entry(root, textvariable=max_size_var, width=10)
max_size_entry.grid(row=3, column=1, padx=5, pady=5)

# Resize button
resize_button = ttk.Button(root, text="Resize Images", command=resize_images)
resize_button.grid(row=4, column=0, columnspan=3, pady=10)

# Run the application
root.mainloop()
