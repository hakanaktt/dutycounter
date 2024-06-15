from PyQt6.QtWidgets import QApplication, QHBoxLayout, QDialog, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView,  QTabWidget, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sqlite3
import sys
import subprocess


class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Interface")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon('adeko.ico'))

        self.button = QPushButton("Open Employee Data", self)
        self.button.setFixedSize(200, 50)
        self.button.clicked.connect(self.open_employee_data)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)

        self.setCentralWidget(self.central_widget)
        
    def open_employee_data(self):
        subprocess.run(["python", "C:/Git/dutycounter/libs/employeedata.py"])

if __name__ == "__main__":
    app = QApplication([])
    main_interface = MainInterface()
    main_interface.show()
    app.exec()