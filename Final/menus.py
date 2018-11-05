# Menus

# (1) login_menu(db_connection, cursor)
# (2) main_menu(db_connection, cursor, member_email)
# (3) inbox(db_connection, cursor, member_email)
# (4) login(db_connection, cursor)
# (5) register(db_connection, cursor)
#
#
#

import sqlite3
import sys
import time
import os
import datetime
import getpass
import time #time delay

from utility import *
# call functions by: module.function 
import requests
import rides
import bookings







################################################################
#
# (1) LOGIN MENU
#
def login_menu(db_connection, cursor):
    # First menu user encounters, allows for logging in, registering a new account and exiting
    while True:
        clear_screen()
        
        print("\n")
        print("    ######################")
        print("    ####              ####")
        print("    ### AUTHENTICATION ###")
        print("    ####              ####")    
        print("    ######################\n\n")
        print("> Select a number option from the menu\n< Type EXIT to end the program >\n")

        print("   1. Login")
        print("   2. Register")
        print("   3. Exit")

        # Validate input
        valid_choice = False
        
        while not valid_choice:
            choice = input()
            
            if choice == "1":
                login(db_connection, cursor)

            elif choice == "2":
                register(db_connection, cursor)

            elif choice == "3":
                db_exit(db_connection)
        
            elif (choice.upper() == "EXIT"):
                db_exit(db_connection)
            
            else:
                print("\n***\n*** < {} > is not a menu option. Try again\n*** ".format(choice)) #shows the user what they inputted wrong
                continue
################################################################
#
# (2) MAIN MENU (opts. 1-10)

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
        print("   5. Search/View for Ride Request")
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
            rides.ride_search(db_connection, cursor, member_email)
            return
       
        #2. Offer Ride    
        if choice == "2":
            rides.offer_ride(db_connection, cursor, member_email)
            return
       ###########
        #3. Book Member on Ride
        if choice == "3":
            #bookings.
            return
        
        #4. Cancel Ride Booking
        if choice == "4":
            #bookings.
            return 
        
        #5. Search for Ride Request
        if choice == "5":
            #requests.search
            return
        
        #6. Post Ride Request
        if choice == "6":
        
            requests.post_ride_request(cursor, member_email)
            return
        
        #7. Delete Ride Request
        if choice == "7":
            #requests.
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
    return
    end 
            
################################################################
#
# (3) MEMBER INBOX
#
def inbox(db_connection, cursor, member_email):
    # Displays the user's unread messages
    clear_screen()
    print("\n")
    print("    ###################")
    print("    ####           ####")
    print("    ###    INBOX    ###")
    print("    ####           ####")    
    print("    ###################\n\n")
    print("< Type EXIT to end the program or BACK/press ENTER to go back to the Main Menu >\n")
    
    print("   1. Unread Messages")
    print("   2. All Messages")
    print("   3. Exit")
    
    # Gets all messages sent to user, creates list of unread messages
    unread_messages = []
    all_messages = []
    cursor.execute("SELECT * FROM inbox WHERE email=? COLLATE NOCASE;", [member_email])
    for row in cursor:
        email, timestamp, sender, content, rno, seen = row
        if seen == 'n':
            unread_messages.append([timestamp, sender, content, rno])
        all_messages.append([timestamp, sender, content, rno])

    #input choice handling 
    choice = input()
    while choice not in ("1", "2", "3", "","exit", "Exit", "EXIT","back","BACK","Back"):
        print("\n***\n*** < {} > is not a menu option. Try again\n*** ".format(choice)) #will show the user what they inputted wrong
        choice = input()
        
    #Unread Messages    
    if choice == "1":
        print("   Unread Messages:\n")
        if len(unread_messages) > 0:
            for message in unread_messages:
                print("{:<15}      {:>19}".format(message[1], message[0]))
                print("   Regarding ride #{}".format(message[3]))
                print(message[2])
                print()
                #input("< Type EXIT to end the program or BACK/press ENTER to go back to the Main Menu >\n")
                # Uncomment when done testing
                # cursor.execute("UPDATE inbox SET seen='y' WHERE email=?;", [member_email])
                # db_connection.commit()
        else:
            clear_screen()
            print("\n***\n*** You have no unread messages\n***")
            input("\n< Press ENTER/any key to go back to your inbox. >")

            
    #All Messages 
    if choice == '2':
        print("   All Messages:\n")
        if len(all_messages) > 0:
            for message in all_messages:
                print("{:<15}      {:>19}".format(message[1], message[0]))
                print("   Regarding ride #{}".format(message[3]))
                print(message[2])
                print() 
        else:
            clear_screen()
            print("\n***\n*** You have no messages\n***")
            input("\n< Press ENTER/any key to go back to your inbox. >")
            
    if choice == '3' or choice.upper() == "EXIT":
        db_exit(db_connection)
        
    if choice == '' or choice.upper() == "BACK":
        main_menu(db_connection, cursor, member_email)
         
    else:  
        inbox(db_connection, cursor, member_email) # default just take the member to the inbox
    
                
################################################################
#
# (4) LOGIN MEMEBER
#
def login(db_connection, cursor):
    # Gets email / password from user, verifies it
    clear_screen()
    print("\n")
    print("    ##################")
    print("    ####          ####")
    print("    ###   LOG IN   ###")
    print("    ####          ####")    
    print("    ##################\n\n")
    print(">Enter email & password: ")
    print("< Type EXIT to end the program or BACK/press ENTER to go back to the Login/Signup Menu >\n")
    
    trueEmail = False
    truePassword = False
    
    while trueEmail == False: #loops until a proper email address is entered
        email = input("  Email: ").upper()
        
        if email == "EXIT":
            db_exit(db_connection)
            
        if email == "BACK" or email == "":
            #return #maybe wrong....... # GOES BACK TO THE MAIN AUTHENTICATION MENU  (before print statements)
            login_menu(db_connection, cursor)
            
        cursor.execute("SELECT email FROM members WHERE email=? COLLATE NOCASE;", [email])
        emailList = cursor.fetchall()
        if len(emailList)>0 and email != "email":
            trueEmail = True
            
        if trueEmail == False:
            print("\n***\n*** No account is registered under that email. Try another\n***")
            
    while truePassword == False: # loops until a proper password (that matches the email) is entered
        password = getpass.getpass("  Password: ")    # Hides input
        cursor.execute("SELECT pwd FROM members WHERE email=? COLLATE NOCASE;", [email])
        correct_password = cursor.fetchone()[0]
        
        if password == correct_password:
            truePassword = True
            print("***\n*** You're now successfully logged in!\n***")
            inbox(db_connection, cursor, email)  # Continue to inbox
#             db_exit(db_connection)
        else:
            print("***\n*** Incorrect password. Try another\n***")
            
################################################################                    
#
# (5) REGISTER MEMBER
#
def register(db_connection, cursor):
    # Gets email, name, phone, password from user
    # If no account registered under that email, creates entry in members table
    # User can return to the login menu by pressing enter at any time
   
    clear_screen()
    print("\n")
    print("    ##################")
    print("    ####          ####")
    print("    ###  REGISTER  ###")
    print("    ####          ####")    
    print("    ##################\n\n> Enter your information below <")
    print("< Type EXIT to end the program or BACK/press ENTER to go back to the Login/Signup Menu >\n")

    emailIsFree = False
    trueName = False
    truePhone = False
    truePWD = False
    
    while emailIsFree == False:
        email = input("  Email: ")
        if(email.upper() == "EXIT"):
            db_exit(db_connection)
        if(email.upper() == "BACK" or email ==""):
            login_menu(db_connection, cursor)
            
        if len(email)>15:
            print("***\n*** Entered email too long (15 character Limit). Try again \n***")
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
            db_exit(db_connection)
        if(name.upper() == "BACK" or name ==""):
            login_menu(db_connection, cursor)
        if len(name)>20:
            print("***\n*** Entered name is too long (20 character limit). Try again\n***")
            continue
        elif len(name)==0:
            continue
        else:
            trueName = True

    while truePhone == False:
        phone = input("  Phone (ex.xxx-xxx-xxxx): ")
        if(phone.upper() == "EXIT"):
            db_exit(db_connection)
        if(phone.upper() == "BACK" or phone ==""):
            login_menu(db_connection, cursor)
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
        password = getpass.getpass("  Password (6 character limit): ")
        if(password.upper() == "EXIT"):
            db_exit(db_connection)
        if(password.upper() == "BACK" or password ==""):
            login_menu(db_connection, cursor)
        if len(password)>6:
            print("***\n*** Password is too long. Try again (6 character limit)\n***")
            continue
        elif len(password)==0:
            continue
        else:
            truePWD = True
    cursor.execute("INSERT INTO members VALUES (?, ?, ?, ?);", [email, name, phone, password])
    db_connection.commit() # commit right now to ensure member can book/use their account
    print("***\n*** You're now successfully registered!\n***")
    time.sleep(1.5)
    main_menu(db_connection, cursor, email) # Continue to main menu (No messages to see for a newly created account)


#RUN MAIN 
# def main():
#     # Setup connection to database
#     if len(sys.argv) != 2:
#         print("Please pass the database file as a command line argument (dbname.db)")
#         exit()
#     
#     clear_screen()    
#     print("\n\n\n\n############ ############# ############")
#     print("############ #############")
#     print("############")
#     print("L O A D I N G. . . . .... .. ....  ...... ..")
#     print("..... .. ..... ..     . ...... .. .... ..  . . The  Ride  Offering  Program")
#     print("############")
#     print("############ #############")
#     print("############ ############# ############")
#     time.sleep(0.5)
#     
#     path = "./{}".format(sys.argv[1])
#     db_connection = sqlite3.connect(path)
#     cursor = db_connection.cursor()
#     cursor.execute('PRAGMA foreign_keys=ON;')
#     db_connection.commit()
# 
#     # Start user at login menu
#     login_menu(db_connection, cursor)
#     
#     #commit and close database
#     db_exit(db_connection)
# 
# 
# if __name__ == "__main__":
#     main()

