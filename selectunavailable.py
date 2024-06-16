from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QCheckBox, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction, QFont
import sqlite3

font = QFont()
font.setPointSize(12)
font.setBold(True)

dbpath = "data.db"
iconpath = "adeko.ico"

class Availability(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Set availability")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon(iconpath))

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.label = QLabel("Select the boxes for the people who are not available")
        self.label.setFont(font)
        self.layout.addWidget(self.label)

        # Connect to the database
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()

        # Execute a query
        cursor.execute("SELECT * FROM employees")
        cursor.execute("SELECT * FROM notavailablepeople")

        # Fetch all rows from the last executed statement
        rows = cursor.fetchall()

        # Close the connection
        conn.close()

        self.checkboxes = []
        for row in rows:
            checkbox = QCheckBox(row[1])
            if row[2] == '0':  # Assuming the availability is in the third column
                checkbox.setChecked(True)
            self.layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.submit_button.setFixedWidth(100)
        self.layout.addWidget(self.submit_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)

        self.setCentralWidget(self.central_widget)

    def submit(self):
        # Connect to the database
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()

        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                # Update the notavailablepeople table
                cursor.execute("UPDATE notavailablepeople SET availability = '0' WHERE name = ?", (checkbox.text(),))
            else:
                # Update the notavailablepeople table
                cursor.execute("UPDATE notavailablepeople SET availability = '1' WHERE name = ?", (checkbox.text(),))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Close the window
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    main_interface = Availability()
    main_interface.show()
    app.exec()