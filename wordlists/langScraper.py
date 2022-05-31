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
# Surname Scraper for building surname wordlists specific to a particular language
#
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

import argparse
import urllib3
import requests
import sys
import os
from bs4 import BeautifulSoup
from colored import fg

txt_blue = fg('blue')
txt_green = fg('green')
txt_white = fg('white')
txt_red = fg('red')

def http_status(r):
    status = r.status_code
    if status == 200:
        traffic = txt_green
        print(txt_blue + "  (Info)\t" + txt_white + "HTTP status code: " + traffic + str(r.status_code) + txt_white)
        return status
    elif status <= 400:
        traffic = txt_blue
        print(txt_blue + "  (Info)\t" + txt_white + "HTTP status code: " + traffic + str(r.status_code) + txt_white)
        return status
    else:
        traffic = txt_red
        print(txt_blue + "  (Info)\t" + txt_white + "HTTP status code: " + traffic + str(r.status_code) + txt_white)
        return status

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
        description='''A little script to scrape surnames of a particular language from familyeducation.com :-). ''',
        epilog="""Josjuar Lister 2021-2022""")
    parser.add_argument('-l', '--lang', help='specify language (use all lowercase)')
    parser.add_argument('-o', '--output', help='output .txt file (default res/lang.txt)')

    # To use arguments parsed here call 'args.<argument>'
    args=parser.parse_args()

    # If no surname is supplied ask for it
    if args.lang is None:
        lang = input("Please specify a language: ")
    else:
        lang = args.lang

    print("getting surnames for: " + lang)

    # Construct output file path

    outputName = lang + ".txt"
    outputPath = os.path.dirname(__file__) + "/res/" + outputName


    url = "https://www.familyeducation.com/baby-names/surname/origin/" + lang
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}

    init = requests.get(url, headers=HEADERS)
    if http_status(init) == 200:
        namesSeen = set()

        # Here we clobber any file that already exists for that same language
        # otherwise we risk repeating names and having massive file sizes
        clobber = open(outputPath, "w")
        clobber.write("")
        clobber.close()

        # Here we get the number of pages that exist for this language
        decoded = init.content.decode('utf-8')
        soup = BeautifulSoup(decoded, "html.parser")
        lastPage = soup.find(title="Go to last page", href=True)
        pages = lastPage['href'].strip(url + "?page=")

        for n in range(int(pages)):
            page = {"page": n}
            r = requests.get(url, params=page, headers=HEADERS)
            http_status(r)
            print(txt_blue + "(info)" + txt_white + "Scraping page: " + str(n))
            decoded = r.content.decode('utf-8')
            soup = BeautifulSoup(decoded, "html.parser")
            output = open(outputPath, "a")

            names = soup.select("a[href^=\"https://www.familyeducation.com/baby-names/name-meaning\"]")
            for element in names:
                name = element.decode_contents()
                if name not in namesSeen:
                    print(name)
                    output.write(name + "\n")
                    namesSeen.add(name)
    else:
        exit(print("Error that language doesn't seem to be supported"))
    
    output.close()
    exit(0)