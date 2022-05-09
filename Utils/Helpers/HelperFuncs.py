import base64
import re

from PyQt5.QtTest import QTest

__all__ = ["encryptPass", "decryptPass", "check_password"]


def encryptPass(password):
    passAscii = password.encode("ascii")
    base64_bytes = base64.b64encode(passAscii)
    return base64_bytes.decode("ascii")


def decryptPass(password):
    password_bytes = base64.b64decode(password)
    return password_bytes.decode("ascii")


def check_password(password, messageBox, messageSuc, messageFail):
    regex = ("^(?=.*[a-z])(?=." + "*[A-Z])(?=.*\\d)" + "(?=.*[-+_!@#$%^&*;:\" \\./'<>{}`=|~, ?]).+$")
    p = re.compile(regex)
    if re.search(p, password) and len(password) == 8:
        messageBox.setPlainText(f"{messageSuc}")
        messageBox.setStyleSheet("color: green")
        QTest.qWait(1500)
        messageBox.setPlainText("")
        return True
    else:
        messageBox.setPlainText(f"{messageFail}")
        messageBox.setStyleSheet("color: red")
        QTest.qWait(1500)
        messageBox.setPlainText("")
        return False
