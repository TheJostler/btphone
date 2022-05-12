# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QDialog, QLabel)
from PySide6.QtGui import QIcon
import argparse
import subprocess

version = "1.1"

class Scan(QDialog):
    def __init__(self, parent=None):
        super(Scan, self).__init__(parent)

        self.setWindowTitle("Btphone")
        self.setWindowIcon(QIcon("res/SplashV" + version + ".png"))

        #Left Pane
        leftPane = QVBoxLayout( self )
        leftPane.setSpacing(5)
        LP_row0 = QHBoxLayout()
        LP_row1 = QHBoxLayout()
        LP_row2 = QHBoxLayout()
        LP_row3 = QHBoxLayout()

        #Left Pane Stuff
        self.street = QLineEdit()
        self.area = QLineEdit()
        self.go = QPushButton("GO")

        #Labels
        labStreet = QLabel("Street Name:")
        labArea = QLabel("Area/Postcode:")

        #LP_row0
        Title = QLabel("BTPhone version " + version + " By Josjuar Lister 2021-2022")
        LP_row0.addWidget(Title)

        #LP_row1
        LP_row1.addWidget(labStreet)
        LP_row1.addWidget(self.street)

        #LP_row2
        LP_row2.addWidget(labArea)
        LP_row2.addWidget(self.area)

        #LP_row3
        LP_row3.addWidget(self.go)

        #Finalize Left Pane
        leftPane.addLayout(LP_row0)
        leftPane.addLayout(LP_row1)
        leftPane.addLayout(LP_row2)
        leftPane.addLayout(LP_row3)

        #Right Pane
        rightPane = QVBoxLayout( self )
        rightPane.setSpacing(5)

        ##Left Pane Stuff goes here!

        #Finalize Left Pane
        #leftPane.adLayout()

        self.setLayout(leftPane)
        self.setLayout(rightPane)
        self.go.clicked.connect(self.start)

    def start(self):

        wordlist = "res/aa_zz.txt"
        output = self.street.text() + ".html"
        print("street: " + self.street.text())
        print("area: " + self.area.text())
        btphone = subprocess.Popen(["python3", "res/btphone.py", "-w", wordlist, "-s", self.street.text(), "-a", self.area.text(), "-o", output], shell=False)

if __name__ == "__main__":
    try:
        import pyi_splash
        pyi_splash.update_text("Yay!!")
        pyi_splash.close()
    except ImportError:
        pass

    print("Welcome btphone version " + version + " By Josjuar Lister 2021-2022")
    print(f"Let's Begin\n")

    ins = QApplication([])

    parser=argparse.ArgumentParser(
        description='''Here is my lovelly little python script to bruteforce phonenumbers from the bt phonebook :-). ''',
        epilog="""Josjuar Lister 2021-2022""")
    parser.add_argument('-n', '--surname', help='specify surname')
    parser.add_argument('-a', '--area', help='Area Town or Postcode')
    parser.add_argument('-s', '--street', help='specify street')
    parser.add_argument('-w', '--wordlist', help='input wordlist file')
    parser.add_argument('-o', '--output', help='output html file and open')
    args=parser.parse_args()

    #run
    window = Scan()
    window.resize(300,200)
    window.show()
    sys.exit(ins.exec())
