# Register 
# registers the member into the database
#
#

import sqlite3 #sql module
import os
import sys
import getpass # password
import time #time delay
import datetime

from menus import *
from utility import *


def register(cursor):
    #registers the member; will return their email 
    clearScreen()
    print("\n")
    print("    ##################")
    print("    ####          ####")
    print("    ###  REGISTER  ###")
    print("    ####          ####")    
    print("    ##################\n\n> Enter your information below <")
    print(">   *FYI*  EXIT to exit, BACK to go to loginMenu <\n")

    emailIsFree = False
    trueName = False
    truePhone = False
    truePWD = False
    
    while emailIsFree == False:
        email = input("  Email: ")
        if(email.upper() == "EXIT"):
            exit()
        if(email.upper() == "BACK"):
            loginMenu()
        if len(email)>15:
            print("***\n*** Entered email too long. Try again \n***")
            continue
        elif len(email)==0:
            continue
            
        cursor.execute("SELECT email FROM members WHERE email = \""+email +"\"") #check if the email is in the members table
        allEmails = cursor.fetchall()
        
        if len(allEmails)==0:
            emailIsFree = True
        if emailIsFree == False:
            print("***\n*** An account exists with that email. Try another\n***")

    while trueName == False:
        name = input("  Name: ")
        if(name.upper() == "EXIT"):
            exit()
        if(name.upper() == "BACK"):
            loginMenu()
        if len(name)>20:
            print("***\n*** Entered name is too long (max 20 characters). Try again\n***")
            continue
        elif len(name)==0:
            continue
        else:
            trueName = True

    while truePhone == False:
        phone = input("  Phone (ex.xxx-xxx-xxxx): ")
        if(phone.upper() == "EXIT"):
            exit()
        if(phone.upper() == "BACK"):
            loginMenu()
        if len(phone)>12:
            print("***\n*** Entered phone number is too long. Try again (ex. xxx-xxx-xxxx)\n***")
            continue
        if len(phone)<12:
            print("***\n*** Entered phone number is too short or in the wrong format. Try again (ex. xxx-xxx-xxxx)\n***")
            continue
        elif len(phone)==0:
            continue
        else:
            truePhone = True

    while truePWD == False:
        password = getpass.getpass("  Password (max 6 characters): ")
        if(password.upper() == "EXIT"):
            exit()
        if(password.upper() == "BACK"):
            loginMenu()
        if len(password)>6:
            print("***\n*** Password is too long. Try again (max 6 characters)\n***")
            continue
        elif len(password)==0:
            continue
        else:
            truePWD = True

    cursor.execute("INSERT INTO members VALUES (\""+email+"\",\""+name+"\",\""+phone+"\",\""+password+"\")")
    print("***\n*** You're now successfully registered!\n***")
    
    
    return email