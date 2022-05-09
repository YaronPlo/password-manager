import json

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtTest import QTest

from Components import PasswordDash
from Utils.Helpers.HelperFuncs import *
from Utils.routes import *


class Ui_LogIn(object):
    def create_user_section_in_pManager(self):
        with open(passManagerDB) as pDB:
            data = json.load(pDB)
        data[self.uNameInput.text()] = {}
        with open(passManagerDB, "w") as pDB:
            json.dump(data, pDB, indent=2)

    def check_user(self):
        uName = self.uNameInput.text()
        password = self.passwordInput.text()

        with open(usersDB, "r") as DB:
            allUsers = json.load(DB)

        try:
            if uName == "" or password == "":
                self.message.setPlainText("Blank Input Try Again!")
                self.message.setStyleSheet("color: red")
                QTest.qWait(1500)
                self.message.setPlainText("")
                return False

            if allUsers[uName]:
                # Decode Password
                decoded_password = decryptPass(allUsers[uName].encode("ascii"))
                if decoded_password == password:
                    return True

                else:
                    self.uNameInput.clear()
                    self.passwordInput.clear()
                    self.message.setPlainText("Wrong Password!")
                    self.message.setStyleSheet("color: red")
                    QTest.qWait(1500)
                    self.message.setPlainText("")
                    return False
        except:
            self.uNameInput.clear()
            self.passwordInput.clear()
            self.message.setPlainText("User Doesn't Exist!")
            self.message.setStyleSheet("color: red")
            QTest.qWait(1500)
            self.message.setPlainText("")
            return False

    def check_master(self):
        uName = self.uNameInput.text()
        password = self.passwordInput.text()

        with open(usersDB, "r") as DB:
            allUsers = json.load(DB)

        try:
            if uName == "" or password == "":
                self.message.setPlainText("Blank Input Try Again!")
                self.message.setStyleSheet("color: red")
                QTest.qWait(1500)
                self.message.setPlainText("")
                return True

            if allUsers[uName]:
                self.uNameInput.clear()
                self.passwordInput.clear()
                self.message.setPlainText("User Allready Exists!")
                self.message.setStyleSheet("color: red")
                QTest.qWait(1500)
                self.message.setPlainText("")
                return True
        except:
            return False

    def create_master_password(self):
        check = self.check_master()
        uName = self.uNameInput.text()

        if not check:
            if check_password(self.passwordInput.text(), self.message, "Master password sucessfully created",
                              "Password not strong Enough!"):
                # Encode Password
                password = self.passwordInput.text()
                base64_password = encryptPass(password)

                with open(usersDB) as uDB:
                    allUsers = json.load(uDB)
                allUsers[uName] = base64_password
                with open(usersDB, "w") as uDB:
                    json.dump(allUsers, uDB, indent=2)

                self.create_user_section_in_pManager()

    def show_password(self):
        if self.showPassCheckbox.isChecked():
            self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)

    def open_password_dashboard(self, LogIn):

        check = self.check_user()
        if check:
            with open(passManagerDB) as pDB:
                currUser = json.load(pDB)
            currUser["current_user"] = self.uNameInput.text()
            with open(passManagerDB, "w") as pDB:
                json.dump(currUser, pDB, indent=2)

            self.passwordDash = QtWidgets.QMainWindow()
            self.ui = PasswordDash.Ui_PasswordDashboard()
            self.ui.setupUi(self.passwordDash)
            self.passwordDash.show()
            LogIn.close()

    def setupUi(self, LogIn):
        LogIn.setObjectName("LogIn")
        LogIn.resize(302, 260)
        LogIn.setWindowIcon(QtGui.QIcon(logo))
        LogIn.setWindowTitle("Log In")
        LogIn.setMouseTracking(False)
        LogIn.setAcceptDrops(False)

        # ---------------- Buttons ---------------
        self.logInBtn = QtWidgets.QPushButton(LogIn)
        self.logInBtn.setText("Log In")
        self.logInBtn.setGeometry(QtCore.QRect(110, 130, 93, 28))
        self.logInBtn.setObjectName("logIn")
        self.logInBtn.clicked.connect(lambda: self.open_password_dashboard(LogIn))

        self.masterPassGenBtn = QtWidgets.QPushButton(LogIn)
        self.masterPassGenBtn.setText("Generate Master Password")
        self.masterPassGenBtn.setGeometry(QtCore.QRect(40, 180, 221, 28))
        self.masterPassGenBtn.setObjectName("passwordGenerator")
        self.masterPassGenBtn.clicked.connect(self.create_master_password)

        self.showPassCheckbox = QtWidgets.QCheckBox(LogIn)
        self.showPassCheckbox.setText("Show password")
        self.showPassCheckbox.setGeometry(QtCore.QRect(120, 100, 141, 20))
        self.showPassCheckbox.setObjectName("showPasswordBtn")
        self.showPassCheckbox.clicked.connect(self.show_password)

        # ------------ Inputs ----------------------
        self.uNameInput = QtWidgets.QLineEdit(LogIn)
        self.uNameInput.setGeometry(QtCore.QRect(120, 30, 141, 22))
        self.uNameInput.setFrame(False)
        self.uNameInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.uNameInput.setDragEnabled(False)
        self.uNameInput.setClearButtonEnabled(True)
        self.uNameInput.setObjectName("userNameInput")

        self.passwordInput = QtWidgets.QLineEdit(LogIn)
        self.passwordInput.setGeometry(QtCore.QRect(120, 70, 141, 22))
        self.passwordInput.setFrame(False)
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordInput.setClearButtonEnabled(True)
        self.passwordInput.setObjectName("passwordInput")

        # ---------- Lables -------------------------
        self.uNameLbl = QtWidgets.QLabel(LogIn)
        self.uNameLbl.setText("User Name:")
        self.uNameLbl.setGeometry(QtCore.QRect(30, 30, 91, 20))
        self.uNameLbl.setObjectName("userNameLbl")

        self.passwordLbl = QtWidgets.QLabel(LogIn)
        self.passwordLbl.setText("Password:")
        self.passwordLbl.setGeometry(QtCore.QRect(30, 70, 81, 20))
        self.passwordLbl.setObjectName("passwordLbl")

        self.message = QtWidgets.QPlainTextEdit(LogIn)
        self.message.setEnabled(False)
        self.message.setGeometry(QtCore.QRect(40, 220, 221, 31))
        self.message.setFocusPolicy(QtCore.Qt.NoFocus)
        self.message.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        self.message.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.message.setFrameShadow(QtWidgets.QFrame.Raised)
        self.message.setObjectName("plainTextEdit")

        QtCore.QMetaObject.connectSlotsByName(LogIn)


def run_login():
    LogInWidget = QtWidgets.QWidget()
    login = Ui_LogIn()  # login Object
    login.setupUi(LogInWidget)
    LogInWidget.show()
