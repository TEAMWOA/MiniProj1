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
        match_list = []
        master_list = []
        for each in prompt:
            keyword = "%" + each + "%"
            print(keyword)

            # a list of sequences for each possible match

            keyword = (keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword,)

            # execute query for each keyword

            cursor.execute(
                "SELECT distinct r.rno, r.price, r.rdate, r.seats, r.lugDesc,r.src, r.dst, r.driver, r.cno, c.make, c.model, c.year, c.seats FROM rides AS r LEFT OUTER JOIN enroute e on r.rno = e.rno LEFT OUTER JOIN locations l1 on r.src = l1.lcode LEFT OUTER JOIN locations l2 on r.dst = l2.lcode LEFT OUTER JOIN cars c on r.cno = c.cno WHERE r.src LIKE ? COLLATE NOCASE or r.dst LIKE ? COLLATE NOCASE or e.lcode LIKE ? COLLATE NOCASE or l1.lcode LIKE ? COLLATE NOCASE or l1.city LIKE ? COLLATE NOCASE or l1.prov LIKE ? COLLATE NOCASE or l1.address LIKE ? COLLATE NOCASE or l2.lcode LIKE ? COLLATE NOCASE or l2.city LIKE ? COLLATE NOCASE or l2.prov LIKE ? COLLATE NOCASE or l2.address LIKE ? COLLATE NOCASE GROUP BY r.rno;",
                keyword)

            # fetch all the matches for each keyword
            ride_matches = cursor.fetchall()
            
            if len(master_list) == 0:
                for each in ride_matches:
                    master_list.append(each)
            else:
                master_list[:] = [each for each in ride_matches if each in master_list]
                
        master_list = list(master_list)
        for each, ride in enumerate(master_list):
            ride = list(ride)
            master_list[each] = ride
            for each, value in enumerate(ride):
                if value is None:
                    ride[each] = ""
       
        stop_list = False
        print("\n{:^5}{:^5}{:^12}{:^5}{:^15}{:^6}{:^6}{:^20}{:^3}{:^10}{:^10}{:^4}{:^10}".format("rno", "price","date","seats","LugDesc","src","dst","driver","cno","make","model","year","seats"))
        while stop_list == False:
            for count, each in enumerate(master_list):
                print("\n{:^5}{:^5}{:^10}{:^5}{:^15}{:^6}{:^6}{:^20}{:^3}{:^10}{:^10}{:^4}{:^10}".format(each[0],each[1],each[2],each[3],each[4],each[5],each[6],each[7],each[8],each[9],each[10],each[11],each[12],))
                if (count == len(master_list)-1) or count > 0 and (count % 4) == 0:
                    prompt = input("\nEnter a ride number or return to see more: ").strip()
                    if prompt == "":
                        print("\n{:^5}{:^5}{:^12}{:^5}{:^15}{:^6}{:^6}{:^20}{:^3}{:^10}{:^10}{:^4}{:^10}".format("rno", "price","date","seats","LugDesc","src","dst","driver","cno","make","model","year","seats"))
                        continue
                    elif prompt.isdigit():
                        stop_list == True
                        message()
                    elif prompt == 'exit':
                        stop_list == True
                        exit()           
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
    valid_rno = False
    valid_cost = False
    ride_numbers = []
    
    # retrieve all FUTURE rides offered by the user
    cursor.execute("SELECT distinct r.rno, r.price, r.rdate, r.seats, r.lugDesc,r.src, r.dst, r.driver, r.cno FROM rides r WHERE driver = ? and rdate > date('now')", user)
    
    # fetch the ride matches
    ride_matches = cursor.fetchall()
    
    #  if there are none, tell the user, and ask if they want to offer a ride
    if not ride_matches:
        prompt = input("\nYou Have Not Offered Any Rides\nDo You Want To Offer A Ride?\nYes/No: ").strip()
        if prompt.strip() == 'yes':
            offer_ride()
        elif prompt.strip() == 'no':
            return False
    
    # Print all the ride matches 
    # make a list of ride_numbers for easier reference
    else:
        
        # print the rides one at a time
        ride_matches = list(ride_matches)
        for each, ride in enumerate(ride_matches):
            ride = list(ride)
            ride_matches[each] = ride
            for each, value in enumerate(ride):
                if value is None:
                    ride[each] = ""
                    
        stop_list = False
        print("\nHere Are Your Future Rides: \n")
        global num_rides
        num_rides = (len(ride_matches)-1)
        for each in ride_matches:
            ride_numbers.append(each[0])
        while stop_list == False:
            print("\n{:^5}{:^7}{:^12}{:^5}{:^15}{:^5}{:^5}{:^20}{:^5}".format('rno','price','date','seats','lugDesc','src','dst','driver','cno'))
            for count, ride in enumerate(ride_matches):
                print("\n{:^5}{:^7}{:^12}{:^5}{:^15}{:^5}{:^5}{:^20}{:^5}".format(ride[0],ride[1],ride[2],ride[3],ride[4],ride[5],ride[6],ride[7],ride[8]))
                if (count == num_rides) or count > 0 and (count % 4) == 0:
                    prompt = input("\nEnter a ride number or return to see more: ").strip()                
                    if prompt == "":
                        print("\n{:^5}{:^7}{:^12}{:^5}{:^15}{:^5}{:^5}{:^20}{:^5}".format(ride[0],ride[1],ride[2],ride[3],ride[4],ride[5],ride[6],ride[7],ride[8]))
                        continue
                    elif prompt == 'exit':
                        stop_list = True
                        exit()
                    elif prompt.isdigit():
                        stop_list = True
                        break
                        
                
            # User picks a ride they want to book on         
        choice = prompt        
  
    #Check if the ride_number belongs to one of the users    
    for each in ride_matches:
            while not choice.isdigit() or int(choice) not in ride_numbers:
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
        while prompt != 'no' or prompt!= 'yes':
            proceed= input("\nPlease enter yes or no: ").strip()        
        if proceed.lower() == 'no':
            add_booking()
        elif proceed.lower() == 'yes':
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
            seats_to_book = input("\nEnter the number of seats being booked: ").strip()
        
        
        # If we are over the seat limit
        if int(seats_to_book) > seats_available:
            prompt = input("\nAttempting to overbook! Proceed?\n(yes/no): ").strip()
            while prompt not in ('no','yes'):
                prompt = input("\nPlease enter yes or no: ").strip()
            if prompt.lower() == 'no':
                add_booking()
            elif prompt.lower() == 'yes':
                seats_to_book = int(seats_to_book)
        
        #recieve the cost per seat and make sure a digit is put in
        # then change it into a float before putting in db
        
        while valid_cost == False:
            try:
                cost_per_seat = input("\nEnter the cost per seat: ").strip()
                float(cost_per_seat)
                valid_cost == True
            except ValueError:
                cost_per_seat = print("\nInvalid Price!! Numbers only")
        
        #recieve the pickup code, then check for validity
        pickup = input("\nEnter the pickup location code: ").strip()
        while not valid_lcode(pickup):
            pickup = input("\nInvalid location code, try again: ").strip()
        
        # Recieve the dropff code, then check for validity
        dropoff = input("\nEnter the dropoff location code: ").strip()
        while not valid_lcode(dropoff):
            dropoff = input("\nInvalid location code, try again: ").strip()
        
        #The list of the new booking info    
        new_booking = (new_bno, member_to_book, choice , cost_per_seat, seats_to_book, pickup, dropoff,)
        
        # GEt final prompt from user
        prompt = input("\nConfirm Booking? (yes/no):   ").strip()
        while prompt != 'no' or prompt!= 'yes':
            prompt= input("\nPlease enter yes or no: ").strip()
        if prompt == "yes":
        # Insert the new bookings into the table
            cursor.execute("INSERT INTO BOOKINGS VALUES(?,?,?,?,?,?,?)", new_booking)
            seats_left = (int(seats_available) - int(seats_to_book))
        
            # Then update the rides table 
            updated_ride = (seats_left, ride_num,)
            cursor.execute("UPDATE rides SET seats = ? where rno = ?", updated_ride)
            
            # after booking, prompt to make another one
            prompt = input("\nBooking Confirmed. Would you like to make another one?\n(yes/no): ").strip()
            while prompt != 'no' or prompt!= 'yes':
                prompt= input("\nPlease enter yes or no: ").strip()            
            if prompt == "yes":
                add_booking()
            elif prompt == "no":
                logged_in_loop()
        elif prompt == "no":
            add_booking()
        
    return True
def cancel_booking():
    
    # Retreive all bookings on rides offered by current user and cancel
    # specified booking(s)
    
    email = "joe@gmail.com"
    user = (email,)
    
    valid_rno = False

    # retrieve all FUTURE bookings offered by the user
    cursor.execute("SELECT distinct bno, email, b.rno, cost, b.seats, pickup, dropoff  FROM rides r, bookings b WHERE driver = ? and rdate > date('now') and b.rno = r.rno", user)
    
    # fetch the bookings matches
    bookings = cursor.fetchall()
    booking_numbers = []
    
    #  if there are none, tell the user, and ask if they want to make a booking
    if not bookings:
        prompt = input("\nYou Have no rides booked. Would you like to add a booking?\nYes/No: ").strip()
        if prompt == 'yes':
            add_booking()
        elif prompt == 'no':
            logged_in_loop()
    
    # Print all the bookings 
    # make a list of booking numbers for easier reference
    else:
        #check for nonetypes and replace them with an empty string
        bookings = list(bookings)
        for each, booking in enumerate(bookings):
            booking = list(booking)
            bookings[each] = booking
            for each, value in enumerate(booking):
                if value is None:
                    booking[each] = ""
                  
        stop_list = False
        num_rides = (len(bookings)-1)
        for ride in bookings:
            booking_numbers.append(ride[0])        
        print("\nHere are the bookings on your rides: \n")
        while stop_list == False:
            print("\n{:^5}{:^15}{:^5}{:^7}{:^7}{:^10}{:^10}".format('bno','email','rno','cost','seats','pickup','dropoff'))
            for count, ride in enumerate(bookings):
                
                print("\n{:^5}{:^15}{:^5}{:^7}{:^7}{:^10}{:^10}".format(ride[0],ride[1],ride[2],ride[3],ride[4],ride[5],ride[6]))
                if (count == num_rides) or count > 0 and (count % 4) == 0:
                    prompt = input("\nEnter a booking to cancel or return to see more: ")                
                    if prompt == "":
                        print("\n{:^5}{:^15}{:^5}{:^5}{:^3}{:^6}{:^6}".format(ride[0],ride[1],ride[2],ride[3],ride[4],ride[5],ride[6]))
                        continue
                    elif prompt == 'exit':
                        stop_list = True
                        exit()
                    elif prompt.isdigit():
                        stop_list = True
                        break                
            
            
    # recieve the bookings number of booking to cancel
    # ensure it belongs to the user
    bno = prompt
    while not bno.isdigit() or int(bno) not in booking_numbers:
        booking_to_cancel = input("\nInvalid booking number, try again: ").strip()
        
    
    
    # get the number of seats that was booked on this ride
    booking_to_cancel = (bno,)
    cursor.execute("SELECT seats,email FROM bookings where bno = ?",(booking_to_cancel,))
    vacant_seats = cursor.fetchone()[0]
    bookee = cursor.fetchone()[1]
    
    
    print("\nCancelling this booking will free up", vacant_seats, "seats" )
    print(bookee, "will be notified of the cancellation")
    prompt = input("Cancel this booking? (yes/no): ")
    if prompt.lower == 'no':
        cancel_booking()
    elif prompt.lower() == 'yes':
        
        # get the number of seats still available and associated ride number
        cursor.execute("SELECT r.rno, r.seats FROM rides r, bookings b where bno = ? and r.rno = b.rno",(booking_to_cancel,))
        ride_info = cursor.fetchall()
        ride_num = ride_info[0][0]
        seats_available = ride_info[0][1]
        
        #Delete the booking for the table
        cursor.execute("DELETE FROM bookings WHERE bno = ?", (booking_to_cancel,))
        
        #Add the open seats back into the table
        seats_left =  int(seats_available) + int(vacant_seats)
        ride_info = (seats_left, ride_num,)
        cursor.execute("UPDATE rides SET seats = ? where rno = ? ",ride_info)
        cancellation_message = "\nYour booking on ride" + ride_num + "has been cancelled by the driver\n"
        
        print("\nBooking",booking_to_cancel,"has been cancelled")
        #message the member about their booking being cancelled
        if message_member(user,bookee,message,ride_num):
            print(bookee, "has been notified.")
        # ask if they want to cancel another bookings
        prompt = input("\nCancel another booking? (yes/no): ").split()
        if prompt == 'no':
            logged_in_loop()
        elif prompt == 'yes':
            cancel_booking()
        
    
    
    return True
def message_member(user, bookee, message, rno):
    
    sender = user
    email = bookee
    content = message
    seen = 'n'
    rno = rno
    
    new_message = (email,sender, content,rno,seen,)
    
    cursor.execute("INSERT INTO inbox VALUES(?,date('now'),?,?,?,? ", new_message)
    
    
    return True

def valid_user(member_to_book):
    valid_user = False
    user = (member_to_book,)
    cursor.execute("SELECT name from members where email = ? ",user)
    if cursor.fetchone():
        valid_user = True
        
    return valid_user

def valid_lcode(lcode):
    valid = False
    location = (lcode,)
    cursor.execute("SELECT address from locations where lcode = ? ", location)
    if cursor.fetchone():
        valid = True
    return valid


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

    ride_search()
    db_exit()


main()
