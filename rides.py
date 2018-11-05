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

################################################################
#
# 1. Search for Rides
#
def ride_search(db_connection, cursor, member_email):
    # Searches for a ride
    # Keyword can match either the location code or substring of the city, province
    # or the address fields of the location
    # display all ride details and car details

    clear_screen()

    print("\n")
    print("    ###################")
    print("    ####           ####")
    print("    ### Ride Search ###")
    print("    ####           ####")
    print("    ###################\n\n")
    print("\n> Enter up to 3 keywords:")
    print("< Type EXIT to end the program or press ENTER/type BACK to go back to the Main Menu. >\n")

    # recieve input from user and split using blankspace
    prompt = input().split()
    print("PROMPT:", prompt)
    if prompt[0].upper() == "EXIT":
        db_exit(db_connection)  # quits program
        return False

    if prompt[0].upper() == "BACK" or prompt == "":
        menus.main_menu(db_connection, cursor, member_email)

    else:
        # for each keyword given, make a sequence ins SQLite
        for each in prompt:
            print("\n> You searched...")
            keyword = "%" + each + "%"
            print(keyword)

            # a list of sequences for each possible match

            keyword = (
            keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword)

            # execute query for each keyword

            cursor.execute(
                "SELECT distinct r.rno, r.price, r.rdate, r.seats, r.lugDesc,r.src, r.dst, r.driver, r.cno, c.cno, c.make, c.model, c.seats, c.owner FROM rides AS r LEFT OUTER JOIN enroute e on r.rno = e.rno LEFT OUTER JOIN locations l1 on r.src = l1.lcode LEFT OUTER JOIN locations l2 on r.dst = l2.lcode LEFT OUTER JOIN cars c on r.cno = c.cno WHERE r.src LIKE ? or r.dst LIKE ? or e.lcode LIKE ? or l1.lcode LIKE ? or l1.city LIKE ? or l1.prov LIKE ? or l1.address LIKE ? or l2.lcode LIKE ? or l2.city LIKE ? or l2.prov LIKE ? or l2.address LIKE ? GROUP BY r.rno;",
                keyword)

            # fetch all the matches for each keyword
            ride_matches = cursor.fetchall()

            # if there is none, provide message and ask again
            if not ride_matches:
                print("\n***\n*** No matches found for < {} >. Try again\n*** ".format(prompt))
                # print("\nNo Matches")
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
                        print("\n***\n*** No more results were found\n*** ")
                        break
                    elif j == (num_columns - 1):
                        break
                    else:

                        # print the first 5 results
                        while j < limit and prompt[0].upper() != "EXIT":
                            try:
                                print(*ride_matches[j])
                                j += 1
                                i += 1
                            except IndexError:
                                print("\n***\n*** No more results were found\n*** ")
                                return False

                        # if there are more results, ask the user
                        # if they want to see more or exit the list
                        print("< Press ENTER to see more results or type EXIT to end the program. >\n")
                        prompt = input()

                        # if they press enter to see more
                        # increase the limit and list the next 5
                        # matches until all matches are listed

                        if len(prompt) == 0:
                            limit += 5
                            print("\n")

                        # if they exit the list, return to search prompt
                        elif prompt[0].upper() == "EXIT":
                            db_exit(db_connection)

    return True

################################################################
#
# 2. Offer Ride 
#
def offer_ride(db_connection, cursor, member_email):
    clear_screen()
    print("\n")
    print("    ##################")
    print("    ####          ####")
    print("    ### Offer Ride ###")
    print("    ####          ####")
    print("    ##################\n")

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

    while truePricePerSeat == False:
        pricePerSeat = input("   {PRICE} Enter a price per seat ($): ")
        if pricePerSeat.isdigit():
            truePricePerSeat = True
        else:
            print("***\n*** Incorrect input format. Try again\n***")
            continue

    while trueLuggage == False:
        luggage = input("   {LUGGAGE} Enter a luggage description: ")
        if len(luggage) > 10:
            print("***\n***Too long of a description (10 characters max). Try again\n***")
            continue
        if len(luggage) == 0:
            print("***\n***You need to enter something for the description. Try again\n***")
            continue
        trueLuggage = True

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

        cursor.execute(
            "INSERT INTO rides VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", [rno, pricePerSeat, date, noSeats, luggage, src, dst, driver, cno])
        for item in enrouteStops:
            cursor.execute("INSERT INTO enroute VALUES (?, ?);", [rno, item[0]])
    db_connection.commit()

    print("\n   . . .. . Ride successfully posted!")
    sleep(1.5)

    menus.main_menu(db_connection, cursor, member_email)
