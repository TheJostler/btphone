# btphone

By Josjuar Lister 2021-2022

An open source, cross platform application for getting UK phone numbers from the BT phone book.

If you would like to contribute to our project, please contact me by email at josj@wjaag.com


## About

Originally I wrote this as a simple python script that uses urllib3 and beautiful soup libraries to brute-force telephone numbers from the by phone book. You pass the Street, postcode, and a file containing surnames as arguments to the script, the script with then send a http 'Get' request to btphone book and filter out any phone numbers from the response.

However as interest in my project began to grow, I felt the need to create a GUI for the program to make the program easier to use. 

## Install

This application is still very much 'in development'.

At the moment I have only compiled a working GUI ELF executable binary for Limux AMDx64 using ParrotSec OS.

However if you wish you can compile the program into your OS using the [pyinstaller](https://pypi.org/project/pyinstaller/) python module.

I have created two directories in the btphone-gui directory, build_d for creating a one-folder bundle containing an executable. And build_f for compiling a single-file bundled executable

## Run

Simply run the btphone.py script in un your Python interrupter, or Use Pyinstaller to create the GUI application from inside the btphone-gui/build_d/f

