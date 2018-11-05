# Ride Request Handling 
#
# 1. post_ride_request(cursor, member_email)
# 2. deleteRequest(db_connection, row, displayedRequests)
# 3. searchRideRequests(db_connection, cursor, member_email)
# 4. searchAndDeleteRequest(db_connection, cursor, member_email)
# 5. searchKeyWordRequest(db_connection, member_email, cursor)
# 6. messageMember(db_connection, row, member_email, displayedResults)
#
#

import datetime
import menus
from time import sleep
from utility import *

################################################################
#
# 1. Post Ride Requests
#
def post_ride_request(db_connection, cursor, member_email):
    # The member can post a ride request by providing a date, a pick up location code,
    # a drop off location code, and the amount willing to pay per seat.
    # The request id is set to a unique number automatically
    # Can return by pressing enter at any time (except for when entering amount)

    clear_screen()

    print("\n")
    print("    ##########################")
    print("    ####                  ####")
    print("    ### Post Ride Requests ###")
    print("    ####                  ####")    
    print("    ##########################\n\n")

    # Generate request id
    try:
        cursor.execute("SELECT MAX(rid) FROM requests;")
        rid = cursor.fetchone()[0] + 1
    except:
        rid = 1  # in case there are no ride requests in the database yet

    # Validate date
    # Date must match format YYYY-MM-DD and be in the future
    date = input("  Date (YYYY-MM-DD): ")
    if len(date) == 0:
        return
    while not will_validate_date(date):
        print("  Please enter a valid date.")
        date = input("  Date (YYYY-MM-DD): ")
        if len(date) == 0:
            return

    # Get list of location codes
    location_codes = []
    cursor.execute("SELECT DISTINCT lcode FROM locations;")
    for row in cursor:
        location_codes.append(row[0])

    # Print all location codes
    print("\n  Location codes:")
    for i in range(len(location_codes)):
        if i == 0:
            print("  ", end="")
        if i % 7 == 0 and i // 7 > 0:
            print("{}".format(location_codes[i]), end="\n  ")
        else:
            print("{}".format(location_codes[i]), end=" ")
    print()

    # Validate pickup location
    pickup = input("  Pickup location: ").lower()
    while pickup not in location_codes:
        print("Please enter a valid pickup location.")
        pickup = input("  Pickup location: ").lower()

    # Validate dropoff location (can't be the same as pickup)
    dropoff = input("  Dropoff location: ").lower()
    while dropoff not in location_codes:
        print("Please enter a valid dropoff location.")
        dropoff = input("\n  Dropoff location: ").lower()

    # Validate amount (non-negative integer)
    amount = -1
    while amount < 0:
        try:
            amount = int(input("  Amount per seat: "))
        except:
            continue

    # print(rid, member_email, date, pickup, dropoff, amount)
    # Insert ride request into database
    cursor.execute("INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?);", [rid, member_email, date, pickup, dropoff, amount])
    db_connection.commit()

    print("\n. .. . .. Request successfully posted!.")
    sleep(1.5)

    menus.main_menu(db_connection, cursor, member_email)

################################################################
#
# 2. Delete Ride Requests
#
def deleteRequest(db_connection, row, displayedRequests):
    #deletes a row in the request table 

    cursor = db_connection.cursor()
    request = displayedRequests[row]

    while(1):
        print("\n> Confirm request deletion (y/n)")
        choice = input()
        if choice.upper() == 'Y':
            break #continue with deletion

        elif choice.upper() == 'N':
            print('***\n*** Not deleting request.\n***\n')
            sleep(1)
            return

        else:
            print("***\n*** Invalid menu option. (y/n)\n***")

    print("> Deleting request.. . .  . . ..")
    sleep(1)
    print("\n.. . .  . . .. Request deleted")
    sleep(1.5)

    #cursor.execute = ("DELETE FROM requests WHERE rid = '{}'").format(request[0])
    cursor.execute("DELETE FROM requests WHERE rid ==?;",[request[0]] )
    db_connection.commit()
    return
    
#########################################################   
# 
# 3. Search Ride Requests
#
def searchRideRequests(db_connection, cursor, member_email):

    cursor.execute("SELECT * FROM requests WHERE email ==? COLLATE NOCASE;", [member_email])
    result = cursor.fetchall()
    #print(result)
    
    
    if len(result) == 0:
        print("***\n*** You have no requests\n***")
        sleep(2)
        return # goes back to searchandeleterequest menu 

    while len(result) != 0:
        #print out 5 results at a time
        displayedRequests = [] #will hold the requests currently displayed on the screen

        print("Your ride requests .... ")
        for i in range(1,6):
            if len(result) == 0:
                break

            request = result.pop()
            displayedRequests.append(request)
            #show 5 results
            print(("\n  [{}]  rid: {}\n       Email: {}\n       RequestDate: {}\n       Pickup: {}\n       Dropoff: {}\n       Amount: {}\n").format(i, request[0], request[1], request[2], request[3], request[4], request[5]))
        
        #type more to see more results or enter request number to delete
        if len(result) != 0:
            print("< Type MORE to see more requests or select the index number to delete the request >")
            choice = input()
            if choice.upper() == 'EXIT': #IF the user wants to exit
                db_exit(db_connection) #QUIT

            elif choice.upper() == 'BACK':
                return #return to main request screen

            elif choice.upper() == 'MORE':
                continue 

            elif '1' <= choice <= '5':
                #delete the request
                deleteRequest(db_connection, int(choice) - 1, displayedRequests)
                return #return to main request screen

            else: #invalid input
                print("***\n*** Incorrect entry. Try again\n***")
                sleep(1)
                return

    # all requests were printed.....
    print("\n< No more requests. Select the index number to delete the request >")
    print("< Type EXIT to end the program or BACK/press ENTER to go back to the Search&DeleteRequest Menu >")
    choice = input()
    if choice.upper() == 'EXIT':  # IF the user wants to exit
        db_exit(db_connection)

    elif choice.upper() == 'BACK': #return to request selection screen
        return

    elif choice.upper() == "":
        return 
     
    elif '1' <= choice <= str(len(displayedRequests)): #may not be 5 displayed requests
        deleteRequest(db_connection, int(choice) - 1, displayedRequests)
        return  # return to main request selection screen

    return

################################################################
#    
# 4. search and delete ride requests (menu)
#

def searchAndDeleteRequest(db_connection, cursor, member_email):    
    while(1):
        clear_screen()
        print("\n")
        print("    ############################")
        print("    ####                    ####")
        print("    ### Search&DeleteRequest ###")
        print("    ####                    ####")    
        print("    ############################\n\n")
        print("< Type EXIT to end the program or BACK/press ENTER to go back to the Main Menu >\n")
        print("   1. View/delete ride requests\n   2. Search for requests by lcode or city *and* message other member\n")
        print
        choice = input()

        if choice.upper() == 'EXIT': #IF the user wants to exit
            db_exit(db_connection)

        elif choice.upper() == 'BACK': #return user to main menu
            menus.main_menu(db_connection, cursor, member_email)
        
        elif choice == "":
            menus.main_menu(db_connection, cursor, member_email)
            
        elif choice == '1':
            searchRideRequests(db_connection, cursor, member_email)

        elif choice == '2':
            searchKeyWordRequest(db_connection, member_email, cursor)
        
#         elif choice == '3':
#             messageMember(db_connection, member_email, cursor)

        else:
            print("***\n*** Invalid menu option. Try again\n***")
            continue   


################################################################
#    
# 5. searchKeyWordRequest(db_connection, member_email, cursor)
#
#    
def searchKeyWordRequest(db_connection, member_email, cursor):
    
    print("< Enter a pickup lcode or a city to see the ride requests >")
    print("< Note: requests queried by lcode or city does not include your requests >")
    choice = input()
    
    if choice.upper() == 'EXIT':  # exit
        db_exit(db_connection)

    elif choice.upper() == 'BACK': #return to request selection screen
        return
        
    elif choice.upper() == "":
        return 
        
    #QUERY
    else:
        cursor.execute("SELECT rid, email, rdate, l1.city, l2.city, amount FROM requests, locations l1, locations l2  WHERE ((l1.lcode LIKE ?) OR (l1.city LIKE ?)) AND l1.lcode = pickup AND l2.lcode = dropoff AND email <> ? COLLATE NOCASE;", [choice, choice, member_email])
        #     cursor.execute("SELECT * FROM requests WHERE email ==? COLLATE NOCASE;", [member_email])
        result = cursor.fetchall() 
        #print(result)
        if len(result) == 0:
            print("***\n*** There are no requests\n***")
            sleep(1)
            return # back to menu

        while len(result) != 0:
            # print out 5 results at a time
            displayedRequests = []  # will hold the requests currently displayed on the screen
            for i in range(1, 6):
                if len(result) == 0:
                    break
                    
                request = result.pop()
                displayedRequests.append(request)
                #show 5 results 
                print(("\n  [{}]  rid: {}\n       Email: {}\n       RequestDate: {}\n       Pickup: {}\n       Dropoff: {}\n       Amount: {}\n").format(i, request[0], request[1], request[2], request[3], request[4], request[5]))
            #type more to see more results or enter request number to delete
            if len(result) != 0:
                print("< Type MORE to see more requests or select the index number to delete the request >")
                choice = input()
                if choice.upper() == 'EXIT': #IF the user wants to exit
                    db_exit(db_connection) #QUIT

                elif choice.upper() == 'BACK':
                    return #return to main request screen

                elif choice.upper() == 'MORE':
                    continue 

                elif '1' <= choice <= '5':
                    #MESSAGE MEMBER
                    messageMember(db_connection, int(choice) - 1, member_email, displayedRequests)
                    return #return to main request screen

                else: #invalid input
                    print("***\n*** Incorrect entry. Try again\n***")
                    sleep(1.3)
                    return

        # all requests were printed.....
        print("\n< No more requests. Select the index number to send a message to the posting member >")
        print("< Type EXIT to end the program or BACK/press ENTER to go back to the Search&DeleteRequest Menu >")
        choice = input()
        if choice.upper() == 'EXIT':  # IF the user wants to exit
            db_exit(db_connection)

        elif choice.upper() == 'BACK': #return to request selection screen
            return

        elif choice.upper() == "":
            return 
 
        elif '1' <= choice <= str(len(displayedRequests)): #may not be 5 displayed requests
            #MESSAGE MEMBER
            messageMember(db_connection, int(choice) - 1, member_email, displayedRequests)
            return  # return to main request selection screen

        return
 
 ################################################################
#    
# 6. message member (db_connection, member_email, cursor)
#
#    

def messageMember(db_connection, row, member_email, displayedRequests):

    cursor = db_connection.cursor()
    request = displayedRequests[row]
    
    trueRNO = False
    
    #RNO     
    while trueRNO == False:
        rno = input("\n   Enter a ride number\n < Press ENTER to skip > ")
        if rno.isdigit():
            cursor.execute("SELECT rno, driver FROM rides WHERE rno = ?;",[rno])
            rnos = cursor.fetchall()
            if len(rnos) == 0:
                print("***\n*** Invalid rno. Try again\n*** ")
                continue
            elif len(rnos) == 1:
                trueRNO = True
            else:
                print("***\n*** Something went wrong. Try again\n*** ")
                continue
        elif rno == "":
            trueRNO = True
            rno = None
        else:
            print("***\n*** Something went wrong. Try again\n***")
            continue     
    
    #Messgae
    rid = request[0]
    poster = request[1]

    timestamp = datetime.now()
    timestamp = str(timestamp)[:19]
    print("\n>Type a message to send  ...  . . ... :\n")
    message = input() 

    # insert inputted message into the table
    cursor.execute(("INSERT INTO inbox VALUES (?, ?, ?, ?, ?, 'n');"),[request[1], timestamp, member_email, message, rno])

    print(">Message sent! .. .. . ..")#.format(message, poster)

    db_connection.commit()
    sleep(1.4)
    return

################################################################
#    