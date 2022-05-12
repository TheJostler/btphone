# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QDialog, QLabel)

import urllib3
import requests
import sys
from bs4 import BeautifulSoup
import argparse
import webbrowser
from colored import fg

class Scan(QDialog):
    def __init__(self, parent=None):
        super(Scan, self).__init__(parent)

        #Elements
        self.setWindowTitle("Btphone")
        self.street = QLineEdit()
        self.area = QLineEdit()
        self.go = QPushButton("GO")

        #Left Pane
        leftPane = QVBoxLayout( self )
        leftPane.setSpacing(2)
        LP_row1 = QHBoxLayout()
        LP_row2 = QHBoxLayout()
        LP_row3 = QHBoxLayout()

        #Labels
        labStreet = QLabel("Street Name:")
        labArea = QLabel("Area/Postcode:")

        #LP_row1
        LP_row1.addWidget(labStreet)
        LP_row1.addWidget(self.street)

        #LP_row2
        LP_row2.addWidget(labArea)
        LP_row2.addWidget(self.area)

        #LP_row3
        LP_row3.addWidget(self.go)

        #Finalize Left Pane
        leftPane.addLayout(LP_row1)
        leftPane.addLayout(LP_row2)
        leftPane.addLayout(LP_row3)

        self.setLayout(leftPane)
        self.go.clicked.connect(self.start)

    def start(self):
        print("street: " + self.street.text())
        print("area: " + self.area.text())

        txt_blue = fg('blue')
        txt_green = fg('green')
        txt_white = fg('white')
        txt_red = fg('red')

        wordlist = set()

        url = "https://www.thephonebook.bt.com/Person/PersonSearch"
        wordlist = "./wordlists/aa_zz.txt"
        output = self.street.text() + ".html"

        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        }

        if output is not None:
                print("output: " + output)
                o = open(output, "a")
                o.write("<html><body style=\"color: green; background-color: black;\"><h1>" + output + "</h1><p>area: " + self.area.text() + "</p><p>street: " + self.street.text() + "</p>")

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

            numsSeen = set()
            num = set()
            with open(wordlist) as f:
                    list = f.read().splitlines()
            for name in list:
                    payload = {"Surname": name, "Location": self.area.text(), "Street": self.street.text()}
                    print("Sending request for: " +name)
                    r = requests.get(url, params=payload, headers=HEADERS)
                    http_status(r)
                    print('trying:\t\t' + txt_blue + name + txt_white, end='\r')
                    ret = r.content.decode('utf-8')
                    soup = BeautifulSoup(ret, "html.parser")
                    nums = soup.select("a[href^=\"tel\"]")
                    if nums is None:
                        print(txt_red + '(Notice)\t' + txt_white + 'No phone numbers returned')
                        break
                    for num in nums:
                            if num not in numsSeen:
                                    print(num)
                                    if output is not None:
                                            o.write(str(num) + " | ")
                                    numsSeen.add(num)
                                    print(name, end='\r')
                                    if output is not None:
                                            o.write("returned by: " + name + "<br>")
                    if args.output is not None:
                            o.write("</body></html>")
                            o.close()
                            webbrowser.open_new_tab(args.output)


if __name__ == "__main__":

    print("Welcome")
    print(f"Let's begin\n")

    #run
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

    window = Scan()
    window.show()
    sys.exit(ins.exec())
