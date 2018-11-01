# Menus
# (1) Login/SignUp
# (2) MainMenu
#
#

import sqlite3 #sql module
import os
import sys
import getpass # password
import time #time delay
import datetime

from offerRide import *
from utility import *

# Login or Sign up Menu
def loginMenu():
    clearScreen()
    print("\n> Select a number option from the menu <\n")
    loginOption = input("1. Login \n2. Register\n< Type EXIT to end the program >\n")
    
    if (loginOption=='1' or loginOption=='2' or loginOption.upper()=='EXIT'):
        if loginOption.upper() == "EXIT":
            exit()
        else:
            loginOption = int(loginOption)
        
    else:
        print("***\n*** Pick 1 or 2. Try again\n***")
        time.sleep(2)
        loginMenu() # recalls the menu again
    
    return loginOption
    
# Main Menu
def mainMenu(database, cursor, member):
    clearScreen()

    print("\n")
    print("    ##################")
    print("    ####          ####")
    print("    ### MAIN  MENU ###")
    print("    ####          ####")    
    print("    ##################\n\n")
    print("> Select a number option from the menu <\n")
    
    menuOption = input("1. Offer a Ride\n2. Logout\n< Type EXIT to end the program >\n")
    
    if(menuOption == "1"): #offer a ride 
        time.sleep(0.5)
        offerRide(cursor, member)
        database.commit()# commit changes after user enters all info in 'offer ride' menu option
    
    elif(menuOption == "2"): # log out option
        clearScreen()
        print("\n\n\n\n############ ############# ############")
        print("############ #############")
        print("############")
        print("L O G G I N G   O U T . . . .... .. ............")
        print("..... .. ..... ..     . ...... ...... ..")
        print("############")
        print("############ #############")
        print("############ ############# ############")
        time.sleep(1.5)
        clearScreen()
        main()
        
    elif(menuOption.upper() == "EXIT"):
        exit()
    else:
        clearScreen()
        print("\n\n*** < {} > is not a menu option. Try again\n*** ".format(menuOption)) #will show the user what they inputted wrong