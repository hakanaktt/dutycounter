from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QVBoxLayout,  QLabel, QLineEdit, QMessageBox,  QVBoxLayout
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
import sqlite3, subprocess, datetime, sys, os
from ops import pickDutyDuo, setAvailableGroup, findNextSaturday, checkNextDutyData, bringNextDutyData, setDutyData, dutyCountInSelectedYear, timeLeftUntilNextDuty
global chosenDuo

Form, Window = uic.loadUiType("md.ui")
appVersion = "0.2 Beta"
fontLarge = QFont()
fontLarge.setPointSize(16)
fontLarge.setBold(True)

fontMid = QFont()
fontMid.setPointSize(12)
fontMid.setBold(True)

fontSmall = QFont()
fontSmall.setPointSize(10)
fontSmall.setBold(False)

class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Form()
        self.ui.setupUi(self)
        self.chosenDuo = None
        self.setStatus()

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
        self.ui.actionExit.triggered.connect(self.exitProgram)
        self.ui.actionAbout_the_program.triggered.connect(self.about)

        #Main interface buttons
        self.ui.shuffleSelection.clicked.connect(self.shuffle)
        self.ui.confirmSelection.clicked.connect(self.confirm)

        #Main interface labels
        self.ui.mainLabel.setFont(fontMid)
        self.ui.availablePeopleLabel.setFont(fontMid)
        self.ui.availablePeopleLabel.setText(f"{findNextSaturday()[0]} Cumartesi müsait kişiler:")
        self.ui.possibleCandidates.setFont(fontMid)
        self.ui.statisticsLabel.setFont(fontMid)
        self.ui.statisticsText.setFont(fontSmall)
        self.ui.timeleft.setFont(fontMid)

    #Function that sets the possible people for the duty for the start of the application
    def setPossiblePeople(self):
        chosenDuo = pickDutyDuo()
        self.ui.possibleCandidates.setText(f"{chosenDuo[0]} ve {chosenDuo[1]}")

    def showAvailablePeople(self):
        availablePeople = setAvailableGroup()
        availablePeopleList = ""

        for member in availablePeople:
            availablePeopleList += member + "\n"
        self.ui.availablePeopleList.setText(availablePeopleList)

    def showStatistics(self):
        
        self.ui.statisticsLabel.setText(f"{findNextSaturday()[2]} yılı nöbet sayıları:")
        duty_dict = dutyCountInSelectedYear(2024)
        duty_str = "\n".join(f"{key}: {value}" for key, value in duty_dict.items())
        self.ui.statisticsText.setText(duty_str)

    #Shuffle Button Function
    def shuffle(self):
        print("Shuffle button clicked")
        self.chosenDuo = pickDutyDuo()
        self.ui.firstPossiblePerson.setText(chosenDuo[0])
        self.ui.secondPossiblePerson.setText(chosenDuo[1])
    #Confirm Button Function
    def confirm(self):
        setDutyData(self.chosenDuo[0], self.chosenDuo[1])
        self.ui.shuffleSelection.setEnabled(False)
        self.ui.confirmSelection.setEnabled(False)        
        QMessageBox.information(self, "Success", "The selection is saved successfully.")

    def setStatus(self):
        self.showAvailablePeople()
        self.showStatistics()
        self.ui.timeleft.setText(f"Bir sonraki nöbet: {findNextSaturday()[0]} \n {timeLeftUntilNextDuty()} sonra nöbetimiz var.")
        if checkNextDutyData():
            self.ui.mainLabel.setText(f"{findNextSaturday()[0]} Cumartesi günü nöbetçileri belirlendi:")
            nextDutyData = bringNextDutyData()
            self.ui.possibleCandidates.setText(f"{nextDutyData[0][2]} ve {nextDutyData[0][3]}")
            self.ui.shuffleSelection.setEnabled(False)
            self.ui.confirmSelection.setEnabled(False)
        else:
            self.ui.mainLabel.setText(f"{findNextSaturday()[0]} Cumartesi günü muhtemel nöbetçileri:")
            self.chosenDuo = pickDutyDuo()
            self.ui.possibleCandidates.setText(f"{self.chosenDuo[0]} ve {self.chosenDuo[1]}")
            self.ui.shuffleSelection.setEnabled(True)
            self.ui.confirmSelection.setEnabled(True)

    #Menu bar functions
    def open_employee_data(self):
        #subprocess.run(["python", "ed.py"])
        os.system("ed.exe")

    def all_time_duty_track(self):
        #subprocess.run(["python", "dd.py"])
        os.system("dd.exe")

    def offtime_data(self):
        #subprocess.run(["python", "otd.py"])
        os.system("otd.exe")

    def settings(self):
        #subprocess.run(["python", "settings.py"])
        QMessageBox.information(self, "Settings", "Settings page is under construction.")

    def add_offtime(self):
        #subprocess.run(["python", "addofftime.py"])
        QMessageBox.information(self, "Add Offtime", "Add Offtime page is under construction.")

    def set_absentees(self):
        #subprocess.run(["python", "su.py"])
        os.system("su.exe")

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

    def exitProgram(self):
        self.close()



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
        self.appLabel.setFont(fontMid)
        self.layout.addWidget(self.appLabel)

        self.loginLabel= QLabel("Lütfen giriş yapın:")
        self.loginLabel.setFont(fontSmall)
        self.layout.addWidget(self.loginLabel)

        self.username_label = QLabel("Kullanıcı Adı")
        self.username_label.setFont(fontSmall)
        self.layout.addWidget(self.username_label)

        self.username_input = QLineEdit()
        self.layout.addWidget(self.username_input)

        self.password_label = QLabel("Parola")
        self.password_label.setFont(fontSmall)
        self.layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.check_credentials)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Connect to the database
        conn = sqlite3.connect('db.db')
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
            QMessageBox.warning(self, "Error", "Geçersiz kullanıcı adı veya parola. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    app = QApplication([])
    login_dialog = LoginDialog()

    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        main_interface = MainInterface()
        main_interface.show()
        app.exec()
                             