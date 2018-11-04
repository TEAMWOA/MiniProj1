# Authentication
# (1) register(db_connection, cursor)
# (2) login(db_connection, cursor)
#
#

import getpass

from menus import *
from utility import *


def register(db_connection, cursor):
    # Gets email, name, phone, password from user
    # If no account registered under that email, creates entry in members table
    # User can return to the login menu by pressing enter at any time

    clear_screen()
    while True:
        # Validate email
        email = input("Enter email (15 Character Limit) or press enter to return: ").lower()
        while len(email) > 15:
            email = input("Enter email (15 Character Limit) or press enter to return: ").lower()
        if len(email) == 0:
            return

        # Make sure no account exists registered to that email
        cursor.execute("SELECT * FROM members WHERE email=? COLLATE NOCASE;", [email])
        if len(cursor.fetchall()) != 0:  # If len != 0 then an account is already registered under that email
            print("\nAccount already registered with that email.\n")

        # Email is valid
        else:
            # Validate name
            name = input("Name (20 Character Limit): ")
            while len(name) > 20:
                name = input("Name (20 Character Limit): ")
            if len(name) == 0:
                return

            # Validate phone
            phone = input("Phone (XXX-XXX-XXXX): ")
            while len(phone) > 12:
                phone = input("Phone (XXX-XXX-XXXX): ")
            if len(phone) == 0:
                return

            # Validate password - also hides input
            password = getpass.getpass("Password (6 Character Limit): ")  # Hides input
            while len(password) > 6:
                password = getpass.getpass("Password (6 Character Limit): ")
            if len(password) == 0:
                return

            # Adds newly created account to members table
            cursor.execute("INSERT INTO members VALUES (?, ?, ?, ?);", [email, name, phone, password])
            break

    # Continue to main menu (No messages to see for a newly created account)
    main_menu(db_connection, cursor, email)
    db_exit(db_connection)


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
                #login_menu(db_connection, cursor) # THIS ISNT WORKING FOR SOME REASON
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
            inbox(db_connection, cursor, email)  # Continue to inbox
            db_exit(db_connection)

        else:
            print("\nIncorrect password.\n")
