#!/usr/bin/env python

# THIS SOFTWARE IS CURRENTLY IN DEVELOPMENT! 
# 
# To keep tack of the development of btphone or if you would like to contribute
# please visit:
# 
# https://github.com/thejostler/btphone
# 
# Please contact me by emailing: josj@wjaag.com
#
# Here is the initial version of my script
# it uses area information and surnames to find phone numbers from the bt phonebook
# it outputs the phone numbers to a html file and opens it with the default web browser
# I am currently trying to create a gui app which can store the phone numbers for later use.

# I have a working gui wrapper which starts this script as a sub-process

# LICENSE
# Copyright (c) 2022 Josjuar Lister

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import urllib3
import requests
import sys
from bs4 import BeautifulSoup
import argparse
import webbrowser
from colored import fg

# include these variables in a print() function to output different clours to your terminal
txt_blue = fg('blue')
txt_green = fg('green')
txt_white = fg('white')
txt_red = fg('red')

# The Website address we will be targeting
url = "https://www.thephonebook.bt.com/Person/PersonSearch"

# Including generic User-Agent http header to make us look like a browser
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}

# A function for outputing the http response to make sure that bt.com is still talking back to us!
# Pass the http response as the argument 'r'
def http_status(r):
    # Generally a http status code higher than 200 is bad news
	if r.status_code == 200:
		traffic = txt_green
		print(txt_blue + "  (Info)\t" + txt_white + "HTTP status code: " + traffic + str(r.status_code) + txt_white)
	elif r.status_code <= 400:
		traffic = txt_blue
		print(txt_red + "  (warn)\t" + txt_white + "HTTP status code: " + traffic + str(r.status_code) + txt_white)
	else:
		traffic = txt_red
		print(txt_red + "  (warn)\t" + txt_white + "HTTP status code: " + traffic + str(r.status_code) + txt_white)

# Start scanning using a wordlist of names to bruteforce phone numbers
def scan_wordlist(street, area, wordlist, output):
    # Define variables
    numsSeen = set()
    num = set()

    # Open wordlist
    with open(wordlist) as f:
        list = f.read().splitlines()
    for name in list:

        # Here is where we package our parameters that we will send to 'bt.com', they are put into an array that will be passed to 'requests.get' as params
        payload = {"Surname": name, "Location": area, "Street": street}

        # We will wait 15 seconds for a response and try again, if we fail to get a response 3 times we skip that name and move on.
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

        # Print http status to terminal
        http_status(r)
        print('trying:\t\t' + txt_blue + name + txt_white, end='\r')

        # Decode response from binary into UTF-8 charcters
        ret = r.content.decode('utf-8')

        # Use Beautiful Soup Module to parse html then find and extract the phone number
        soup = BeautifulSoup(ret, "html.parser")
        nums = soup.select("a[href^=\"tel\"]")

        for element in nums:

            # Extract inner content of 'html' <a> tags that are found
            num = element.decode_contents()

            # We want to remember numbers we have seen before so that we don't get repeats
            if num not in numsSeen:
                print(str(num) + " returned by: " + str(name))
                if output is not None:
                    o.write(str(num) + " | ")
                numsSeen.add(num)
                print(name, end='\r')
                if output is not None:
                    o.write("returned by: " + name + "<br>")
    # If outputing to a 'html' file, append closing tabs( </...> ) to the end of the file
    if output is not None:
        o.write("</body></html>")
        o.close()
        webbrowser.open_new_tab(output)

    # Success
    return 0

# Start a scan only once using a single surname
def scan_surname(street, area, surname, output):

    # Here is where we package our parameters that we will send to 'bt.com', they are put into an array that will be passed to 'requests.get' as params
    payload = {"Surname": surname, "Location": area, "Street": street}

    # We will wait 15 seconds for a response and try again, if we fail to get a response 3 times we skip that name and move on.
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

    # Print http status to terminal
    http_status(r)
    

    # Decode response from binary into UTF-8 charcters
    ret = r.content.decode('utf-8')

    # Use Beautiful Soup Module to parse html then find and extract the phone number
    soup = BeautifulSoup(ret, "html.parser")
    nums = soup.select("a[href^=\"tel\"]")

    # If there we have found a phone number
    if (len(nums) > 1):
        for element in nums:

            # Extract inner content of 'html' <a> tags that are found
            num = element.decode_contents()
            print(num)

            # If outputing to a 'html' file, append closing tabs( </...> ) to the end of the file
            if output is not None:
                o.write(str(num))
                o.write("</body></html>")
                o.close()
                # Finally open the default webbrowser and show the page
                webbrowser.open_new_tab(output)
    else:
    	print(txt_red + '(Notice)\t' + txt_white + 'No phone numbers returned')
    return 0

# Initialize -- Start Here! Here is where we parse command line argyments.
if __name__ == "__main__":
	parser=argparse.ArgumentParser(
		description='''Here is my lovelly little python script to bruteforce phonenumbers from the bt phonebook :-). ''',
		epilog="""Josjuar Lister 2021-2022""")
	parser.add_argument('-n', '--surname', help='specify surname')
	parser.add_argument('-a', '--area', help='Area Town or Postcode', required=True)
	parser.add_argument('-s', '--street', help='specify street', required=True)
	parser.add_argument('-w', '--wordlist', help='input wordlist file')
	parser.add_argument('-o', '--output', help='output html file and open')
    
    # To use arguments parsed by here call 'args.<argument>'
	args=parser.parse_args()
else:
    exit(1)

# If we want to output to a html file, ...
if args.output is not None:
	print("output: " + args.output)
	o = open(args.output, "a")
	o.write("<html><body style=\"color: green; background-color: black;\"><h1>" + args.output + "</h1><p>area: " + args.area + "</p><p>street: " + args.street + "</p>")

if args.street is not None:
    ##Wordlist scan
    if args.wordlist is not None:
        sys.exit(scan_wordlist(args.street, args.area, args.wordlist, args.output))

    ##One person scan
    elif args.surname is not None:
        sys.exit(scan_surname(args.street, args.area, args.surname, args.output))
