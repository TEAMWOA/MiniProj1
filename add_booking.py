from utility import *
import menus


def add_booking(db_connection, cursor, member_email):
    # list all rides offered by the user then select a ride to book a member
    # on
    #
    # username is the only match, and only show future rides 

    print_logo("Add Booking")

    user = (member_email,)
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
        
        #make a list of just the ride numbers
        for each in ride_matches:
            ride_numbers.append(each[0])
        while stop_list == False:
            
            #print the data max 5 times at a time
            print("\n{:^5}{:^7}{:^12}{:^5}{:^15}{:^5}{:^5}{:^20}{:^5}".format('rno','price','date','seats','lugDesc','src','dst','driver','cno'))
            for count, ride in enumerate(ride_matches):
                print("\n{:^5}{:^7}{:^12}{:^5}{:^15}{:^5}{:^5}{:^20}{:^5}".format(ride[0],ride[1],ride[2],ride[3],ride[4],ride[5],ride[6],ride[7],ride[8]))
                
                #5 at a time
                if (count == num_rides) or count > 0 and (count % 4) == 0:
                    
                    # get the input for a ride number 
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
        rno = prompt        
  
    #Check if the ride_number belongs to one of the users    
    for each in ride_matches:
            while not rno.isdigit() or int(rno) not in ride_numbers:
                rno = input("\nInvalid ride number, try again: ")
            
    rno = int(rno)
    
    #Check if the chosen ride is out of seats    
    cursor.execute("SELECT seats FROM rides where rno = ? ",(rno,))
    seats_available = cursor.fetchone()[0]
    print("\nRide Number: ", rno)
    print("\nSeats Available: ", seats_available)
    
    # if it is full, return a message asking to proceed
    if seats_available == 0:
        proceed = input("\nThis ride is full! Proceed?\n(yes/no)").strip()
        while proceed.lower not in ["no","yes"]:
            proceed= input("\nPlease enter yes or no: ").strip()        
        if proceed.lower() == 'no':
            add_booking(db_connection,cursor,member_email)
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
        cursor = db_connection.cursor()
        while not valid_user(member_to_book,cursor):
            member_to_book = input("\nInvalid Email, Enter another email: ").strip()
        
        #Get how many seats to book for the member
        #Check that they input an int only
        while True:
            seats_to_book = input("\nEnter the number of seats being booked: ").strip()

            try:
                # If we are over the seat limit
                if int(seats_to_book) > seats_available:
                    prompt = input("\nAttempting to overbook! Proceed?\n(yes/no): ").strip()
                    while prompt not in ('no', 'yes'):
                        prompt = input("\nPlease enter yes or no: ").strip()
                    if prompt.lower() == 'no':
                        add_booking(db_connection, cursor, member_email)
                    elif prompt.lower() == 'yes':
                        seats_to_book = int(seats_to_book)

                elif int(seats_to_book) == 0:
                    print("Can't book 0 seats.")

                elif int(seats_to_book) < 0:
                    print("Invalid number.")

                else:
                    seats_to_book = int(seats_to_book)
                    break
            except:
                continue
        
        #recieve the cost per seat and make sure a digit is put in
        # then change it into a float before putting in db
        valid_cost = False
        while valid_cost == False:
            try:
                cost_per_seat = input("\nEnter the cost per seat: ").strip()
                float(cost_per_seat)
                valid_cost = True
            except ValueError:
                cost_per_seat = print("\nInvalid Price!! Numbers only")
        
        #recieve the pickup code, then check for validity
        pickup = input("\nEnter the pickup location code: ").strip()
        while not valid_lcode(pickup,cursor):
            pickup = input("\nInvalid location code, try again: ").strip()
        
        # Recieve the dropff code, then check for validity
        dropoff = input("\nEnter the dropoff location code: ").strip()
        while not valid_lcode(dropoff,cursor):
            dropoff = input("\nInvalid location code, try again: ").strip()
        
        #The list of the new booking info    
        new_booking = (new_bno, member_to_book, rno , cost_per_seat, seats_to_book, pickup, dropoff,)
        
        # GEt final prompt from user
        prompt = input("\nConfirm Booking? (yes/no):   ").strip()
        while prompt not in ["yes","no"]:
            prompt= input("\nPlease enter yes or no: ").strip()
        if prompt == "yes":
        # Insert the new bookings into the table
            cursor.execute("INSERT INTO BOOKINGS VALUES(?,?,?,?,?,?,?)", new_booking)
            seats_left = (int(seats_available) - int(seats_to_book))
        
            # Then update the rides table and message the booked member
            updated_ride = (seats_left, rno,)
            cursor.execute("UPDATE rides SET seats = ? where rno = ?", updated_ride)
            

            message = "You have been booked on ride " + str(rno) + "."
            sender = member_email
            recipient = member_to_book
            message_member(db_connection, cursor, recipient, sender, message, rno)
            db_connection.commit()
            # after booking, prompt to make another one
            prompt = input("\nBooking Confirmed. Would you like to make another one?\n(yes/no): ").strip()
            
            while prompt not in ["yes","no"]:
                prompt= input("\nPlease enter yes or no: ").strip()            
            if prompt == "yes":
                add_booking(db_connection, cursor, member_email)
            elif prompt == "no":
                menus.main_menu(db_connection, cursor, member_email)
            elif prompt == "exit":
                menus.main_menu(db_connection,cursor,member_email)
        elif prompt == "no":
            add_booking(db_connection, cursor, member_email)
        
    return True
