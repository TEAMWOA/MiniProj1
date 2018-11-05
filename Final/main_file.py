# Main Program 
#
#

import sqlite3
import sys
import time
import os
import datetime

from menus import *
from utility import *


def main():
    # Setup connection to database
    if len(sys.argv) != 2:
        print("Please pass the database file as a command line argument (dbname.db)")
        exit()
    
    clear_screen()    
    print("\n\n############ ############# ############")
    print("############ #############")
    print("############")
    print("L O A D I N G. . . . .... .. ....  ...... ..")
    print("..... .. ..... ..     . ...... .. .... ..  . . The  Ride  Offering  Program")
    print("############")
    print("############ #############")
    print("############ ############# ############")
    time.sleep(2.5)
    
    path = "./{}".format(sys.argv[1])
    db_connection = sqlite3.connect(path)
    # db_connection = sqlite3.connect("./testDatabase.db")
    cursor = db_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    db_connection.commit()

    # Start user at login menu
    login_menu(db_connection, cursor)
    
    # commit and close database
    db_connection.commit()
    db_connection.close()
    # exit with print messages
    db_exit()


if __name__ == "__main__":
    main()
