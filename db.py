import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('db.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    cancomealone TEXT NOT NULL, 
    beenonduty INTEGER NOT NULL,
    lastdutydate TEXT NOT NULL,
    numberOfHolidays INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS dutychart (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    firstonduty TEXT NOT NULL,
    secondonduty TEXT NOT NULL,
    month TEXT NOT NULL
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

cursor.execute('''
CREATE TABLE IF NOT EXISTS notavailablepeople (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    availability TEXT NOT NULL
)
''')

# Insert sample data
cursor.execute('INSERT INTO employees (name, department, cancomealone, beenonduty, lastdutydate, numberOfHolidays) VALUES (?, ?, ?, ?, ?, ?)', ('Yusuf', 'Support', "1", 1, "2024-06-12", 10))
cursor.execute('INSERT INTO dutychart (date, firstonduty, secondonduty) VALUES (?, ?, ?)', ('2024-06-12', 'Yusuf', 'Hakan'))
cursor.execute('INSERT INTO notavailablepeople (name, availability) VALUES (?, ?)', ('  Yusuf', 1))
cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', 'admin'))
# Commit changes and close the connection
conn.commit()
conn.close()