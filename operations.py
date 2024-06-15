import tkinter as tk
from tkinter import ttk, messagebox

def create_employee():
    # Create a new window
    new_window = tk.Toplevel()
    new_window.title("Create Employee")

    # Create labels and entry widgets for each field
    name_label = tk.Label(new_window, text="Name")
    name_entry = tk.Entry(new_window)
    department_label = tk.Label(new_window, text="Department")
    department_entry = tk.Entry(new_window)
    marketing_label = tk.Label(new_window, text="Marketing (True/False)")
    marketing_entry = tk.Entry(new_window)
    designing_label = tk.Label(new_window, text="Designing (True/False)")
    designing_entry = tk.Entry(new_window)
    scripting_label = tk.Label(new_window, text="Scripting (True/False)")
    scripting_entry = tk.Entry(new_window)
    machineknowledge_label = tk.Label(new_window, text="Machine Knowledge (True/False)")
    machineknowledge_entry = tk.Entry(new_window)

    # Function to handle the submit button click
    def submit():
        # Connect to SQLite database
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        # Insert a new employee
        cursor.execute('INSERT INTO employees (name, department, marketing, designing, scripting, machineknowledge, numberOfHolidays) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                       (name_entry.get(), department_entry.get(), marketing_entry.get() == 'True', designing_entry.get() == 'True', scripting_entry.get() == 'True', machineknowledge_entry.get() == 'True', 0))

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        # Close the new window
        new_window.destroy()

        # Refresh the table
        display_table()

    # Create the submit button
    submit_button = tk.Button(new_window, text="Submit", command=submit)

    # Pack the labels, entries, and button
    name_label.pack()
    name_entry.pack()
    department_label.pack()
    department_entry.pack()
    marketing_label.pack()
    marketing_entry.pack()
    designing_label.pack()
    designing_entry.pack()
    scripting_label.pack()
    scripting_entry.pack()
    machineknowledge_label.pack()
    machineknowledge_entry.pack()
    submit_button.pack()

def update_employee():
    # Create a new window
    new_window = tk.Toplevel()
    new_window.title("Update Employee")

    # Create a label and entry widget for the employee ID
    id_label = tk.Label(new_window, text="Employee ID")
    id_entry = tk.Entry(new_window)

    # Create labels and entry widgets for each field
    name_label = tk.Label(new_window, text="Name")
    name_entry = tk.Entry(new_window)
    department_label = tk.Label(new_window, text="Department")
    department_entry = tk.Entry(new_window)
    marketing_label = tk.Label(new_window, text="Marketing (True/False)")
    marketing_entry = tk.Entry(new_window)
    designing_label = tk.Label(new_window, text="Designing (True/False)")
    designing_entry = tk.Entry(new_window)
    scripting_label = tk.Label(new_window, text="Scripting (True/False)")
    scripting_entry = tk.Entry(new_window)
    machineknowledge_label = tk.Label(new_window, text="Machine Knowledge (True/False)")
    machineknowledge_entry = tk.Entry(new_window)
    numberOfHolidays_label = tk.Label(new_window, text="Number of Holidays")
    numberOfHolidays_entry = tk.Entry(new_window)

    # Function to handle the submit button click
    def submit():
        # Connect to SQLite database
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        # Update the employee
        cursor.execute('UPDATE employees SET name = ?, department = ?, marketing = ?, designing = ?, scripting = ?, machineknowledge = ?, numberOfHolidays = ? WHERE id = ?', 
                       (name_entry.get(), department_entry.get(), marketing_entry.get() == 'True', designing_entry.get() == 'True', scripting_entry.get() == 'True', machineknowledge_entry.get() == 'True', int(numberOfHolidays_entry.get()), int(id_entry.get())))

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        # Close the new window
        new_window.destroy()

        # Refresh the table
        display_table()

    # Create the submit button
    submit_button = tk.Button(new_window, text="Submit", command=submit)

    # Pack the labels, entries, and button
    id_label.pack()
    id_entry.pack()
    name_label.pack()
    name_entry.pack()
    department_label.pack()
    department_entry.pack()
    marketing_label.pack()
    marketing_entry.pack()
    designing_label.pack()
    designing_entry.pack()
    scripting_label.pack()
    scripting_entry.pack()
    machineknowledge_label.pack()
    machineknowledge_entry.pack()
    numberOfHolidays_label.pack()
    numberOfHolidays_entry.pack()
    submit_button.pack()

def delete_employee():
    # Create a new window
    new_window = tk.Toplevel()
    new_window.title("Delete Employee")

    # Create a label and entry widget for the employee ID
    id_label = tk.Label(new_window, text="Employee ID")
    id_entry = tk.Entry(new_window)

    # Function to handle the submit button click
    def submit():
        # Connect to SQLite database
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        # Delete the employee
        cursor.execute('DELETE FROM employees WHERE id = ?', (int(id_entry.get()),))

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        # Close the new window
        new_window.destroy()

        # Refresh the table
        display_table()

    # Create the submit button
    submit_button = tk.Button(new_window, text="Submit", command=submit)

    # Pack the label, entry, and button
    id_label.pack()
    id_entry.pack()
    submit_button.pack()
