from PyQt6.QtWidgets import QApplication, QHBoxLayout, QDialog, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView,  QTabWidget, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sqlite3
import sys

dbpath = "db.db"
iconpath = "adeko.ico"

class EmployeeDataApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1100, 768)
        self.setFixedSize(1100, 768)
        self.setWindowTitle("Employee Data")
        self.setWindowIcon(QIcon(iconpath))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.layout.addWidget(self.table)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        self.create_button = QPushButton("Create")
        self.create_button.setFixedWidth(100)
        self.create_button.setFixedHeight(50)
        self.create_button.clicked.connect(self.create_employee)
        button_layout.addWidget(self.create_button)

        self.update_button = QPushButton("Update")
        self.update_button.setFixedWidth(100)
        self.update_button.setFixedHeight(50)
        self.update_button.clicked.connect(self.update_employee)
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setFixedWidth(100)
        self.delete_button.setFixedHeight(50)
        self.delete_button.clicked.connect(self.delete_employee)
        button_layout.addWidget(self.delete_button)

        # Add the button layout to the main layout
        self.layout.addLayout(button_layout)

        self.display_table()

    def fetch_data(self):
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees')
        rows = cursor.fetchall()
        conn.close()
        return rows

    def display_table(self):
        rows = self.fetch_data()
        self.table.setRowCount(0)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Department", "Group","Last duty date", "Number of Holidays"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)  # Set fixed width for columns
        for i in range(6):
            self.table.setColumnWidth(i, 150)  # Set the width of each column to 100 pixels
        for row_data in rows:
            row_number = self.table.rowCount()
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def create_employee(self):
        self.create_employee_dialog = CreateEmployeeDialog(self)
        self.create_employee_dialog.show()

    def update_employee(self):
        selected_rows = self.table.selectedItems()
    
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "You didn't select an employee!")
            return
    
        selected_row = []
        for i in range(self.table.columnCount()):  # Assuming you have multiple columns
            selected_row.append(selected_rows[i].text())
    
        self.update_dialog = UpdateEmployeeDialog(selected_row, self)
        self.update_dialog.show()
    
    def delete_employee(self):
        selected_items = self.table.selectedItems()
    
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "You didn't select an employee!")
            return
    
        selected_item = selected_items[0]  # get selected item
        selected_row = self.table.row(selected_item)
        row_items = [self.table.item(selected_row, col).text() for col in range(self.table.columnCount())]
    
        # Ask for confirmation before deleting
        reply = QMessageBox.question(self, 'Confirmation', "Are you sure you want to delete this employee?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    
        if reply == QMessageBox.StandardButton.Yes:
            # Connect to SQLite database
            conn = sqlite3.connect(dbpath)
            cursor = conn.cursor()
    
            # Delete the employee
            cursor.execute('DELETE FROM employees WHERE id = ?', (int(row_items[0]),))
            cursor.execute('DELETE FROM notavailablepeople WHERE name = ?', (row_items[1],))
    
            # Commit changes and close the connection
            conn.commit()
            conn.close()
    
            # Refresh the table
            self.display_table()
# Rest of the code...
class CreateEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Create Employee")

        self.layout = QVBoxLayout(self)

        self.labels = ["Name", "Department", "Group"]
        self.entries = {}

        for label in self.labels:
            self.layout.addWidget(QLabel(label))
            self.entries[label] = QLineEdit()
            self.layout.addWidget(self.entries[label])

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

    def submit(self):
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()

        cursor.execute('INSERT INTO employees (name, department, group, lastdutydate, numberOfHolidays) VALUES (?, ?, ?, ?, ?)',
                       (self.entries["Name"].text(), self.entries["Department"].text(),  self.entries["Group"].text() == "1", 0, "", 0))

        cursor.execute('INSERT INTO notavailablepeople (name, availability) VALUES (?, ?)', (self.entries["Name"].text(), 1))

        conn.commit()
        conn.close()

        self.close()

        # Refresh the table
        self.parent().display_table()

class UpdateEmployeeDialog(QDialog):
    def __init__(self, selected_row, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Update Employee")

        self.layout = QVBoxLayout(self)

        self.labels = ["Employee ID", "Name", "Department", "Group", "Number of Holidays"]
        self.entries = {}

        for i, label in enumerate(self.labels):
            self.layout.addWidget(QLabel(label))
            self.entries[label] = QLineEdit()
            self.entries[label].setText(str(selected_row[i]))
            self.layout.addWidget(self.entries[label])

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

    def submit(self):
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()

        cursor.execute('UPDATE employees SET name = ?, department = ?, group = ?, numberOfHolidays = ? WHERE id = ?',
                       (self.entries["Name"].text(), self.entries["Department"].text(), self.entries["Group"].text() == "1",int(self.entries["Number of Holidays"].text()), int(self.entries["Employee ID"].text())))

        cursor.execute('UPDATE notavailablepeople SET name = ? WHERE name = ?', (self.entries["Name"].text(), self.entries["Name"].text()))
        conn.commit()
        conn.close()

        self.close()

        # Refresh the table
        self.parent().display_table()


app = QApplication(sys.argv)

window = EmployeeDataApp()
window.show()

sys.exit(app.exec())