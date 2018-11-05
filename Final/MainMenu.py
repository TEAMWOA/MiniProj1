import sqlite3 #sql module
import os
import sys
import getpass # password
import time #time delay
import datetime

from utility import *
from authentication import *
from requests import *
from rides import *

################################################################
#
# (2) MAIN MENU (opts. 1-10)
#
def main_menu(db_connection, cursor, member_email):
    # Main menu
    while True:
        clear_screen()
        
        print("\n")
        print("    ##################")
        print("    ####          ####")
        print("    ### MAIN  MENU ###")
        print("    ####          ####")    
        print("    ##################\n\n")
    
        print("\n> Select a number option from the menu")
        print("< Type EXIT to end the program >\n")
        print("   1. Search for Rides")
        print("   2. Offer Ride")
        print("   3. Book Member on Ride")
        print("   4. Cancel Ride Booking")
        print("   5. Search for Ride Request")
        print("   6. Post Ride Request")
        print("   7. Delete Ride Request")
        print("   8. Inbox")
        print("   9. Logout")
        print("   10. Exit")

        # Validate input
        choice = input()
        while choice not in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "exit", "Exit", "EXIT"):
            print("\n***\n*** < {} > is not a menu option. Try again\n*** ".format(choice)) #will show the user what they inputted wrong
            choice = input()
        
        #1. Search for Rides
        if choice == "1":
            ride_search(db_connection, cursor)
            return
       
        #2. Offer Ride    
        if choice == "2":
            offer_ride(db_connection, cursor, member_email)
            return
       ###########
        #3. Book Member on Ride
        if choice == "3":
            post_ride_request(cursor, member_email)
            return
        
        #4. Cancel Ride Booking
        if choice == "4":
            post_ride_request(cursor, member_email)
            return 
        
        #5. Search for Ride Request
        if choice == "5":
            post_ride_request(cursor, member_email)
            return
        
        #6. Post Ride Request
        if choice == "6":
            post_ride_request(cursor, member_email)
            return
        
        #7. Delete Ride Request
        if choice == "7":
            post_ride_request(cursor, member_email)
            return
        ############
        #8. Inbox
        if choice == "8":
            inbox(db_connection, cursor, member_email)
            return
        
        #9. Logout
        if choice == "9": 
            clear_screen()
            print("\n\n\n\n############ ############# ############")
            print("############ #############")
            print("############")
            print("L O G G I N G   O U T . . . .... .. ............")
            print("..... .. ..... ..     . ...... ...... ..")
            print("############")
            print("############ #############")
            print("############ ############# ############")
            time.sleep(1.5)
            clear_screen()
            login_menu(db_connection, cursor)

        #10. Exit
        if choice == "10" or choice.upper() == "EXIT":
            #time.sleep(0.5)
            db_exit(db_connection)
            
        #Anything Else
        else:
            clear_screen()
            print("\n***\n*** < {} > is not a menu option. Try again\n*** ".format(choice)) #will show the user what they inputted wrong
            time.sleep(1.5)
    #return
    # end 
  