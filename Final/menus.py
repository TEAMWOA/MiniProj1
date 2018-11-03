from requests import *
from rides import *
from authentication import *
from utility import *


def login_menu(db_connection, cursor):
    # First menu user encounters, allows for logging in, registering a new account and exiting
    while True:
        clear_screen()

        print("Please choose an option:\n")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        # Validate input
        choice = input()
        while choice not in ("1", "2", "3"):
            choice = input()

        if choice == "1":
            login(db_connection, cursor)

        elif choice == "2":
            register(db_connection, cursor)

        elif choice == "3":
            db_exit(db_connection)


def main_menu(db_connection, cursor, member_email):
    # Main menu
    while True:
        clear_screen()

        print("Please choose an option:\n")
        print("1. Post Ride Request")
        print("2. Search for Rides")
        print("3. Logout")
        print("4. Exit")

        # Validate input
        choice = input()
        while choice not in ("1", "2", "3", "4"):
            choice = input()

        if choice == "1":
            post_ride_request(cursor, member_email)

        elif choice == "2":
            ride_search(cursor)

        elif choice == "3":
            login_menu(db_connection, cursor)

        elif choice == "4":
            db_exit(db_connection)


def inbox(db_connection, cursor, member_email):
    # Displays the user's unread messages
    clear_screen()

    # Gets all messages sent to user, creates list of unread messages
    unread_messages = []
    cursor.execute("SELECT * FROM inbox WHERE email=? COLLATE NOCASE;", [member_email])
    for row in cursor:
        email, timestamp, sender, content, rno, seen = row
        if seen == 'n':
            unread_messages.append([timestamp, sender, content, rno])

    # Prints all unread messages
    if len(unread_messages) > 0:
        for message in unread_messages:
            print("{:<15}      {:>19}".format(message[1], message[0]))
            print("Regarding ride #{}".format(message[3]))
            print(message[2])
            print()

        # Uncomment when done testing
        # cursor.execute("UPDATE inbox SET seen='y' WHERE email=?;", [member_email])

        input("Press enter to continue to main menu.")
        main_menu(db_connection, cursor, member_email)
    else:  # No unread messages - continue straight to main menu
        main_menu(db_connection, cursor, member_email)
