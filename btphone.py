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

wordlist = set()
parser=argparse.ArgumentParser(
    description='''Here is my lovelly little python script to bruteforce phonenumbers from the bt phonebook :-). ''',
    epilog="""Josjuar Lister 2021-2022""")
parser.add_argument('-n', '--surname', help='specify surname')
parser.add_argument('-a', '--area', help='Area Town or Postcode')
parser.add_argument('-s', '--street', help='specify street')
parser.add_argument('-w', '--wordlist', help='input wordlist file')
parser.add_argument('-o', '--output', help='output html file and open')
args=parser.parse_args()

if args is None:
	print('run btphone -h')
	exit()
url = "https://www.thephonebook.bt.com/Person/PersonSearch"
#url = "https://httpbin.org/get"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}

if args.output is not None:
	print("output: " + args.output)
	o = open(args.output, "a")
	o.write("<html><body style=\"color: green; background-color: black;\"><h1>" + args.output + "</h1><p>area: " + args.area + "</p><p>street: " + args.street + "</p>")

def http_status(r):
	if r.status_code == 200:
		traffic = txt_green
		//print(txt_blue + "  (Info)\t" + txt_white + "HTTP status code: " + traffic + str(r.status_code) + txt_white)
	elif r.status_code <= 400:
		traffic = txt_blue
		print(txt_blue + "  (Info)\t" + txt_white + "HTTP status code: " + traffic + str(r.status_code) + txt_white)
	else:
		traffic = txt_red
		print(txt_blue + "  (Info)\t" + txt_white + "HTTP status code: " + traffic + str(r.status_code) + txt_white)

if args.wordlist is not None:
	numsSeen = set()
	num = set()
	with open(args.wordlist) as f:
		list = f.read().splitlines()
	for name in list:
		payload = {"Surname": name, "Location": args.area, "Street": args.street}
		
		r = requests.get(url, params=payload, headers=HEADERS, timeout=15)
			
		http_status(r)
		print('trying:\t\t' + txt_blue + name + txt_white, end='\r')
		ret = r.content.decode('utf-8')
		soup = BeautifulSoup(ret, "html.parser")
		nums = soup.select("a[href^=\"tel\"]")
		for num in nums:
			if num not in numsSeen:
				print(num)
				if args.output is not None:
					o.write(str(num) + " | ")
				numsSeen.add(num)
				print(name, end='\r')
				if args.output is not None:
					o.write("returned by: " + name + "<br>")
	if args.output is not None:
		o.write("</body></html>")
		o.close()
		webbrowser.open_new_tab(args.output)
else:
	payload = {"Surname": args.surname, "Location": args.area, "Street": args.street}
	
	r = requests.get(url, params=payload, headers=HEADERS, timeout=15)

	http_status(r)
	ret = r.content.decode('utf-8')

	soup = BeautifulSoup(ret, "html.parser")
	nums = soup.select("a[href^=\"tel\"]")
	numsSeen = set()
	for num in nums:
		if num not in numsSeen:
			print(num)
			if args.output is not None:
				o.write(str(num))
				o.write("</body></html>")
				o.close()
				webbrowser.open_new_tab(args.output)
	else:
		print(txt_red + '(Notice)\t' + txt_white + 'No phone numbers returned')
