import json

import pandas as pd
import pyperclip
from PyQt5 import QtCore, QtGui, QtWidgets

from Components import Login, PasswordManager
from Utils.Helpers.HelperFuncs import *
from Utils.routes import *


class Ui_PasswordDashboard(object):
    def __init__(self):
        self.flag = 1
        self.clipFlag = 0

    def copy_data(self):
        if self.tableWidget.selectedItems():
            arr = self.tableWidget.selectedItems()
            clipboard = [a.text() for a in arr]

            if not self.clipFlag:
                pyperclip.copy(clipboard[self.clipFlag])
                self.clipFlag = 1
            else:
                clipboard[1] = decryptPass(clipboard[1])
                pyperclip.copy(clipboard[self.clipFlag])
                self.clipFlag = 0

    def show_table(self):
        user_names = []
        passwords = []

        with open(passManagerDB) as pDB:
            all_passwords = json.load(pDB)
        currUser = all_passwords["current_user"]
        this_user_passwords = all_passwords[currUser]
        df = pd.DataFrame.from_dict(this_user_passwords, orient='index')

        for index, row in df.iterrows():
            for col in df.columns:
                if not pd.isnull(row[col]):
                    passwords.append(row[col])
        for col in df.columns:
            user_names.append(col)

        # set the amout of rows and cols
        self.tableWidget.setRowCount(len(this_user_passwords))
        self.tableWidget.setColumnCount(2)

        # Fill the Headers rows and cols in the Table
        self.tableWidget.setHorizontalHeaderLabels(['User name', 'Encrypted Password'])
        self.tableWidget.setVerticalHeaderLabels(str(rowName) for rowName in df.index)

        for rows in range(len(this_user_passwords)):
            self.tableWidget.setItem(rows, 0, QtWidgets.QTableWidgetItem(user_names[rows]))

        for rows in range(len(passwords)):
            self.tableWidget.setItem(rows, 1, QtWidgets.QTableWidgetItem(passwords[rows]))

    def enc_dec_password(self):
        passwords = []
        with open(passManagerDB) as pDB:
            all_passwords = json.load(pDB)
        currUser = all_passwords["current_user"]
        this_user_passwords = all_passwords[currUser]
        df = pd.DataFrame.from_dict(this_user_passwords, orient='index')

        for index, row in df.iterrows():
            for col in df.columns:
                if not pd.isnull(row[col]):
                    passwords.append(row[col])

        if self.tableWidget.selectedItems():
            if self.flag:
                if self.tableWidget.currentItem().text() in passwords:
                    dec_pass = decryptPass(self.tableWidget.currentItem().text())
                    self.tableWidget.setItem(self.tableWidget.currentRow(), 1, QtWidgets.QTableWidgetItem(dec_pass))
                    self.flag = 0
            else:
                if self.tableWidget.currentColumn() == 1:
                    enc_pass = encryptPass(self.tableWidget.currentItem().text())
                    self.tableWidget.setItem(self.tableWidget.currentRow(), 1, QtWidgets.QTableWidgetItem(enc_pass))
                    self.flag = 1

    def delete_password(self):
        if self.tableWidget.rowCount() > 0 and self.tableWidget.selectedItems():
            row = self.tableWidget.currentRow()
            label = self.tableWidget.verticalHeaderItem(row).text()

            with open(passManagerDB) as pDB:
                all_passwords = json.load(pDB)

            currUser = all_passwords["current_user"]
            this_user_passwords = all_passwords[currUser]
            del this_user_passwords[label]
            all_passwords[currUser] = this_user_passwords

            with open(passManagerDB, "w") as pDB:
                json.dump(all_passwords, pDB, indent=2)

            self.tableWidget.removeRow(self.tableWidget.currentRow())

    def open_login(self, PasswordDashboard):
        self.Login = QtWidgets.QMainWindow()
        self.ui = Login.Ui_LogIn()
        self.ui.setupUi(self.Login)
        self.Login.show()
        PasswordDashboard.close()

    def open_pass_manager(self, PasswordDashboard):
        self.passManager = QtWidgets.QMainWindow()
        self.ui = PasswordManager.Ui_PasswordManager()
        self.ui.setupUi(self.passManager)
        self.passManager.show()
        PasswordDashboard.close()

    def setupUi(self, PasswordDashboard):
        PasswordDashboard.setObjectName("PasswordDashboard")
        PasswordDashboard.setWindowIcon(QtGui.QIcon(logo))
        PasswordDashboard.setWindowTitle("Password Dashboard")
        PasswordDashboard.resize(649, 564)

        # --------------- Buttons -------------

        self.encDec = QtWidgets.QPushButton(PasswordDashboard)
        self.encDec.setText("Encrypt - Decrypt")
        self.encDec.setGeometry(QtCore.QRect(10, 520, 141, 28))
        self.encDec.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.encDec.setDefault(False)
        self.encDec.setObjectName("encDec")
        self.encDec.clicked.connect(self.enc_dec_password)

        self.addNewBtn = QtWidgets.QPushButton(PasswordDashboard)
        self.addNewBtn.setGeometry(QtCore.QRect(160, 520, 93, 28))
        self.addNewBtn.setObjectName("addNewBtn")
        self.addNewBtn.setText("Add New")
        self.addNewBtn.clicked.connect(lambda: self.open_pass_manager(PasswordDashboard))

        self.copyBtn = QtWidgets.QPushButton(PasswordDashboard)
        self.copyBtn.setGeometry(QtCore.QRect(260, 520, 93, 28))
        self.copyBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.copyBtn.setDefault(False)
        self.copyBtn.setObjectName("copyBtn")
        self.copyBtn.setText("Copy")
        self.copyBtn.clicked.connect(self.copy_data)

        self.deleteBtn = QtWidgets.QPushButton(PasswordDashboard)
        self.deleteBtn.setGeometry(QtCore.QRect(370, 520, 93, 28))
        self.deleteBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.deleteBtn.setDefault(False)
        self.deleteBtn.setObjectName("deleteBtn")
        self.deleteBtn.setText("Delete")
        self.deleteBtn.setStyleSheet("QPushButton::hover{background-color : #ffa4a4;}")
        self.deleteBtn.clicked.connect(self.delete_password)

        self.exitBtn = QtWidgets.QPushButton(PasswordDashboard)
        self.exitBtn.setText("Exit")
        self.exitBtn.setGeometry(QtCore.QRect(550, 520, 93, 28))
        self.exitBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exitBtn.setAutoFillBackground(False)
        self.exitBtn.setObjectName("exitBtn")
        self.exitBtn.clicked.connect(lambda: self.open_login(PasswordDashboard))

        # ---------- Table View ---------------
        self.tableWidget = QtWidgets.QTableWidget(PasswordDashboard)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 631, 501))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        # ------ with start funcs ----
        self.show_table()

        QtCore.QMetaObject.connectSlotsByName(PasswordDashboard)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    PasswordDashboard = QtWidgets.QWidget()
    ui = Ui_PasswordDashboard()
    ui.setupUi(PasswordDashboard)
    PasswordDashboard.show()
    sys.exit(app.exec_())
