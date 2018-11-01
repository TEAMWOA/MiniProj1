# Utility functions for the program
#
#

import sqlite3 #sql module
import os
import sys
import getpass # password
import time #time delay
import datetime

def clearScreen():
    # Function to clear the screen - less clutter
    os.system("clear")
    
    
def exit():
    # Exits the Program
    clearScreen()
    print('\n\n\n   .. .. .... .... .. .\n.. ... .. \nQuitting Program ..... \n\n')
    print("    ###################")
    print("    ####           ####")
    print("    ##  SeeYouAgain  ##")
    print("    ####           ####")    
    print("    ###################\n")
    print('\n    . . . .... .... ..\n                ... . ..... .. .. ')
    time.sleep(2) 
    sys.exit()