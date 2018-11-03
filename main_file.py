import sqlite3
import getpass
import os
from datetime import datetime, timedelta
import sys


def validate_date(date):
    # Checks whether the date is valid according to the format YYYY-MM-DD
    # Returns True if valid, False otherwise
    try:
        date = datetime.strptime(date, '%Y-%m-%d')
        if date >= (datetime.now() - timedelta(days=1)):
            return True
    except:
        return False


def clear_screen():
    # Function to clear the screen - less clutter
    os.system("clear")


def db_exit(db_connection):
    # Commits to database, closes connection and clears screen prior to quitting
    db_connection.commit()
    db_connection.close()
    clear_screen()
    quit()


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
        cursor.execute("SELECT * FROM members WHERE email=?;", [email])
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


def post_ride_request(cursor, member_email):
    # The member can post a ride request by providing a date, a pick up location code,
    # a drop off location code, and the amount willing to pay per seat.
    # The request id is set to a unique number automatically
    # Can return by pressing enter at any time (except for when entering amount)

    clear_screen()

    # Generate request id
    try:
        cursor.execute("SELECT MAX(rid) FROM requests;")
        rid = cursor.fetchone()[0] + 1
    except:
        rid = 1  # in case there are no ride requests in the database yet

    # Validate date
    # Date must match format YYYY-MM-DD and be in the future
    date = input("Date (YYYY-MM-DD): ")
    if len(date) == 0:
        return
    while not validate_date(date):
        print("Please enter a valid date.")
        date = input("Date (YYYY-MM-DD): ")
        if len(date) == 0:
            return

    # Get list of location codes
    location_codes = []
    cursor.execute("SELECT DISTINCT lcode FROM locations;")
    for row in cursor:
        location_codes.append(row[0])

    # Print all location codes
    print("\nLocation codes:")
    for i in range(len(location_codes)):
        if i % 7 == 0 and i // 7 > 0:
            print("{}".format(location_codes[i]), end="\n")
        else:
            print("{}".format(location_codes[i]), end=" ")
    print()

    # Validate pickup location
    pickup = input("Pickup location: ").lower()
    while pickup not in location_codes:
        if len(pickup) == 0:
            return
        pickup = input("Pickup location: ").lower()

    # Validate dropoff location (can't be the same as pickup)
    dropoff = input("Dropoff location: ").lower()
    while dropoff not in location_codes or dropoff == pickup:
        if len(dropoff) == 0:
            return
        dropoff = input("Dropoff location: ").lower()

    # Validate amount (non-negative integer)
    amount = -1
    while amount < 0:
        try:
            amount = int(input("Amount per seat: "))
        except:
            pass

    # Insert ride request into database
    cursor.execute("INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?);", [rid, member_email, date, pickup, dropoff, amount])
    return


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


def ride_search(cursor):
    # Searches for a ride
    # Keyword can match either the location code or substring of the city, province
    # or the address fields of the location
    # display all ride details and car details

    # recieve input from user and split using blankspace
    prompt = input("\nEnter keywords or 'exit': ").split()

    if prompt == "exit":
        return False
    else:
        # for each keyword given, make a sequence ins SQLite

        for each in prompt:
            keyword = "%" + each + "%"
            print(keyword)

            # a list of sequences for each possible match

            keyword = (keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword)

            # execute query for each keyword

            cursor.execute(
                "SELECT distinct r.rno, r.price, r.rdate, r.seats, r.lugDesc,r.src, r.dst, r.driver, r.cno, c.cno, c.make, c.model, c.seats, c.owner FROM rides AS r LEFT OUTER JOIN enroute e on r.rno = e.rno LEFT OUTER JOIN locations l1 on r.src = l1.lcode LEFT OUTER JOIN locations l2 on r.dst = l2.lcode LEFT OUTER JOIN cars c on r.cno = c.cno WHERE r.src LIKE ? or r.dst LIKE ? or e.lcode LIKE ? or l1.lcode LIKE ? or l1.city LIKE ? or l1.prov LIKE ? or l1.address LIKE ? or l2.lcode LIKE ? or l2.city LIKE ? or l2.prov LIKE ? or l2.address LIKE ? GROUP BY r.rno;",
                keyword)

            # fetch all the matches for each keyword
            ride_matches = cursor.fetchall()

            # if there is none, provide message and ask again

            if not ride_matches:
                print("\nNo Matches")
                ride_search(cursor)

            # if there are matches, list them 5 at a time

            else:
                print("\n")
                limit = 5
                i = 0
                j = 0
                num_matches = len(ride_matches)
                num_columns = len(ride_matches[0])
                while i < (num_matches - 1):

                    # If we've shown all results provide a message
                    # go back to main menu

                    if i == (num_matches - 1):
                        print("\nNo More Results")
                        break
                    elif j == (num_columns - 1):
                        break
                    else:

                        # print the first 5 results

                        while j < limit and prompt != "Exit":
                            try:
                                print(*ride_matches[j])
                                j += 1
                                i += 1
                            except IndexError:
                                print("\nNo More Results")
                                return False

                        # if there are more results, ask the user
                        # if they want to see more or exit the list

                        prompt = input("\nPress Enter For More or 'exit': ")

                        # if they press enter to see more
                        # increase the limit and list the next 5
                        # matches until all matches are listed

                        if len(prompt) == 0:
                            limit += 5
                            print("\n")

                        # if they exit the list, return to search prompt
                        elif prompt == "exit":
                            ride_search(cursor)

    return True


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


def login(db_connection, cursor):
    # Gets email / password from user, verifies it
    clear_screen()

    while True:
        while True:
            email = input("Enter email or press enter to return: ").lower()
            if email == '':
                return
            else:
                cursor.execute("SELECT pwd FROM members WHERE email=?;", [email])

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


def inbox(db_connection, cursor, member_email):
    # Displays the user's unread messages
    clear_screen()

    # Gets all messages sent to user, creates list of unread messages
    unread_messages = []
    cursor.execute("SELECT * FROM inbox WHERE email=?;", [member_email])
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


def main():
    # Setup connection to database
    if len(sys.argv) != 2:
        print("Please pass the database file as a command line argument (dbname.db)")
        exit()

    path = "./{}".format(sys.argv[1])
    db_connection = sqlite3.connect(path)
    cursor = db_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    db_connection.commit()

    # Start user at login menu
    login_menu(db_connection, cursor)
    db_exit(db_connection)


if __name__ == "__main__":
    main()
