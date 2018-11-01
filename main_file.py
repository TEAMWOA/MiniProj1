import sqlite3
import getpass


def db_exit():
    # Commits to database and closes connection before quitting

    connection.commit()
    connection.close()
    quit()
    
def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    connection.commit()
    return


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
    
    # make email global so we can access it 
    global email
    
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

            keyword = (keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword,)

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



def add_booking():
    
    # list all rides offered by the user then select a ride to book a member
    # on
    #
    # username is the only match, and only show future rides
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()   
    
    user = 'joe@gmail.com'
    user = (user,)
    
    # retrieve all FUTURE rides offered by the user
    cursor.execute("SELECT distinct r.rno, r.price, r.rdate, r.seats, r.lugDesc,r.src, r.dst, r.driver, r.cno FROM rides r WHERE driver = ? and rdate > date('now')", user)
    
    # fetch the ride matches
    ride_matches = cursor.fetchall()
    ride_numbers = []
    
    #  if there are none, tell the user, and ask if they want to offer a ride
    if not ride_matches:
        prompt = input("\nYou Have Not Offered Any Rides\nDo You Want To Offer A Ride?\nYes/No: ")
        if prompt.strip() == 'yes':
            offer_ride()
        elif prompt.strip() == 'no':
            return False
    
    # Print all the ride matches 
    # make a list of ride_numbers for easier reference
    else:
        
        print("\nHere Are Your Future Rides: \n")
        for each in ride_matches:
            print(*each)
            ride_numbers.append(each["rno"])
            
    
    # User picks a ride they want to book on         
    choice = (input("\nEnter The Ride Number To Book or Enter to see more: "))
    
    
    #will only accept integer for ride number matches
    while not choice.isdigit():
        choice = (input("\nEnter The Ride Number To Book or Enter to see more: "))
        
    #Check if the ride_number belongs to one of the users    
    for each in ride_matches:
        while int(choice) not in ride_numbers:
            choice = input("\nInvalid ride number, try again: ")
            
    ride_num = int(choice)
    
    #Check if the chosen ride is out of seats    
    cursor.execute("SELECT seats FROM rides where rno = ? ",(ride_num,))
    seats_available = cursor.fetchone()[0]
    print("\nRide Number: ", ride_num)
    print("\nSeats Available: ", seats_available)
    
    # if it is full, return a message asking to proceed
    if seats_available == 0:
        proceed = ("\nThis ride is full! Proceed?\n(yes/no)").strip()
        if proceed == 'no':
            add_booking()
        elif proceed == 'yes':
            pass
   
    #If there are available seats, create new bookings number
    # and start collecting booking data    
    elif seats_available > 0:
        cursor.execute("SELECT MAX(bno) from bookings")
        old_bno = cursor.fetchone()[0]
        new_bno = old_bno + 1
        
        #to check for a valid user
        member_to_book = input("\nEnter member's email to book: ").strip()
        while not valid_user(member_to_book):
            member_to_book = input("\nInvalid Email, Enter another email: ").strip()
        
        #Get how many seats to book for the member
        #Check that they input an int only
        seats_to_book =input("\nHow many seats are being booked? ").strip()
        while not seats_to_book.isdigit():
            seats_to_book = input("\nEnter the number of seats being booked: ")
        
        
        # If we are over the seat limit
        if int(seats_to_book) > seats_available:
            prompt = input("\nAttempting to overbook! Proceed?\n(yes/no): ")
            if prompt == 'no':
                add_booking()
            elif prompt == 'yes':
                seats_to_book = int(seats_to_book)
        
        #recieve the cost per seat and make sure a digit is put in
        # then change it into a float before putting in db
        
        cost_per_seat = input("\nEnter the cost per seat: ")
        while not cost_per_seat.isdigit():
            
            cost_per_seat = input("\nEnter the cost per seat: ")
        
        #recieve the pickup code, then check for validity
        pickup = input("\nEnter the pickup location code: ")
    
        while not valid_lcode(pickup):
            pickup = input("\nInvalid location code, try again: ")
        
        # Receieve the dropff code, then check for validity
        dropoff = input("\nEnter the dropoff location code: ")
        while not valid_lcode(dropoff):
            dropoff = input("\nInvalid location code, try again: ")
        
        #The list of the new booking info    
        new_booking = (new_bno, member_to_book, choice , cost_per_seat, seats_to_book, pickup, dropoff,)
        
        # GEt final prompt from user
        prompt = input("\nConfirm Booking? (yes/no):   ").strip()
        if prompt == "yes":
        # Insert the new bookings into the table
            cursor.execute("INSERT INTO BOOKINGS VALUES(?,?,?,?,?,?,?)", new_booking)
            seats_left = (int(seats_available) - int(seats_to_book))
        
            # Then update the rides table 
            updated_ride = (seats_left, ride_num,)
            cursor.execute("UPDATE rides SET seats = ? where rno = ?", updated_ride)
            
            # after booking, prompt to make another one
            prompt = input("\nBooking Confirmed. Would you like to make another one?\n(yes/no): ").strip()
            if prompt == "yes":
                add_booking()
            elif prompt == "no":
                logged_in_loop()
        elif prompt == "no":
            add_booking()
        

       
    return True
def valid_user(member_to_book):
    valid = False
    user = (member_to_book,)
    cursor.execute("SELECT name from members where email = ? ",user)
    if cursor.fetchone():
        valid = True
        
    return valid

def valid_lcode(lcode):
    valid = False
    location = (lcode,)
    cursor.execute("SELECT address from locations where lcode = ? ", location)
    if cursor.fetchone():
        valid = True
    return valid

def cancel_booking():
    
    # Retreive all bookings on rides offered by current user and cancel
    # specified booking(s)
    
    return


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
        print("3. Create/Cancel Bookings")
        print("4. Logout")
        print("5. Quit")

        choice = input()

        while choice not in ("1", "2", "3", "4", "5"):
            choice = input()

        if choice == "1":
            post_ride_request()

        elif choice == "2":
            ride_search()
        
        elif choice == "3":
            add_booking()

        elif choice == "4":
            login_loop()

        elif choice == "5":
            db_exit()


def main():
    path = "./rideshare.db"
    connect(path)

    add_booking()

    db_exit()


main()
