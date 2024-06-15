import tkinter as tk
from tkinter import ttk
import sqlite3

def fetch_data():
    # Connect to SQLite database
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Fetch data
    cursor.execute('SELECT * FROM employees')
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    return rows

def display_table():
    # Fetch data
    rows = fetch_data()

    # Create the main window
    root = tk.Tk()
    root.title("Adeko Duty Counter")

    # Create Treeview
    tree = ttk.Treeview(root, columns=("ID", "Name", "Age", "Department"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Department", text="Department")

    # Insert data into Treeview
    for row in rows:
        tree.insert("", tk.END, values=row)

    # Pack the Treeview widget
    tree.pack(expand=True, fill='both')

    # Start the Tkinter event loop
    root.mainloop()

# Call the function to display the table
display_table()
