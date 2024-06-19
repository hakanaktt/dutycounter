from PyQt6.QtWidgets import QApplication, QHBoxLayout, QComboBox, QDialog, QCalendarWidget, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView,  QTabWidget, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sqlite3
import sys

dbpath = "db.db"
iconpath = "adeko.ico"

class OfftimeDataApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1100, 768)
        self.setFixedSize(1100, 768)
        self.setWindowTitle("Offtime Data")
        self.setWindowIcon(QIcon(iconpath))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.layout.addWidget(self.table)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        #edit row button
        self.add_button = QPushButton("Add Offtime")
        self.add_button.setFixedWidth(100)
        self.add_button.setFixedHeight(50)
        self.add_button.clicked.connect(self.add_offtime)
        button_layout.addWidget(self.add_button)

        #delete row button
        self.delete_button = QPushButton("Delete")
        self.delete_button.setFixedWidth(100)
        self.delete_button.setFixedHeight(50)
        self.delete_button.clicked.connect(self.delete_offtime)
        button_layout.addWidget(self.delete_button)

        # Add the button layout to the main layout
        self.layout.addLayout(button_layout)

        self.display_table()

    def fetch_data(self):
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM holidaychart')
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def display_table(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Name", "Amount"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        for row in self.fetch_data():
            self.table.insertRow(self.table.rowCount())
            for column, item in enumerate(row):
                self.table.setItem(self.table.rowCount() - 1, column, QTableWidgetItem(str(item)))

    def add_offtime(self):
        dialog = add_offtime(self)
        dialog.exec()
        self.display_table()

    def delete_offtime(self):
        if len(self.table.selectedItems()) == 0:
            return

        row = self.table.selectedItems()[0].row()
        id = self.table.item(row, 0).text()

        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM holidaychart WHERE id = ?', (id,))
        conn.commit()
        conn.close()

        self.display_table()

class add_offtime(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Offtime")

        self.layout = QVBoxLayout(self)

        self.labels = ["Date", "Name", "Amount"]
        self.entries = {}

        for label in self.labels:
            if label == "Name":
                self.entries[label] = QComboBox()
                self.load_names()
            else:
                self.entries[label] = QLineEdit()
            self.layout.addWidget(self.entries[label])

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)
        self.layout.addWidget(self.save_button)

        #choose date from the calendar
        self.entries["Date"].setReadOnly(True)
        self.entries["Date"].setPlaceholderText("Click to choose date")
        self.entries["Date"].mousePressEvent = self.show_calendar

    def load_names(self):
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM employees')
        names = cursor.fetchall()
        conn.close()

        for name in names:
            self.entries["Name"].addItem(name[0])

    def show_calendar(self, event):
        self.calendar = QCalendarWidget()
        self.calendar.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.calendar.clicked.connect(self.set_date)
        self.calendar.show()

    def set_date(self, event):
        self.entries["Date"].setText(self.calendar.selectedDate().toString("yyyy-MM-dd"))
        self.calendar.close()

    def save(self):
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO holidaychart (date, name, amount) VALUES (?, ?, ?)', 
                       (self.entries["Date"].text(), self.entries["Name"].currentText(), float(self.entries["Amount"].text())))
        cursor.execute('UPDATE employees SET numberOfHolidays = numberOfHolidays - ? WHERE name = ?', (float(self.entries["Amount"].text()), self.entries["Name"].currentText(),))
        conn.commit()
        conn.close()
    
        self.close()
    
        self.parent().display_table()

class OfftimeDialog(QDialog):
    def __init__(self, parent, id, name):
        super().__init__(parent)
        self.setWindowTitle("Offtime Table")
        self.setWindowIcon(QIcon(iconpath))

        self.layout = QVBoxLayout(self)

        self.id = id

        self.name_label = QLabel("Name")
        self.layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.name_input.setText(name)
        self.layout.addWidget(self.name_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)
        self.layout.addWidget(self.save_button)

    def save(self):
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        cursor.execute('UPDATE holidaychart SET name = ? WHERE id = ?', (self.name_input.text(), self.id))
        conn.commit()
        conn.close()

        self.accept()

app = QApplication(sys.argv)
window = OfftimeDataApp()
window.show()
sys.exit(app.exec())