## About

This is the beginning of our GUI app...

I'm using at the moment I have a lazy little btphone-start-sub-process.py which uses PySide6 to create a little app window with input fields for Street and area.

It then starts ../btphone.py as a subprocess and passes the street and area as arguments to the script..

This script should be called inside of a terminal so that you can see the progress of the script and the returned phone numbers.

## The Plan

I want to copy the code of byphone.py into the GUI wrapper so that no sub-process need to be called...
