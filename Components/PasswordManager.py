import json
import secrets
import string

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtTest import QTest

from Components import PasswordDash
from Utils.Helpers.HelperFuncs import *
from Utils.routes import *


class Ui_PasswordManager(object):
    def generate_password(self):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        while True:
            password = ''.join(secrets.choice(alphabet) for _ in range(8))
            if (any(c.islower() for c in password) and any(c.isupper() for c in password) and any(
                    c.isdigit() for c in password) and any(c in string.punctuation for c in password)):
                break

        self.passwordInput.setText(password)
        self.message.setPlainText(f"Password Successfully Generated.")
        self.message.setStyleSheet("color: green")
        QTest.qWait(1500)
        self.message.setPlainText("")

    def add_new_service(self):
        with open(passManagerDB) as pDB:
            all_passwords = json.load(pDB)
        try:
            currUser = all_passwords["current_user"]
            if all_passwords[currUser][self.nameOfServiceInput.text()]:
                if check_password(self.passwordInput.text(), self.message, "Service Updated!",
                                  "Bad Password!"):
                    all_passwords[currUser][self.nameOfServiceInput.text()][
                        self.userNameInput.text()] = encryptPass(
                        self.passwordInput.text())
                    with open(passManagerDB, "w") as pDB:
                        json.dump(all_passwords, pDB, indent=2)

        except Exception as e:
            if check_password(self.passwordInput.text(), self.message, "Service Created!",
                              "Bad Password!"):
                all_passwords[currUser][self.nameOfServiceInput.text()] = {
                    self.userNameInput.text(): encryptPass(self.passwordInput.text())}

                with open(passManagerDB, "w") as pDB:
                    json.dump(all_passwords, pDB, indent=2)
        finally:
            self.userNameInput.clear()
            self.passwordInput.clear()
            self.nameOfServiceInput.clear()

    def open_password_dashboard(self, PasswordManager):
        self.passwordDash = QtWidgets.QMainWindow()
        self.ui = PasswordDash.Ui_PasswordDashboard()
        self.ui.setupUi(self.passwordDash)
        self.passwordDash.show()
        PasswordManager.close()

    def setupUi(self, PasswordManager):
        PasswordManager.setObjectName("PasswordManager")
        PasswordManager.resize(308, 279)
        PasswordManager.setWindowIcon(QtGui.QIcon(logo))
        PasswordManager.setWindowTitle("Manager")
        PasswordManager.setMouseTracking(False)
        PasswordManager.setAcceptDrops(False)

        # ------------ Input Lines ------------
        self.nameOfServiceInput = QtWidgets.QLineEdit(PasswordManager)
        self.nameOfServiceInput.setGeometry(QtCore.QRect(22, 30, 271, 22))
        self.nameOfServiceInput.setClearButtonEnabled(True)
        self.nameOfServiceInput.setObjectName("nameOfServiceInput")

        self.userNameInput = QtWidgets.QLineEdit(PasswordManager)
        self.userNameInput.setGeometry(QtCore.QRect(20, 80, 271, 22))
        self.userNameInput.setClearButtonEnabled(True)
        self.userNameInput.setObjectName("userNameInput")

        self.passwordInput = QtWidgets.QLineEdit(PasswordManager)
        self.passwordInput.setGeometry(QtCore.QRect(20, 130, 271, 22))
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordInput.setClearButtonEnabled(True)
        self.passwordInput.setObjectName("passwordInput")
        # -------------- Buttons ---------------
        self.manualyGenPass = QtWidgets.QPushButton(PasswordManager)
        self.manualyGenPass.setText("Generate")
        self.manualyGenPass.setGeometry(QtCore.QRect(20, 160, 121, 28))
        self.manualyGenPass.setObjectName("Add")
        self.manualyGenPass.clicked.connect(self.add_new_service)

        self.autoGenPass = QtWidgets.QPushButton(PasswordManager)
        self.autoGenPass.setText("Automatically Generate strong password")
        self.autoGenPass.setGeometry(QtCore.QRect(20, 200, 271, 28))
        self.autoGenPass.setObjectName("autoGenPass")
        self.autoGenPass.clicked.connect(self.generate_password)

        self.closeBtn = QtWidgets.QPushButton(PasswordManager)
        self.closeBtn.setText("Close")
        self.closeBtn.setGeometry(QtCore.QRect(170, 160, 121, 28))
        self.closeBtn.setObjectName("closeBtn")
        self.closeBtn.clicked.connect(lambda: self.open_password_dashboard(PasswordManager))

        # -----------Message Box --------------
        self.message = QtWidgets.QPlainTextEdit(PasswordManager)
        self.message.setEnabled(False)
        self.message.setGeometry(QtCore.QRect(20, 240, 271, 31))
        self.message.setFocusPolicy(QtCore.Qt.NoFocus)
        self.message.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        self.message.setObjectName("registerMsg")

        # ----------- Labels ------------------
        self.userNameLbl = QtWidgets.QLabel(PasswordManager)
        self.userNameLbl.setText("User Name:")
        self.userNameLbl.setGeometry(QtCore.QRect(20, 60, 81, 20))
        self.userNameLbl.setObjectName("userNameLbl")

        self.passwordLbl = QtWidgets.QLabel(PasswordManager)
        self.passwordLbl.setText("Password:")
        self.passwordLbl.setGeometry(QtCore.QRect(20, 110, 81, 20))
        self.passwordLbl.setObjectName("passwordLbl")

        self.nameOfServiceLbl = QtWidgets.QLabel(PasswordManager)
        self.nameOfServiceLbl.setText("Name of Service:")
        self.nameOfServiceLbl.setGeometry(QtCore.QRect(20, 10, 111, 20))
        self.nameOfServiceLbl.setObjectName("nameOfServiceLbl")

        QtCore.QMetaObject.connectSlotsByName(PasswordManager)
