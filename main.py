from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QComboBox, QDialog, QCalendarWidget, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView,  QTabWidget, QVBoxLayout
from PyQt6.QtGui import QIcon, QAction, QFont
from PyQt6.QtCore import Qt
import sqlite3, subprocess, sys, datetime, random
from operations import pick_two_people

Form, Window = uic.loadUiType("dialog.ui")
appVersion = "0.1 Alpha"
font = QFont()
font.setPointSize(12)

font2 = QFont()
font2.setPointSize(16)
font2.setBold(True)

class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Form()
        self.ui.setupUi(self)
        self.setWindowTitle(f"Adeko Duty Tracker v.{appVersion}")
        self.setWindowIcon(QIcon('adeko.ico'))
        self.ui.actionEmployeeData.triggered.connect(self.open_employee_data)
        self.ui.actionAdd_Absentees.triggered.connect(self.set_availabilities)
        self.ui.actionDuty_Chart.triggered.connect(self.all_time_duty_track)
        self.ui.actionOfftime_Chart.triggered.connect(self.holiday_data)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionAbout_the_program.triggered.connect(self.about)
        self.ui.pushButton.clicked.connect(self.shuffle)
        self.ui.pushButton_2.clicked.connect(self.confirm)
        self.ui.label.setText("Henüz seçilmedi")
        self.ui.label_2.setText("Henüz seçilmedi")
        self.ui.label_3.setText("Henüz seçilmedi")
        self.ui.label_4.setText("Henüz seçilmedi")
        self.ui.label_5.setText("Henüz seçilmedi")
        self.ui.label_6.setText("Henüz seçilmedi")

    def shuffle(self):
        chosen_people = pick_two_people()
        self.label5.setText(chosen_people[0] + " and " + chosen_people[1])

    def open_employee_data(self):
        subprocess.run(["python", "employeedata.py"])

    def set_availabilities(self):
        subprocess.run(["python", "selectunavailable.py"])

    def all_time_duty_track(self):
        subprocess.run(["python", "dutydata.py"])

    def holiday_data(self):
        subprocess.run(["python", "holidaydata.py"])
        

    def confirm(self):
        #calculate the month in format e.g. "June 2024"
        currentMonth = datetime.date.today().strftime("%B %Y")
        # Connect to the database
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # Calculate the date
        date = str(datetime.date.today() + datetime.timedelta((5-datetime.date.today().weekday()) % 7))
        
        # Check if there is a registry on the same date
        cursor.execute('SELECT * FROM dutychart WHERE date = ?', (date,))
        rows = cursor.fetchall()
        
        if rows:
            QMessageBox.warning(self, 'Warning', 'There is already a registry on this date.')
        else:
            cursor.execute('INSERT INTO dutychart (date, firstonduty, secondonduty, month) VALUES (?, ?, ?, ?)', (date, self.label5.text().split(" ve ")[0], self.label5.text().split(" ve ")[1], currentMonth))
            cursor.execute('UPDATE employees SET beenonduty = 1, lastdutydate = ? WHERE name = ?', (date, self.label5.text().split(" ve ")[0]))
            cursor.execute('UPDATE employees SET beenonduty = 1, lastdutydate = ? WHERE name = ?', (date, self.label5.text().split(" ve ")[1]))
            cursor.execute('UPDATE employees SET numberOfHolidays = numberOfHolidays + 1 WHERE name = ?', (self.label5.text().split(" ve ")[0],))
            cursor.execute('UPDATE employees SET numberOfHolidays = numberOfHolidays + 1 WHERE name = ?', (self.label5.text().split(" ve ")[1],))
            conn.commit()
            self.label5.setText("Onaylandı")
        
        conn.close()

    def about(self):
        QMessageBox.about(self, "About Adeko Duty Tracker", "This is a simple duty tracker for Adeko. You can see the employees and their data, set their availabilities, and see the next duty information."  + "\n" + "This software is free to use and open source. It is developed with Python and PyQt6." + "\n" + "This software is not an official software of Adeko. It is developed by an Adeko employee for personal use." + "\n" + "\n" + "Developed by Hakan AK, an ADeko Employee, 2024")


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 300)
        self.setWindowIcon(QIcon('adeko.ico'))

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.appIcon = QLabel()
        self.appIcon.setPixmap(QIcon('adeko.ico').pixmap(100, 100))
        self.layout.addWidget(self.appIcon)

        self.appLabel= QLabel(f"Adeko Duty Tracker v.{appVersion}")
        self.appLabel.setFont(font2)
        self.layout.addWidget(self.appLabel)

        self.loginLabel= QLabel("Please enter your credentials")
        self.loginLabel.setFont(font)
        self.layout.addWidget(self.loginLabel)

        self.username_label = QLabel("Username")
        self.username_label.setFont(font)
        self.layout.addWidget(self.username_label)

        self.username_input = QLineEdit()
        self.layout.addWidget(self.username_input)

        self.password_label = QLabel("Password")
        self.password_label.setFont(font)
        self.layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_credentials)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Connect to the database
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        # Execute a query
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))

        # Fetch all rows from the last executed statement
        rows = cursor.fetchall()

        # Close the connection
        conn.close()

        if rows:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

if __name__ == "__main__":
    app = QApplication([])
    login_dialog = LoginDialog()

    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        main_interface = MainInterface()
        main_interface.show()
        app.exec()