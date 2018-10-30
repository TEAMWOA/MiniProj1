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
    email = input("\nEmail: ").lower()
    cursor.execute("SELECT pwd FROM members WHERE email=?;", [email])

    try:
        # Get password associated to email entered
        correct_password = cursor.fetchone()[0]

    except TypeError:   # TypeError when the email entered doesn't exist in the database
        print("\nNo account registered under that email.")
        return False

    password = getpass.getpass("Password: ")    # Hides input

    if password == correct_password:
        # User global variable necessary for other functions (e.g. post request requires the poster's email)
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

    email = input("\nEmail: ").lower()
    while len(email) > 15:
        email = input("\nEmail (15 Character Limit): ").lower()

    cursor.execute("SELECT * FROM members WHERE email=?;", [email])
    if len(cursor.fetchall()) != 0:     # If len != 0 then an account is already registered under that email
        print("\nAccount already registered under that email.")
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


def main():
    path = "./rideshare.db"
    connect(path)

    # First loop - login, register account, quit
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
                break   # Continue to second loop once successfully logged in

        elif choice == "2":
            if register():
                break   # Continue to second loop once successfully registered

        elif choice == "3":
            db_exit()

    # Second loop - post ride request, quit
    cont = True
    while cont:
        print("\nPlease choose an option:")
        print("1. Post Ride Request")
        print("2. Quit")

        choice = input()

        while choice not in ("1", "2"):
            choice = input()

        if choice == "1":
            post_ride_request()

        elif choice == "2":
            db_exit()

    db_exit()


main()
