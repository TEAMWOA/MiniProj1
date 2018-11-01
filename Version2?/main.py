# Main Program 

import sqlite3 #sql module
import os
import sys
import getpass # password
import time #time delay
import datetime

from loginMenu import *
from offerRide import *
from register import *
from utility import *


def main():

    database = sqlite3.connect("testDatabase.db")
    cursor = database.cursor()
    
    clearScreen()
    print("\n\n\n\n############ ############# ############")
    print("############ #############")
    print("############")
    print("L O A D I N G. . . . .... .. ....  ...... ..")
    print("..... .. ..... ..     . ...... .. .... ..  . . The  Ride  Offering  Program")
    print("############")
    print("############ #############")
    print("############ ############# ############")
    
    time.sleep(2.5)
    
    member = register(cursor)
    #member = loginMenu()
    
    mainMenu(database, cursor, member)
    database.commit() # commit changes before exiting
    database.close()
    exit()


if __name__ == "__main__":
    main()
