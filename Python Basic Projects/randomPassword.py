import tkinter as tk
from tkinter import messagebox
import random
import string

# Function to generate a random password
def generate_password():
    length = int(length_entry.get())
    if length < 6:
        messagebox.showerror("Error", "Password length must be at least 6 characters")
    else:
        password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

# Create the main window
window = tk.Tk()
window.title("Random Password Generator")

# Create labels
length_label = tk.Label(window, text="Password Length:")
password_label = tk.Label(window, text="Generated Password:")

# Create entry fields
length_entry = tk.Entry(window)
password_entry = tk.Entry(window, show='*')

# Create a generate button
generate_button = tk.Button(window, text="Generate Password", command=generate_password)

# Place widgets in the window
length_label.grid(row=0, column=0, padx=10, pady=10)
length_entry.grid(row=0, column=1, padx=10, pady=10)
generate_button.grid(row=1, column=0, columnspan=2, pady=10)
password_label.grid(row=2, column=0, padx=10, pady=10)
password_entry.grid(row=2, column=1, padx=10, pady=10)

# Start the main loop
window.mainloop()
