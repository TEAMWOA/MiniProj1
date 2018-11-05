# Authentication
# (1) register(db_connection, cursor)
# (2) login(db_connection, cursor)
#
#

import getpass
import menus
from time import sleep
from utility import *


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
    print(">   *FYI*  EXIT to exit, BACK to go to loginMenu <\n")

    emailIsFree = False
    trueName = False
    truePhone = False
    truePWD = False
    
    while not emailIsFree:
        email = input("  Email: ")
        if email.upper() == "EXIT":
            db_exit(db_connection)
        if email.upper() == "BACK":
            menus.login_menu(db_connection, cursor)
        if len(email) > 15:
            print("***\n*** Entered email too long (15 character Limit). Try again \n***")
            continue
        elif len(email) == 0:
            continue
            
        cursor.execute("SELECT email FROM members WHERE email = ?;", [email]) #check if the email is in the members table
        allEmails = cursor.fetchall()
        
        if len(allEmails) == 0:
            emailIsFree = True
        if not emailIsFree:
            print("***\n*** An account exists with that email. Try another\n***")

    while not trueName:
        name = input("  Name: ")
        if name.upper() == "EXIT":
            db_exit(db_connection)
        if name.upper() == "BACK":
            menus.login_menu(db_connection, cursor)
        if len(name) > 20:
            print("***\n*** Entered name is too long (20 character limit). Try again\n***")
            continue
        elif len(name) == 0:
            continue
        else:
            trueName = True

    while not truePhone:
        phone = input("  Phone (xxx-xxx-xxxx): ")
        if phone.upper() == "EXIT":
            exit()
        if phone.upper() == "BACK":
            menus.login_menu(db_connection, cursor)
        if len(phone) > 12:
            print("***\n*** Entered phone number is too long. Try again (xxx-xxx-xxxx)\n***")
            continue
        if len(phone) < 12:
            print("***\n*** Entered phone number is too short or in the wrong format. Try again (xxx-xxx-xxxx)\n***")
            continue
        elif len(phone) == 0:
            continue
        else:
            truePhone = True

    while not truePWD:
        password = getpass.getpass("  Password (6 character limit): ")
        if password.upper() == "EXIT":
            db_exit(db_connection)
        if password.upper() == "BACK":
            menus.login_menu(db_connection, cursor)
        if len(password) > 6:
            print("***\n*** Password is too long. Try again (6 character limit)\n***")
            continue
        elif len(password) == 0:
            continue
        else:
            truePWD = True

    cursor.execute(
        "INSERT INTO members VALUES (?, ?, ?, ?);", [email, name, phone, password])
    db_connection.commit()
    print("\n***\n*** You're now successfully registered!\n***")
    sleep(2)
    menus.main_menu(db_connection, cursor, email)


def login(db_connection, cursor):
    # Gets email / password from user, verifies it
    clear_screen()
    print("\n")
    print("    ##################")
    print("    ####          ####")
    print("    ###   LOG IN   ###")
    print("    ####          ####")    
    print("    ##################\n\n")

    while True:
        while True:
            email = input("Enter email or press enter to return: ").lower()
            if email == '':
                menus.login_menu(db_connection, cursor)
                return
                
            if email =='exit':
                db_exit(db_connection)
            else:
                cursor.execute("SELECT pwd FROM members WHERE email=? COLLATE NOCASE;", [email])

            try:
                # Get password associated to email entered
                correct_password = cursor.fetchone()[0]
                break
            except:   # Error when the email entered doesn't exist in the database
                print("\nNo account registered under that email.\n")

        password = getpass.getpass("Password: ")    # Hides input

        if password == correct_password:
            menus.inbox(db_connection, cursor, email)  # Continue to inbox
            db_exit(db_connection)

        else:
            print("\nIncorrect password.\n")
