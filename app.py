
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QDialog, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView,  QTabWidget, QVBoxLayout
from PyQt6.QtGui import QIcon, QAction, QFont
from PyQt6.QtCore import Qt
import sqlite3, subprocess, sys, datetime, random
from operations import pick_two_people

font = QFont()
font.setPointSize(12)

font2 = QFont()
font2.setPointSize(16)
font2.setBold(True)

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

        breakpoint = QLabel("\n" + "\n")
        self.layout.addWidget(breakpoint)


        #possible people who will be on duty next saturday
        self.label4 = QLabel("Bir sonraki cumartesi nöbette olabilecekler: ")
        self.label4.setFont(font)
        self.layout.addWidget(self.label4)

        chosen_people = pick_two_people()

        self.label5 = QLabel(chosen_people[0] + " and " + chosen_people[1])
        self.label5.setFont(font)
        self.layout.addWidget(self.label5)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        self.layout.setContentsMargins(20, 20, 0, 0)

        self.shuffleAgain = QPushButton("Yeniden karıştır")
        self.shuffleAgain.setFixedWidth(100)
        self.shuffleAgain.setFixedHeight(30)
        self.shuffleAgain.clicked.connect(self.shuffle)
        button_layout.addWidget(self.shuffleAgain)

        self.confirmChoice = QPushButton("Onayla")
        self.confirmChoice.setFixedWidth(100)
        self.confirmChoice.setFixedHeight(30)
        self.confirmChoice.clicked.connect(self.confirm)
        button_layout.addWidget(self.confirmChoice)

        self.layout.addLayout(button_layout)

    # Set up the menu bar
        menubar = self.menuBar()
        data_menu = menubar.addMenu('Data')

        open_action = QAction('See Employee Data', self)
        open_action.triggered.connect(self.open_employee_data)
        data_menu.addAction(open_action)

        open_action = QAction('Duty Chart', self)
        open_action.triggered.connect(self.all_time_duty_track)
        data_menu.addAction(open_action)

        open_action = QAction('Holiday Data', self)
        open_action.triggered.connect(self.holiday_data)
        data_menu.addAction(open_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        data_menu.addAction(exit_action)

        action_menu = menubar.addMenu('Actions')

        open_action = QAction('Set Availabilities', self)
        open_action.triggered.connect(self.set_availabilities)
        action_menu.addAction(open_action)

        open_action = QAction('Add Offtime', self)
        open_action.triggered.connect(self.add_offtime)
        action_menu.addAction(open_action)

        about_menu = menubar.addMenu('About')

        about_action = QAction('About', self)
        about_action.triggered.connect(self.about)
        about_menu.addAction(about_action)

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
    
    def add_offtime(self):
        subprocess.run(["python", "addofftime.py"])

    def confirm(self):
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
            cursor.execute('INSERT INTO dutychart (date, firstonduty, secondonduty) VALUES (?, ?, ?)', (date, self.label5.text().split(" and ")[0], self.label5.text().split(" and ")[1]))
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

        self.appLabel= QLabel("Adeko Duty Tracker v.0.1")
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