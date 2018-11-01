# Menu Options 
#

import sqlite3 #sql module
import os
import sys
import getpass # password
import time #time delay
import datetime

from utility import *

# Login or Sign up Menu
def loginMenu():
    
    login_option = 0
    
    while(login_option<1 or login_option>2):
        login_option = (input("Pick 1 to login as an existing user, or pick 2 to register\nAt any point, type EXIT to end your session\n"))
        if login_option.upper() == "EXIT":
            exit()
        
        if not (login_option[0].isdigit()):
            print("\n*** Invalid entry. Try again\n***")
            time.sleep(1)
            login_option = 0
            clearScreen()
        
        else:
            login_option = int(login_option)
            clearScreen()
    
    return login_option
    
    
# Main Menu
def mainMenu(database, cursor, member):
    clearScreen()
    exiting = False
    while not exiting:

        print("\n")
        print("    ##################")
        print("    ####          ####")
        print("    ### MAIN  MENU ###")
        print("    ####          ####")    
        print("    ##################\n\n")
        print("> Select a number option from the menu <\n")
        
        menuOption = input("1. Offer a Ride\n2. Logout\n< Type EXIT to end your session >\n")
        
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
            print("\n\n*** < {} > is not a menu option. Try again *** ".format(menuOption)) #will show the user what they inputted wrong