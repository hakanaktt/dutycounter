import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    cancomealone BOOLEAN NOT NULL, 
    numberOfHolidays INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS dutychart (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    firstonduty TEXT NOT NULL,
    secondonduty TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS holidaychart (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    name TEXT NOT NULL,
    amount INTEGER NOT NULL
)
''')

# Insert sample data
cursor.execute('INSERT INTO employees (name, department, cancomealone, numberOfHolidays) VALUES (?, ?, ?, ?)', ('Yusuf', 'Support', True, 10))

# Commit changes and close the connection
conn.commit()
conn.close()