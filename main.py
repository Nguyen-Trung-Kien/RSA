import numpy as np
import math
import sys
import random
from PyQt5.QtWidgets import *
from qt_material import apply_stylesheet
from PyQt5.uic import loadUiType
import threading

ui, _ = loadUiType('main.ui')
class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Button()

    flag = 0
    public_key = 0
    private_key = 0
    def Handle_Button(self):
        self.btn1.clicked.connect(self.thread_getinfo)
        self.btn2.clicked.connect(self.thread_crip)
        self.btn3.clicked.connect(self.thread_clear)
    def is_prime(self, number):
        count = 0
        if number == 2:
            return True
        if number < 2:
            return False
        if number % 2 == 0:
            return False
        for i in range(1, number + 1):
            if number % i == 0:
                count += 1
        if count == 2:
            return True
        return False

    def random_e(self, phi):
        e = random.randrange(1, phi)
        g = np.gcd(e, phi)
        while g != 1:
            e = random.randrange(1, phi)
            g = np.gcd(e, phi)
        return e

    def inverse_d(self, e, phi):
        # phi_x +e_y = 1
        r1 = phi
        r2 = e
        t1 = 0
        t2 = 1
        while r2 > 0:
            q = r1 // r2
            r = r1 - q * r2
            t = t1 - t2 * q
            r1 = r2
            r2 = r
            t1 = t2
            t2 = t
        d = t1
        print("d1 = " + str(d))
        if d < 0:
            d = t2 + t1
            print("d2 = " + str(d))
        if r1 == 1 or d == e:
            d = d + phi
            print("d3 = " + str(d))
        return d

    def generate_key(self, p, q):
        n = p * q  # calc n
        phi_n = (p - 1) * (q - 1)  # calc phi
        e = self.random_e(phi_n)  # find e
        d = self.inverse_d(e, phi_n)
        return ((e, n), (d, n))

    def encrypt(self, pk, messager):
        public_key, n = pk
        Cipher = []
        # C = M^e mod n
        for char in messager:
            a = pow(ord(char), public_key, n)
            Cipher.append(a)
        return Cipher

    def decryption(self,pk, ciphertext):
        private_key, n = pk
        # M = C^d mod n
        plain_text = []

        temp = []
        for char in ciphertext:
            a = str(pow(char, private_key, n))
            temp.append(a)
        self.landing.appendPlainText("ablo: " + str(temp))
        for char2 in temp:
            a = chr(int(char2))
            plain_text.append(a)
        return ''.join(plain_text)
    def thread_crip(self):
        t = threading.Thread(target=self.crip)
        t.start()
    def thread_getinfo(self):
        t = threading.Thread(target=self.getinfo)
        t.start()
    def thread_clear(self):
        t = threading.Thread(target=self.clear)
        t.start()

    def getinfo(self):
        p = self.inputP.text()
        q = self.InputQ.text()
        print(p)
        print(q)
        if p.isdigit()!= True or q.isdigit() !=True:
            QMessageBox.warning(self,"Canh bao","Hay nhap la so")
        elif p == q:
            QMessageBox.warning(self,"Canh bao","p va q khong duoc trung nhau")
        elif self.is_prime(int(p))!= True or self.is_prime(int(q))!=True:
            QMessageBox.warning(self, "Canh bao", "Hay nhap so nguyen to")
        else:
            p = int(p)
            q = int(q)
            self.public_key, self.private_key = self.generate_key(p, q)
            self.landing.appendPlainText("Values of p: " + str(p))
            self.landing.appendPlainText("Values of q: " + str(q))
            self.landing.appendPlainText("....................... ")
            self.landing.appendPlainText("wait....")
            self.landing.appendPlainText("generate_key....")
            self.landing.appendPlainText("Public Key: " + str(self.public_key))
            self.landing.appendPlainText("Private Key: " + str(self.private_key))
            self.flag =1

    def clear(self):
        self.landing.clear()


    def crip(self):
        msg = self.InputMsg.text()
        if self.flag == 0:
            QMessageBox.warning(self, "Canh bao", "Hay nhap p va q")
        elif msg == '':
            QMessageBox.warning(self,"Cảnh báo", "Hãy nhập thông điệp cần mã hoá!")
        else:
            self.landing.appendPlainText("Thông Điệp đang được mã hoá!")
            self.landing.appendPlainText("Wait......")
            encrypt = self.encrypt(self.public_key,msg)
            decrypt = self.decryption(self.private_key,encrypt)

            self.landing.appendPlainText("Thông điệp sau khi được mã hoá là: " + ''.join(map(lambda x: str(x), encrypt)))
            self.landing.appendPlainText("Tiến hành Giải mã thông điệp")
            self.landing.appendPlainText("Wait......")
            self.landing.appendPlainText("Thông điệp sau khi được mã hoá là: " + decrypt)




# Press the green button in the gutter to run the script.


def main():
    app = QApplication(sys.argv)
    windows = MainApp()
    apply_stylesheet(app, theme='dark_blue.xml')
    windows.show()
    app.exec()


if __name__ == '__main__':
    main()

