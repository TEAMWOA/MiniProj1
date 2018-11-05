# Rides
#
# 1. ride_search(db_connection, cursor, member_email)
# 2. offer_ride(db_connection, cursor, member_email)
#

import sqlite3  # sql module
import os
import sys
import getpass  # password
from time import sleep  # time delay
import datetime

from utility import *
import menus


def ride_search(db_connection, cursor, member_email):
    # Searches for a ride
    # Keyword can match either the location code or substring of the city, province
    # or the address fields of the location
    # display all ride details and car details

    print_logo("Search Rides")

    # recieve input from user and split using blankspace
    prompt = input("\nEnter keywords or 'exit': ")
    if prompt.lower() == "exit":
        menus.main_menu(db_connection, cursor, member_email)
    else:
        # for each keyword given, make a sequence ins SQLite
        match_list = []
        master_list = []
        for keyword in prompt.split(" "):
            print("KEYWORD:" + keyword)
            keyword = "%" + keyword + "%"

            # a list of sequences for each possible match

            keywords = [keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword]

            # execute query for each keyword
            cursor.execute(
                "SELECT distinct r.rno, r.price, r.rdate, r.seats, r.lugDesc,r.src, r.dst, r.driver, r.cno, c.make, c.model, c.year, c.seats FROM rides AS r LEFT OUTER JOIN enroute e on r.rno = e.rno LEFT OUTER JOIN locations l1 on r.src = l1.lcode LEFT OUTER JOIN locations l2 on r.dst = l2.lcode LEFT OUTER JOIN cars c on r.cno = c.cno WHERE r.src LIKE ? COLLATE NOCASE or r.dst LIKE ? COLLATE NOCASE or e.lcode LIKE ? COLLATE NOCASE or l1.lcode LIKE ? COLLATE NOCASE or l1.city LIKE ? COLLATE NOCASE or l1.prov LIKE ? COLLATE NOCASE or l1.address LIKE ? COLLATE NOCASE or l2.lcode LIKE ? COLLATE NOCASE or l2.city LIKE ? COLLATE NOCASE or l2.prov LIKE ? COLLATE NOCASE or l2.address LIKE ? COLLATE NOCASE GROUP BY r.rno;",
                keywords)

            # fetch all the matches for each keyword
            ride_matches = cursor.fetchall()

            if len(master_list) == 0:
                for each in ride_matches:
                    master_list.append(each)
            else:
                master_list[:] = [each for each in ride_matches if each in master_list]
        
        # the masterlist contains only matches all keywords
        # gets fetched as immutable tuples so must be converted into a list
        # for manipulation
        
        master_list = list(master_list)
        
        # Iterate through the list looking for none types and turn them
        # into empty strings 
        for each, ride in enumerate(master_list):
            
            # gets fetched as immutable tuples so must be converted into a list
            # for manipulation            
            ride = list(ride)
            master_list[each] = ride
            
            # if value is none type then replace with an empty string
            for each, value in enumerate(ride):
                if value is None:
                    ride[each] = ""
        
        # boolean to help listing
        stop_list = False

        print_logo("Search Rides")
        
        # print the labels
        print("\n {:<5}{:<7}{:<12}{:<7}{:<15}{:<6}{:<6}{:<20}{:<5}{:<12}{:<10}{:<6}{:<10}".format("rno", "price", "date", "seats", "LugDesc", "src", "dst", "driver", "cno", "make", "model", "year", "seats"))
        
        
        # stop_list is only true if the the input is a ride number or exit
        while stop_list == False:
            
            #print matches maximum 5 at a time
            for count, each in enumerate(master_list):
                print(
                    "\n {:<5}{:<7}{:<12}{:<7}{:<15}{:<6}{:<6}{:<20}{:<5}{:<12}{:<10}{:<6}{:<10}".format(each[0], each[1], each[2], each[3], each[4], each[5], each[6], each[7], each[8], each[9], each[10], each[11], each[12]))
                
                # if we are at the last ride or the the 5th value, ask for an input
                
                if (count == len(master_list) - 1) or (count > 0 and ((count+1) % 5) == 0):
                    prompt = input("\n Enter a ride number or return to see more: ").strip()
                    
                      #if the prompt is empty then keep listing
                    if prompt == "":

                        print_logo("Search Rides")

                        print("\n {:<5}{:<7}{:<12}{:<7}{:<15}{:<6}{:<6}{:<20}{:<5}{:<12}{:<10}{:<6}{:<10}".format("rno", "price", "date", "seats", "LugDesc", "src", "dst", "driver", "cno", "make", "model", "year", "seats"))

                        continue
                    #if the input is a digit then get the email of the driver who is offering the ride from the table
                    # the user will send a message to the driver
                    elif prompt.isdigit():
                        prompt = int(prompt)
                        cursor.execute("SELECT driver FROM rides WHERE rno = ?;", (prompt,))
                        driver = cursor.fetchone()[0]
                        stop_list == True
                        message = input(" Enter message: ")
                        message_member(db_connection, cursor, driver, member_email, message, int(prompt))
                    elif prompt == 'exit':
                        stop_list == True
                        menus.main_menu(db_connection, cursor, member_email)
    return True


################################################################
#
# 2. Offer Ride 
#
def offer_ride(db_connection, cursor, member_email):
    print_logo("Offer Ride")

    driver = str(member_email)
    cursor.execute("SELECT MAX(rno) FROM rides")
    rno = str(int(cursor.fetchone()[0]) + 1)

    trueDate = False
    trueNoSeats = False
    truePricePerSeat = False
    trueLuggage = False
    trueSRC = False
    trueDST = False
    trueCar = False
    trueEnroutes = False

    enrouteStops = []

    # validates date entered by the user; does not let past dates be selected 
    while trueDate == False:
        now = datetime.now()
        date = input("   {DATE} Enter ride date (ex. YYYY-MM-DD): ")
        if (len(date) != 10) or (date[4] != "-") or (date[7] != '-') or not (date[0:4].isdigit()) or not (
        date[5:7].isdigit()) or not (date[8:10].isdigit()):
            print("***\n*** Incorrect date format. Try again (ex. YYYY-MM-DD)\n***")
            continue
        else:
            year = int(date[0:4])
            month = int(date[5:7])
            day = int(date[8:10])
            todaysDATE = now.strftime(
                "%Y-%m-%d")  # check if less than today's date... the date today https://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/

            if date < todaysDATE:
                print("***\n*** Incorrect date. Cannot offer rides in the past.\n*** Today's date is: {}\n***".format(
                    todaysDATE))
                continue
            if (month > 12) or (month < 1) or (day < 1) or (day > 31):
                print("***\n*** Incorrect date. Try again (ex. YYYY-MM-DD)\n***")
                continue
            if (month == 4) or (month == 6) or (month == 9) or (month == 11):
                if day > 30:
                    print(
                        "***\n*** Incorrect date. There are not that many days in the month. Try again (ex. YYYY-MM-DD)\n***")
                    continue
            if (month == 2):
                if (year % 4 == 0):
                    if day > 29:
                        print("***\n*** Incorrect date format. Remember it's February... (ex. YYYY-MM-DD)\n***")
                        continue
                elif day > 28:
                    print("***\n*** Incorrect date. Remember it's February... (ex. YYYY-MM-DD)\n***")
                    continue
            trueDate = True

    # checks if number of seats are related to the cno; does not let a member offer 0 seats
    while trueNoSeats == False:
        noSeats = input("   {SEATS} Enter the number of seats: ")
        if noSeats.isdigit():
            if noSeats != '0':
                trueNoSeats = True
            else:
                print("***\n*** Incorrect input. You can't offer a ride with 0 seats. Try again\n***")
            continue
        else:
            print("\n*** Incorrect input format. Try again\n***")
            continue
    #enter price per seat
    while truePricePerSeat == False:
        pricePerSeat = input("   {PRICE} Enter a price per seat ($): ")
        if pricePerSeat.isdigit():
            truePricePerSeat = True
        else:
            print("***\n*** Incorrect input format. Try again\n***")
            continue
            
    # enter luggage description 
    while trueLuggage == False:
        luggage = input("   {LUGGAGE} Enter a luggage description: ")
        if len(luggage) > 10:
            print("***\n***Too long of a description (10 characters max). Try again\n***")
            continue
        if len(luggage) == 0:
            print("***\n***You need to enter something for the description. Try again\n***")
            continue
        trueLuggage = True
    
    #pick up location: add and select
    while trueSRC == False:
        SRCnum = input("\n   {PICKUP} Enter a pickup location: ")
        if len(SRCnum) > 16 or len(SRCnum) == 0:
            print("***\n*** Incorrect input format. Try again\n***")
            continue

        cursor.execute(
            "SELECT * FROM locations WHERE lcode LIKE \"%" + SRCnum + "%\"  OR city LIKE \"%" + SRCnum + "%\" OR prov LIKE \"%" + SRCnum + "%\" OR address LIKE \"%" + SRCnum + "%\"")
        srcOptions = cursor.fetchall()
        x = 0

        if (len(srcOptions) > 1):
            clear_screen()
            print("\n   Select a pickup location by the listed number option \n   <press ENTER for more options>")
            while x < len(srcOptions):
                try:
                    print(str(x + 1) + ". " + str(srcOptions[x]))
                    x = x + 1
                except:
                    continue
                if x // 5 > 0:
                    choice = input("")
                    if choice.isdigit():
                        src = srcOptions[int(choice) - 1][0]
                        trueSRC = True
                        break
                    elif choice == "":
                        if x + 1 > len(srcOptions):
                            x = 0
                        continue
                    else:
                        print("***\n*** Incorrect choice. Try again\n***")
                        x = 0
                        continue
        elif (len(srcOptions) == 1):
            src = srcOptions[0][0]
            print(srcOptions)
            trueSRC = True
        else:
            print(
                "***\n*** Something is MIA. We couldn't find any lcode, city, province or address with that query\n***")
            continue
            
    # destination location: add and select
    while trueDST == False:
        DSTnum = input("\n   {DROPOFF} Enter a destination location: ")
        if len(DSTnum) > 16 or len(DSTnum) == 0:
            print("***\n*** Incorrect input format. Try again\n***")
            continue

        cursor.execute(
            "SELECT * FROM locations WHERE lcode LIKE \"%" + DSTnum + "%\"  OR city LIKE \"%" + DSTnum + "%\" OR prov LIKE \"%" + DSTnum + "%\" OR address LIKE \"%" + DSTnum + "%\"")
        dstOptions = cursor.fetchall()

        x = 0
        if (len(dstOptions) > 1):
            clear_screen()
            print("\n   Select a destination location by the listed number option \n   <press ENTER for more options>")
            while x < len(dstOptions):
                try:
                    print(str(x + 1) + ". " + str(dstOptions[x]))
                    x = x + 1
                except:
                    continue
                if x // 5 > 0:
                    choice = input("")
                    if choice.isdigit():
                        dst = dstOptions[int(choice) - 1][0]
                        trueDST = True
                        break
                    elif choice == "":
                        if x + 1 > len(dstOptions):
                            x = 0
                        continue
                    else:
                        print("***\n*** Incorrect choice. Try again\n***")
                        x = 0
                        continue

        elif (len(dstOptions) == 1):
            dst = dstOptions[0][0]
            print(dstOptions)
            trueDST = True
        else:
            print("\n*** Something is MIA. We couldn't find any lcode, city, province or address with that query\n***")
    
    
    # add enroutes
    while trueEnroutes == False:
        stop = input("\n   {ENROUTE} Enter an enroute location \n < press ENTER to skip > ")
        if len(stop) > 16:
            print("***\n***Incorrect input format. Try again\n***")
            continue

        if stop == "":
            trueEnroutes = True
            continue

        cursor.execute(
            "SELECT * FROM locations  WHERE lcode LIKE \"%" + stop + "%\"  OR city LIKE \"%" + stop + "%\" OR prov LIKE \"%" + stop + "%\" OR address LIKE \"%" + stop + "%\"")
        stopOptions = cursor.fetchall()

        x = 0

        if (len(stopOptions) > 1):
            print("\n   {ENROUTE} Choose an enroute location by the listed number\n < press ENTER for all options >")
            while x < len(stopOptions):
                try:
                    print(str(x + 1) + ". " + str(stopOptions[x]))
                    x = x + 1
                except:
                    continue
                if x // 5 > 0:
                    choice = input("")
                    if choice.isdigit():
                        stop = stopOptions[int(choice) - 1]
                        enrouteStops.append(stop)
                        break
                    elif choice == "":
                        if x + 1 > len(stopOptions):
                            x = 0
                        continue
                    else:
                        print("\n*** Incorrect choice. Try again ***")
                        x = 0
                        continue
        elif (len(stopOptions) == 1):
            enrouteStops.append(stopOptions[0])
            print(stopOptions)
        else:
            print("\n*** Something is MIA. We couldn't find any lcode, city, province or address with that query\n***")
   
    # valid car number
    while trueCar == False:
        cno = input("\n   {CARNUMBER} Enter a car number\n < Press ENTER to skip > ")
        if cno.isdigit():
            cursor.execute("SELECT cno FROM cars WHERE cno = ? AND owner = ?;", [cno, member_email])
            cars = cursor.fetchall()
            if len(cars) == 0:
                print("***\n*** Invalid car. Try again\n*** ")
                continue
            elif len(cars) == 1:
                trueCar = True
            else:
                print("***\n*** Something went wrong. Try again\n*** ")
                continue
        elif cno == "":
            trueCar = True
            cno = None
        else:
            print("***\n*** Something went wrong. Try again\n***")
            continue

        #enter ride into database with all inputted info
        cursor.execute(
            "INSERT INTO rides VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", [rno, pricePerSeat, date, noSeats, luggage, src, dst, driver, cno])
        for item in enrouteStops:
            cursor.execute("INSERT INTO enroute VALUES (?, ?);", [rno, item[0]])
    db_connection.commit()

    print("\n   . . .. . Ride successfully posted!") #validation 
    sleep(1.5)

    menus.main_menu(db_connection, cursor, member_email)
