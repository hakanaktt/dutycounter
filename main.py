from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QVBoxLayout,  QLabel, QLineEdit, QMessageBox,  QVBoxLayout
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
import sqlite3, subprocess, datetime
from operations import pickTwoPeople

chosen_people = []

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
        self.setPossiblePeople()

        self.setWindowTitle(f"Adeko Duty Tracker v.{appVersion}")
        self.setWindowIcon(QIcon('adeko.ico'))
        #Menu bar
        self.ui.actionEmployeeData.triggered.connect(self.open_employee_data)
        self.ui.actionAdd_Absentees.triggered.connect(self.set_absentees)
        self.ui.actionDuty_Chart.triggered.connect(self.all_time_duty_track)
        self.ui.actionOfftime_Chart.triggered.connect(self.offtime_data)
        self.ui.actionSettings.triggered.connect(self.settings)
        self.ui.actionAdd_Offtime.triggered.connect(self.add_offtime)
        self.ui.actionYearly_Report.triggered.connect(self.yearly_report)
        self.ui.actionMonthly_Report.triggered.connect(self.monthly_report)
        self.ui.actionCustom_Report.triggered.connect(self.custom_report)
        self.ui.actionLicense.triggered.connect(self.license)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionAbout_the_program.triggered.connect(self.about)

        #Main interface buttons
        self.ui.shuffleSelection.clicked.connect(self.shuffle)
        self.ui.confirmSelection.clicked.connect(self.confirm)

        #Main interface labels
        self.ui.mainLabel.setFont(font2)
        self.ui.mainLabel.setText(f"BuĞ hafta muhtemel nöbetçileri:")
        self.ui.firstPossiblePerson.setFont(font)
        self.ui.secondPossiblePerson.setFont(font)

    #Function that sets the possible people for the duty for the start of the application
    def setPossiblePeople(self):
        chosen_people = pickTwoPeople()
        self.ui.firstPossiblePerson.setText(chosen_people[0])
        self.ui.secondPossiblePerson.setText(chosen_people[1])
        print(chosen_people)
    #Shuffle Button Function
    def shuffle(self):
        chosen_people = pickTwoPeople()
        self.ui.firstPossiblePerson.setText(chosen_people[0])
        self.ui.secondPossiblePerson.setText(chosen_people[1])
        print(chosen_people)
    #Confirm Button Function
    def confirm(self):
        global chosen_people
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO duties (first_person, second_person, date) VALUES (?, ?, ?)", (chosen_people[0], chosen_people[1], datetime.datetime.now()))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "The selection is saved successfully.")

    #Menu bar functions
    def open_employee_data(self):
        subprocess.run(["python", "employeedata.py"])

    def all_time_duty_track(self):
        subprocess.run(["python", "dutydata.py"])

    def offtime_data(self):
        subprocess.run(["python", "offtimedata.py"])

    def settings(self):
        #subprocess.run(["python", "settings.py"])
        QMessageBox.information(self, "Settings", "Settings page is under construction.")

    def add_offtime(self):
        #subprocess.run(["python", "addofftime.py"])
        QMessageBox.information(self, "Add Offtime", "Add Offtime page is under construction.")

    def set_absentees(self):
        subprocess.run(["python", "selectunavailable.py"])

    def yearly_report(self):
        QMessageBox.information(self, "Yearly Report", "Yearly report page is under construction.")

    def monthly_report(self):
        QMessageBox.information(self, "Monthly Report", "Monthly report page is under construction.")
    
    def custom_report(self):
        QMessageBox.information(self, "Custom Report", "Custom report page is under construction.")
    
    def license(self):
        QMessageBox.information(self, "License", "This software is free to use and open source. It is developed with Python and PyQt6. You can use it for free and modify it as you wish. You can not sell it or use it for commercial purposes without the permission of the developer.")
    
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