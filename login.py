import sys
from PyQt5 import QtWidgets
import sqlite3 as sql

class Pencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.baglanti_olustur()

    def baglanti_olustur(self):
        conn = sql.connect("database.db")
        self.cursor = conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Uyeler (kullanici_adi TEXT,parola TEXT)")
        conn.commit()

    def init_ui(self):
        self.kullanici_adi = QtWidgets.QLineEdit()
        self.parola = QtWidgets.QLineEdit()
        self.parola.setEchoMode(QtWidgets.QLineEdit.Password)
        self.giris = QtWidgets.QPushButton("Giriş Yap")
        self.kayit = QtWidgets.QPushButton("Kayıt Ol")
        self.yazi_alani = QtWidgets.QLabel("")

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(QtWidgets.QLabel("Kullanıcı Adı:"))
        v_box.addWidget(self.kullanici_adi)
        v_box.addWidget(QtWidgets.QLabel("Parola:"))
        v_box.addWidget(self.parola)
        v_box.addWidget(self.yazi_alani)
        v_box.addWidget(self.giris)
        v_box.addWidget(self.kayit)
        v_box.addStretch()

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()

        self.setLayout(h_box)
        self.setWindowTitle("Kullanıcı Girişi")
        self.setFixedSize(300, 250)
        self.giris.clicked.connect(self.login)
        self.kayit.clicked.connect(self.register)
        self.giris.clicked.connect(self.click)
        self.kayit.clicked.connect(self.click)
        self.show()

    def login(self):
        adi = self.kullanici_adi.text()
        par = self.parola.text()
        self.cursor.execute("SELECT * FROM Uyeler WHERE kullanici_adi = ? and parola = ?",(adi,par))
        data = self.cursor.fetchall()
        
        if len(data) == 0:
            self.yazi_alani.setText("Boyle bir kullanici yok\nLutfen tekrar deneyiniz")
        else:
            self.yazi_alani.setText("Hosgeldiniz, " + adi + " !")

    def register(self):
        conn = sql.connect("database.db")
        self.cursor = conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Uyeler (kullanici_adi TEXT,parola TEXT)")
        adi = self.kullanici_adi.text()
        par = self.parola.text()
        self.cursor.execute("INSERT INTO Uyeler VALUES (?,?)",(adi,par))
        conn.commit()
        self.yazi_alani.setText("Kayıt oluşturuldu, giriş yapınız...")

    def click(self):
        sender = self.sender()

        if sender.text() == "Giriş Yap":
            self.kullanici_adi.clear()
            self.parola.clear()
        elif sender.text() == "Kayıt Ol":
            self.kullanici_adi.clear()
            self.parola.clear()

app = QtWidgets.QApplication(sys.argv)
pencere = Pencere()
sys.exit(app.exec_())