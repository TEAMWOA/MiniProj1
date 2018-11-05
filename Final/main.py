# Main Program 
#
# 

import sqlite3
import sys
import time
import os
import datetime

import menus # all of the menus ; menus imports requests, rides, bookings
from utility import * #various utility functions


def main():
    # Setup connection to database
    if len(sys.argv) != 2:
        print("Please pass the database file as a command line argument (dbname.db)")
        exit()
    
    clear_screen()    
    print("\n\n\n\n############ ############# ############")
    print("############ #############")
    print("############")
    print("L O A D I N G. . . . .... .. ....  ...... ..")
    print("..... .. ..... ..     . ...... .. .... ..  . . The  Ride  Offering  Program")
    print("############")
    print("############ #############")
    print("############ ############# ############")
    time.sleep(0.5)
    
    path = "./{}".format(sys.argv[1])
    db_connection = sqlite3.connect(path)
    cursor = db_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    db_connection.commit()

    # Start user at login menu
    menus.login_menu(db_connection, cursor)
    
    #commit and close database
    db_exit(db_connection)


if __name__ == "__main__":
    main()
