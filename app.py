
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QDialog, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView,  QTabWidget, QVBoxLayout
from PyQt6.QtGui import QIcon, QAction, QFont
from PyQt6.QtCore import Qt
import sqlite3
import sys
import subprocess
import datetime

font = QFont()
font.setPointSize(14)
font.setBold(True)

class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Adeko Duty Tracker")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon('adeko.ico'))

        # Calculate next saturday
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # put some right margin
        self.layout.setContentsMargins(20, 20, 0, 0)

        self.label = QLabel("Bir sonraki cumartesi:  " + str(datetime.date.today() + datetime.timedelta((5-datetime.date.today().weekday()) % 7)))
        self.label.setFont(font)
        self.layout.addWidget(self.label)

        #Show many days left for the next saturday
        self.label2 = QLabel("Bir sonraki cumartesine " + str((5-datetime.date.today().weekday()) % 7) + " gün kaldı")
        self.label2.setFont(font)
        self.layout.addWidget(self.label2)

        #people who were on duty last saturday
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dutychart WHERE date = ?', (str(datetime.date.today() + datetime.timedelta((5-datetime.date.today().weekday()) % 7 - 1)),))
        rows = cursor.fetchall()
        conn.close()
        if rows:
            self.label3 = QLabel("Geçen cumartesi nöbette olanlar: " + rows[0][2] + " and " + rows[0][3])
            self.label3.setFont(font)
        else:
            self.label3 = QLabel("Geçen cumartesi nöbette olanlar hakkında veri yok")
            self.label3.setFont(font)
        self.layout.addWidget(self.label3)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)

        self.setCentralWidget(self.central_widget)

        #possible people who will be on duty next saturday
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE cancomealone = ?', (True,))
        rows = cursor.fetchall()
        conn.close()

        if rows:
            availablePeople = ', '.join([row[1] for row in rows])
            self.label4 = QLabel(f"Gelmeye müsait olan kişiler: {availablePeople}")
            self.label4.setFont(font)
            self.layout.addWidget(self.label4)
        else:
            self.label4 = QLabel("No people can come alone")
            self.label4.setFont(font)
            self.layout.addWidget(self.label4)

    # Set up the menu bar
        menubar = self.menuBar()
        actions_menu = menubar.addMenu('Actions')

        open_action = QAction('See Employee Data', self)
        open_action.triggered.connect(self.open_employee_data)
        actions_menu.addAction(open_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        actions_menu.addAction(exit_action)
        
    def open_employee_data(self):
        subprocess.run(["python", "libs/employeedata.py"])

if __name__ == "__main__":
    app = QApplication([])
    main_interface = MainInterface()
    main_interface.show()
    app.exec()