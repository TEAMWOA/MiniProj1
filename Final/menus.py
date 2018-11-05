# Menus
# (1) Login/SignUp [authentications]
# (2) MainMenu
# (3) Inbox
#
from requests import *
from rides import *
from authentication import *
from utility import *
from add_booking import *
from cancel_booking import *

import time #time delay


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

        print("1. Login")
        print("2. Register")
        print("3. Exit")

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
                #db_exit()
        
            elif choice.upper() == "EXIT":
                db_exit(db_connection)
                #db_exit()
            
            else:
                print("\n\n*** < {} > is not a menu option. Try again\n*** ".format(choice)) #will show the user what they inputted wrong
                continue


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
        print("> Select a number option from the menu <\n")
    
        print("\n> Select a number option from the menu\n< Type EXIT to end the program >\n")
        # print("R I D E S ")
        print("1. Search for Rides")
        print("2. Post Ride Request")
        print("3. (UNIMPLEMENTED) Offer Ride")
        #print("R E Q U E S T S")
        print("4. (UNIMPLEMENTED) Search for Ride Requests")
        print("5. (UNIMPLEMENTED) Delete Ride Requests")
        print("6. Cancel Ride Booking")
        print("7. Book Member on a Ride")
        print("8. Inbox")
        print("9. Logout")
        print("10. Exit")

        # Validate input
        choice = input()
        while choice not in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "EXIT"):
            choice = input()

        if choice == "1":
            ride_search(cursor)
            
        elif choice == "2":
            post_ride_request(db_connection, cursor, member_email)

        elif choice == "3":
            # offer_ride()
            pass

        elif choice == "4":
            # request_search()
            pass

        elif choice == "5":
            # delete_request()
            pass

        elif choice == "6":
            cancel_booking(db_connection, cursor, member_email)

        elif choice == "7":
            add_booking(db_connection, cursor, member_email)

        elif choice == "8":
            check_inbox(db_connection, cursor, member_email)

        elif choice == "9":
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

        elif choice == "10":
            db_exit(db_connection)
            
        elif(choice.upper() == "EXIT"):
            db_exit(db_connection)
        
        else:
            clear_screen()
            print("\n\n*** < {} > is not a menu option. Try again\n*** ".format(choice)) #will show the user what they inputted wrong

def inbox(db_connection, cursor, member_email):
    # Displays the user's unread messages
    # clear_screen()

    print("\n")
    print("    #######################")
    print("    ####               ####")
    print("    ###      INBOX      ###")
    print("    ####               ####")
    print("    #######################\n\n")
    print("> Select a number option from the menu\n< Type EXIT to end the program >\n")

    print("1. Unread Messages")
    print("2. All Messages")
    print("3. Main Menu")
    print("4. Logout")
    print("5. Exit")

    # Validate input
    while True:
        choice = input()

        if choice == "1":
            show_messages(db_connection, cursor, member_email, True)

        elif choice == "2":
            show_messages(db_connection, cursor, member_email, False)

        elif choice == "3":
            main_menu(db_connection, cursor, member_email)

        elif choice == "4":
            login_menu(db_connection, cursor)

        elif choice == "5":
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
            db_exit(db_connection)

        elif choice.upper() == "EXIT":
            db_exit(db_connection)

        else:
            print("\n\n*** < {} > is not a menu option. Try again\n*** ".format(
                choice))  # will show the user what they inputted wrong
            continue


def show_messages(db_connection, cursor, member_email, unread_only):
    # clear_screen()

    print("\n")
    print("    #######################")
    print("    ####               ####")
    print("    ###      INBOX      ###")
    print("    ####               ####")
    print("    #######################\n\n")

    # Gets all messages sent to user, creates list of unread messages
    messages = []
    cursor.execute("SELECT * FROM inbox WHERE email = ? COLLATE NOCASE;", [member_email])
    for row in cursor:
        email, timestamp, sender, content, rno, seen = row
        if not (seen == 'n' and unread_only):
            messages.append([timestamp, sender, content, rno])

    # Prints all unread messages
    if len(messages) > 0:
        for message in messages:
            print("{:<15}      {:>19}".format(message[1], message[0]))
            print("Regarding ride #{}".format(message[3]))
            print(message[2])
            print()

            cursor.execute("UPDATE inbox SET seen = y WHERE email = ? COLLATE NOCASE;", [member_email])
            db_connection.commit()

        input("Press enter to return to inbox.")
        inbox(db_connection, cursor, member_email)
    else:  # No unread messages - continue straight to main menu
        inbox(db_connection, cursor, member_email)

