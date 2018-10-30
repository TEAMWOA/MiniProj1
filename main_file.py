import sqlite3
import getpass


def db_exit():
    # Commits to database and closes connection before quitting

    connection.commit()
    connection.close()
    quit()


def login():
    # Gets email / password from user, verifies it
    # If login is successful, returns True and initializes global variable "user", containing the user's email
    # If login unsuccessful returns False

    # Get and validate email
    email = input("\nEmail: ")
    cursor.execute("SELECT pwd FROM members WHERE email=?;", [email])

    try:
        # Get password associated to email entered
        correct_password = cursor.fetchone()[0]

    except TypeError:   # TypeError when the email entered doesn't exist in the database
        print("\nNo account registered under that email.")
        return False

    password = getpass.getpass("Password: ")    # Hides input

    if password == correct_password:
        # User global variable necessary for other functions (e.g. post request requires the posters email)
        global user
        user = email
        print("\nSuccessfully logged in.")
        return True

    else:
        print("\nIncorrect password.")
        return False


def register():
    # Gets email, name, phone, password from user
    # If no account registered under that email, creates entry in members table
    # If registration successful, returns True and initializes global variable "user", containing the user's email
    # Otherwise returns False

    # Get and validate email
    email = input("\nEmail: ").lower()
    while len(email) > 15:
        email = input("\nEmail (15 Character Limit): ").lower()

    # Make sure no account exists registered to that email
    cursor.execute("SELECT * FROM members WHERE email=?;", [email])
    if len(cursor.fetchall()) != 0:     # If len != 0 then an account is already registered under that email
        print("\nAccount already registered with that email.")
        return False

    else:
        name = input("Name: ")
        while len(name) > 20:
            name = input("Name (20 Character Limit): ")

        phone = input("Phone (XXX-XXX-XXXX): ")
        while len(phone) > 12:
            name = input("Phone (XXX-XXX-XXXX): ")

        password = getpass.getpass("Password: ")    # Hides input
        while len(password) > 6:
            password = getpass.getpass("Password (6 Character Limit): ")

        cursor.execute("INSERT INTO members VALUES (?, ?, ?, ?);", [email, name, phone, password])  # Registers account

        print("\nSuccessfully registered.")

        global user
        user = email

        return True


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    connection.commit()
    return


def post_ride_request():
    # Post ride requests.
    # The member should be able to post a ride request by providing a date, a pick up location code,
    # a drop off location code, and the amount willing to pay per seat.
    # The request rid is set by your system to a unique number and the email is set to the email address of the member.

    cursor.execute("SELECT MAX(rid) FROM requests;")
    rid = cursor.fetchone()[0] + 1

    email = user

    date = input("Date (YYYY-MM-DD): ")
    pickup = input("Pickup location: ").lower()
    dropoff = input("Dropoff location: ").lower()
    amount = int(input("Amount per seat: "))

    cursor.execute("INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?);", [rid, email, date, pickup, dropoff, amount])

    print("\nSuccessfully posted request.")

    return True


def ride_search():
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
                ride_search()

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
                            ride_search()

    return True


def login_loop():
    while True:
        print("\nPlease choose an option:")
        print("1. Login")
        print("2. Register")
        print("3. Quit")

        choice = input()

        while choice not in ("1", "2", "3"):
            choice = input()

        if choice == "1":
            if login():
                logged_in_loop()   # Continue to second loop once successfully logged in

        elif choice == "2":
            if register():
                logged_in_loop()   # Continue to second loop once successfully registered

        elif choice == "3":
            db_exit()


def logged_in_loop():
    # Second loop - post ride request, quit
    cont = True
    while cont:
        print("\nPlease choose an option:")
        print("1. Post Ride Request")
        print("2. Search for Rides")
        print("3. Logout")
        print("4. Quit")

        choice = input()

        while choice not in ("1", "2", "3", "4"):
            choice = input()

        if choice == "1":
            post_ride_request()

        elif choice == "2":
            ride_search()

        elif choice == "3":
            login_loop()

        elif choice == "4":
            db_exit()


def main():
    path = "./rideshare.db"
    connect(path)

    login_loop()

    db_exit()


main()
