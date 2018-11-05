from utility import *


def cancel_booking(db_connection, cursor, member_email):
    
    # Retreive all bookings on rides offered by current user and cancel
    # specified booking(s)
    
    user = (member_email,)
    
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
        bno = input("\nInvalid booking number, try again: ").strip()
        
    bno = int(bno)
    
    # get the number of seats that was booked on this ride
    cursor.execute("SELECT seats, email, rno FROM bookings where bno = ?",(bno,))
    ride = cursor.fetchone()
    vacant_seats = ride[0]
    recipient = ride[1]
    rno = ride[2]
    
    
    print("\nCancelling this booking will free up", vacant_seats, "seat(s).\n" )
    print(recipient, "will be notified of the cancellation.\n\n")
    prompt = input("Cancel this booking? (yes/no): ")
    if prompt.lower == 'no':
        cancel_booking()
    elif prompt.lower() == 'yes':
        
        # get the number of seats still available and associated ride number
        cursor.execute("SELECT r.rno, r.seats FROM rides r, bookings b where bno = ? and r.rno = b.rno",(bno,))
        ride_info = cursor.fetchall()
        ride_num = ride_info[0][0]
        seats_available = ride_info[0][1]
        
        #Delete the booking for the table
        cursor.execute("DELETE FROM bookings WHERE bno = ?", (bno,))
        
        #Add the open seats back into the table
        seats_left =  int(seats_available) + int(vacant_seats)
        ride_info = (seats_left, ride_num,)
        cursor.execute("UPDATE rides SET seats = ? where rno = ? ",ride_info)
        print("\nBooking",bno,"has been cancelled")
        
        #message the member about their booking being cancelled
        sender = member_email
        recipient = recipient
        message = "Your booking on ride" + str(ride_num) + "has been cancelled by the driver"
        rno = rno
        if message_member(db_connection,cursor, recipient, sender, message, rno):
            print(recipient, "has been notified.")
        db_connection.commit()
        # ask if they want to cancel another bookings
        prompt = input("\nCancel another booking? (yes/no): ").split()
        if prompt == 'no':
            exit()
        elif prompt == 'yes':
            cancel_booking(db_connection,cursor, member_email)
        
    return True
    
