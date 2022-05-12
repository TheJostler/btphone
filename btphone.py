#!/usr/bin/env python

import urllib3
import requests
import sys
from bs4 import BeautifulSoup
import argparse
import webbrowser
from colored import fg

txt_blue = fg('blue')
txt_green = fg('green')
txt_white = fg('white')
txt_red = fg('red')

url = "https://www.thephonebook.bt.com/Person/PersonSearch"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}

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
				
	parser=argparse.ArgumentParser(
		description='''Here is my lovelly little python script to bruteforce phonenumbers from the bt phonebook :-). ''',
		epilog="""Josjuar Lister 2021-2022""")
	parser.add_argument('-n', '--surname', help='specify surname')
	parser.add_argument('-a', '--area', help='Area Town or Postcode', required=True)
	parser.add_argument('-s', '--street', help='specify street', required=True)
	parser.add_argument('-w', '--wordlist', help='input wordlist file')
	parser.add_argument('-o', '--output', help='output html file and open')
	args=parser.parse_args()

if args.street is not None:
        ##Wordlist scan
        if args.wordlist is not None:
            sys.exit(scan_wordlist(args.street, args.area, args.wordlist, args.output))

        ##One person scan
        else:
            if args.surname is not None:
                sys.exit(scan_surname)
