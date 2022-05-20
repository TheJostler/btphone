# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QDialog, QLabel)
from PySide6.QtGui import QIcon
import argparse
import urllib3
import requests
from bs4 import BeautifulSoup
import argparse
import webbrowser
from colored import fg

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

    txt_blue = fg('blue')
    txt_green = fg('green')
    txt_white = fg('white')
    txt_red = fg('red')

    url = "https://www.thephonebook.bt.com/Person/PersonSearch"

    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}

    def http_status(r):
        if r.status_code == 200:
            traffic = txt_green
            print(txt_blue + "  (Info)\t" + txt_white + "HTTP status code: " + traffic + str(r.status_code) + txt_white)
        elif r.status_code <= 400:
            traffic = txt_blue
            print(txt_blue + "  (Info)\t" + txt_white + "HTTP status code: " + traffic + str(r.status_code) + txt_white)
        else:
            traffic = txt_red
            print(txt_blue + "  (Info)\t" + txt_white + "HTTP status code: " + traffic + str(r.status_code) + txt_white)

    def scan_wordlist(street, area, wordlist, output):
        numsSeen = set()
        num = set()
        with open(wordlist) as f:
            list = f.read().splitlines()
        for name in list:
            payload = {"Surname": name, "Location": area, "Street": street}
            try:
                r = requests.get(url, params=payload, headers=HEADERS, timeout=15)
            except:
                print(txt_blue + "  (info)\t" + txt_white + name + " Timed out, retrying")
                try:
                    r = requests.get(url, params=payload, headers=HEADERS, timeout=15)
                except:
                    print(txt_blue + "  (info)\t" + txt_white + name + " Timed out, twice, retrying")
                    try:
                        r = requests.get(url, params=payload, headers=HEADERS, timeout=15)
                    except:
                        print(txt_red + "  (warn)\t" + txt_white + name + " Timed out, tree times, skipping")
                        pass
            http_status(r)
            print('trying:\t\t' + txt_blue + name + txt_white, end='\r')
            ret = r.content.decode('utf-8')
            soup = BeautifulSoup(ret, "html.parser")
            nums = soup.select("a[href^=\"tel\"]")
            for num in nums:
                if num not in numsSeen:
                    print(str(num) + " returned by: " + str(name))
                    if output is not None:
                        o.write(str(num) + " | ")
                    numsSeen.add(num)
                    print(name, end='\r')
                    if output is not None:
                        o.write("returned by: " + name + "<br>")
        if output is not None:
            o.write("</body></html>")
            o.close()
            webbrowser.open_new_tab(output)

    def scan_surname(street, area, surname, output):
        payload = {"Surname": surname, "Location": area, "Street": street}
        try:
            r = requests.get(url, params=payload, headers=HEADERS, timeout=15)
        except:
            print(txt_blue + "  (info)\t" + txt_white + name + " Timed out, retrying")
            try:
                r = requests.get(url, params=payload, headers=HEADERS, timeout=15)
            except:
                print(txt_blue + "  (info)\t" + txt_white + name + " Timed out, twice, retrying")
                try:
                    r = requests.get(url, params=payload, headers=HEADERS, timeout=15)
                except:
                    print(txt_red + "  (warn)\t" + txt_white + name + " Timed out, tree times, skipping")
                    pass
        http_status(r)
        ret = r.content.decode('utf-8')

        soup = BeautifulSoup(ret, "html.parser")
        nums = soup.select("a[href^=\"tel\"]")
        numsSeen = set()
        for num in nums:
            if num not in numsSeen:
                print(num)
                if output is not None:
                    o.write(str(num))
                    o.write("</body></html>")
                    o.close()
                    webbrowser.open_new_tab(output)
        else:
            print(txt_red + '(Notice)\t' + txt_white + 'No phone numbers returned')

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
