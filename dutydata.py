from PyQt6.QtWidgets import QApplication, QHBoxLayout, QDialog, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView,  QTabWidget, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sqlite3
import sys

dbpath = "data.db"
iconpath = "adeko.ico"

class DutyChartApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1100, 768)
        self.setFixedSize(1100, 768)
        self.setWindowTitle("Duty Chart")
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
        self.edit_button = QPushButton("Edit")
        self.edit_button.setFixedWidth(100)
        self.edit_button.setFixedHeight(50)
        self.edit_button.clicked.connect(self.edit_duty)
        button_layout.addWidget(self.edit_button)

        #delete row button
        self.delete_button = QPushButton("Delete")
        self.delete_button.setFixedWidth(100)
        self.delete_button.setFixedHeight(50)
        self.delete_button.clicked.connect(self.delete_duty)
        button_layout.addWidget(self.delete_button)

        # Add the button layout to the main layout
        self.layout.addLayout(button_layout)

        self.display_table()

    def fetch_data(self):
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dutychart')
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def display_table(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "First Person", "Second Person", "Month"])

        rows = self.fetch_data()
        for i, row in enumerate(rows):
            self.table.insertRow(i)
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

    def edit_duty(self):
        if len(self.table.selectedItems()) == 0:
            QMessageBox.critical(self, "Error", "Please select a row to edit")
            return

        row = self.table.selectedItems()[0].row()
        id = self.table.item(row, 0).text()
        date = self.table.item(row, 1).text()
        first_person = self.table.item(row, 2).text()
        second_person = self.table.item(row, 3).text()
        month = self.table.item(row, 4).text()

        dialog = EditDutyDialog(self, id, date, first_person, second_person, month)
        dialog.exec()
        self.display_table()

    def delete_duty(self):
        if len(self.table.selectedItems()) == 0:
            QMessageBox.critical(self, "Error", "Please select a row to delete")
            return

        row = self.table.selectedItems()[0].row()
        id = self.table.item(row, 0).text()

        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM dutychart WHERE id = ?', (id,))
        conn.commit()
        conn.close()

        self.display_table()

class EditDutyDialog(QDialog):
    def __init__(self, parent, id, date, first_person, second_person, month):
        super().__init__(parent)
        self.setWindowTitle("Edit Duty")
        self.setWindowIcon(QIcon(iconpath))

        self.layout = QVBoxLayout(self)

        self.id = id

        self.date_label = QLabel("Date")
        self.layout.addWidget(self.date_label)

        self.date_input = QLineEdit()
        self.date_input.setText(date)
        self.layout.addWidget(self.date_input)

        self.first_person_label = QLabel("First Person")
        self.layout.addWidget(self.first_person_label)

        self.first_person_input = QLineEdit()
        self.first_person_input.setText(first_person)
        self.layout.addWidget(self.first_person_input)

        self.second_person_label = QLabel("Second Person")
        self.layout.addWidget(self.second_person_label)

        self.second_person_input = QLineEdit()
        self.second_person_input.setText(second_person)
        self.layout.addWidget(self.second_person_input)

        self.month_label = QLabel("Month")
        self.layout.addWidget(self.month_label)

        self.month_input = QLineEdit()
        self.month_input.setText(month)
        self.layout.addWidget(self.month_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)
        self.layout.addWidget(self.save_button)

    def save(self):
        date = self.date_input.text()
        first_person = self.first_person_input.text()
        second_person = self.second_person_input.text()
        month = self.month_input.text()

        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        cursor.execute('UPDATE dutychart SET date = ?, first_person = ?, second_person = ?, month = ? WHERE id = ?', (date, first_person, second_person, month, self.id))
        conn.commit()
        conn.close()

        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DutyChartApp()
    window.show()
    sys.exit(app.exec())