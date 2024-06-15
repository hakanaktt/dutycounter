import tkinter as tk
from tkinter import ttk, messagebox
from operations import create_employee, update_employee, delete_employee

# ... (the rest of your script goes here)

import sqlite3

root = None

def fetch_data():
    # Connect to SQLite database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Fetch data
    cursor.execute('SELECT * FROM employees')
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    return rows

def display_table():
    global root

    # Fetch data
    rows = fetch_data()

    # Check if the main window already exists
    if root is not None:
        # Clear the existing table
        for widget in root.winfo_children():
            widget.destroy()
    else:
        # Create the main window
        root = tk.Tk()
        root.title("Employee Data")

    # Create Treeview
    tree = ttk.Treeview(root, columns=("ID", "Name", "Department", "Marketing", "Designing", "Scripting", "Machine Knowledge", "Number of Holidays"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Department", text="Department")
    tree.heading("Marketing", text="Marketing")
    tree.heading("Designing", text="Designing")
    tree.heading("Scripting", text="Scripting")
    tree.heading("Machine Knowledge", text="Machine Knowledge")
    tree.heading("Number of Holidays", text="Number of Holidays")

    # Insert data into Treeview
    for row in rows:
        tree.insert("", tk.END, values=row)

    # Create CRUD buttons
    create_button = tk.Button(root, text="Create", command=create_employee)




    update_button = tk.Button(root, text="Update", command=update_employee)
    delete_button = tk.Button(root, text="Delete", command=delete_employee)

    # Pack the Treeview widget and the buttons
    tree.pack(expand=True, fill='both')
    create_button.pack(side='left', padx=(10, 0))
    update_button.pack(side='left')
    delete_button.pack(side='left')

    # Start the Tkinter event loop
    root.mainloop()

# Call the function to display the table
display_table()