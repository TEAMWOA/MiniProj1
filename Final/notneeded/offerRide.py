#Offer Ride
#
#

import sqlite3 #sql module
import os
import sys
import getpass # password
import time #time delay
import datetime

from utility import *

def offerRide(cursor, member):
    clearScreen()
    print("\n")
    print("    ##################")
    print("    ####          ####")
    print("    ### Offer Ride ###")
    print("    ####          ####")    
    print("    ##################\n")

    driver = str(member)
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
        now = datetime.datetime.now()
        date = input("{DATE} Enter ride date (ex. YYYY-MM-DD): ")
        if (len(date) != 10) or (date[4]!="-") or (date[7]!='-') or not (date[0:4].isdigit()) or not (date[5:7].isdigit()) or  not (date[8:10].isdigit()):
            print("***\n*** Incorrect date format. Try again (ex. YYYY-MM-DD)\n***")
            continue
        else:
            year = int(date[0:4])
            month = int(date[5:7])
            day = int(date[8:10])
            todaysDATE = now.strftime("%Y-%m-%d")#check if less than today's date... the date today https://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
            
            if date<todaysDATE:
                print("***\n*** Incorrect date. Cannot offer rides in the past.\n*** Today's date is: {}\n***".format(todaysDATE))
                continue
            if (month > 12) or (month < 1) or (day < 1) or (day>31):
                print("***\n*** Incorrect date. Try again (ex. YYYY-MM-DD)\n***")
                continue
            if(month==4)or(month==6)or(month==9)or(month==11): 
                if day>30:
                    print("***\n*** Incorrect date. There are not that many days in the month. Try again (ex. YYYY-MM-DD)\n***")
                    continue
            if(month==2):
                if(year%4 == 0):
                    if day>29:
                        print("***\n*** Incorrect date format. Remember it's February... (ex. YYYY-MM-DD)\n***")
                        continue
                elif day>28:
                    print("***\n*** Incorrect date. Remember it's February... (ex. YYYY-MM-DD)\n***")
                    continue
            trueDate = True
                                                                                                
    while trueNoSeats == False:
        noSeats = input("{SEATS} Enter the number of seats: ")
        if noSeats.isdigit():
            if noSeats != '0':
                trueNoSeats = True
            else:
                print("***\n*** Incorrect input. You can't offer a ride with 0 seats. Try again\n***")
            continue    
        else:
            print("\n*** Incorrect input format. Try again\n***")
            continue
                                                                                                
    while truePricePerSeat == False :
        pricePerSeat = input("{PRICE} Enter a price per seat($) : ")
        if pricePerSeat.isdigit():
            truePricePerSeat = True
        else:
            print("***\n*** Incorrect input format. Try again\n***")
            continue
        
                                                                                                
    while trueLuggage == False:
        luggage = input("{LUGGAGE} Enter a luggage description: ")
        if len(luggage) >10:
            print("***\n***Too long of a description (10 characters max). Try again\n***")
            continue
        if len(luggage)==0:
            print("***\n***You need to enter something for the description. Try again\n***")
            continue
        trueLuggage = True
                                                                                                
    while trueSRC == False:
        SRCnum = input("{PICKUP} Enter a pickup location: ")
        if len(SRCnum) >16 or len(SRCnum)==0:
            print("***\n*** Incorrect input format. Try again\n***")
            continue
        
        cursor.execute("SELECT * FROM locations WHERE lcode LIKE \"%"+SRCnum+"%\"  OR city LIKE \"%"+SRCnum+"%\" OR prov LIKE \"%"+SRCnum+"%\" OR address LIKE \"%"+SRCnum+"%\"")
        srcOptions = cursor.fetchall()
        x = 0
        if(len(srcOptions)>1):
            clearScreen()
            print("\nSelect a pickup location by the listed number option \n<press ENTER for more options>")
            while x < len(srcOptions):
                try:
                    print(str(x+1) +". " +str(srcOptions[x]))
                    x = x+1
                except:
                    continue
                if x//5 > 0:
                    choice = input("")
                    if choice.isdigit():
                        src = srcOptions[int(choice)-1][0]
                        trueSRC = True
                        break
                    elif choice == "":
                        if x+1 > len(srcOptions):
                            x = 0
                        continue
                    else:
                        print("***\n*** Incorrect choice. Try again\n***")
                        x = 0
                        continue    
        elif(len(srcOptions)==1):
            src = srcOptions[0][0]
            print(srcOptions)
            trueSRC = True
        else:
            print("***\n*** Something is MIA. We couldn't find any lcode, city, province or address with that query\n***")
            continue
    
    while trueDST == False:
        DSTnum = input("{DROPOFF} Enter a destination location: ")
        if len(DSTnum) >16 or len(DSTnum)==0:
            print("***\n*** Incorrect input format. Try again\n***")
            continue
        
        cursor.execute("SELECT * FROM locations WHERE lcode LIKE \"%"+DSTnum+"%\"  OR city LIKE \"%"+DSTnum+"%\" OR prov LIKE \"%"+DSTnum+"%\" OR address LIKE \"%"+DSTnum+"%\"")
        dstOptions = cursor.fetchall()
        
        x = 0
        if(len(dstOptions)>1):
            clearScreen()
            print("\nSelect a destination location by the listed number option \n<press ENTER for more options>")
            while x < len(dstOptions):
                try:
                    print(str(x+1) +". " +str(dstOptions[x]))
                    x = x+1
                except:
                    continue
                if x//5 > 0:
                    choice = input("")
                    if choice.isdigit():
                        dst = dstOptions[int(choice)-1][0]
                        trueDST = True
                        break
                    elif choice == "":
                        if x+1 > len(dstOptions):
                            x = 0
                        continue
                    else:
                        print("***\n*** Incorrect choice. Try again\n***")
                        x = 0
                        continue    
                        
        elif(len(dstOptions)==1):
            dst = dstOptions[0][0]
            print(dstOptions)
            trueDST = True
        else:
             print("\n*** Something is MIA. We couldn't find any lcode, city, province or address with that query\n***")



    while trueEnroutes == False:
        stop = input("{ENROUTE} Enter an enroute location \n < press ENTER to skip > ")
        if len(stop) >16:
            print("***\n***Incorrect input format. Try again\n***")
            continue

        if stop == "":
            trueEnroutes = True
            continue
        
        cursor.execute("SELECT * FROM locations  WHERE lcode LIKE \"%"+stop+"%\"  OR city LIKE \"%"+stop+"%\" OR prov LIKE \"%"+stop+"%\" OR address LIKE \"%"+stop+"%\"")
        stopOptions = cursor.fetchall()
        
        x = 0
        
        if(len(stopOptions)>1):
            print("{ENROUTE} Choose an enroute location by the listed number\n < press ENTER for all options >")
            while x < len(stopOptions):
                try:
                    print(str(x+1) +". " +str(stopOptions[x]))
                    x = x+1
                except:
                    continue
                if x//5 > 0:
                    choice = input("")
                    if choice.isdigit():
                        stop = stopOptions[int(choice)-1]
                        enrouteStops.append(stop)
                        break
                    elif choice == "":
                        if x+1 > len(stopOptions):
                            x = 0
                        continue
                    else:
                        print("\n*** Incorrect choice. Try again ***")
                        x = 0
                        continue    
        elif(len(stopOptions)==1):
            enrouteStops.append(stopOptions[0])
            print(stopOptions)
        else:
             print("\n*** Something is MIA. We couldn't find any lcode, city, province or address with that query\n***")
        

    while trueCar == False:
        cno = input("{CARNUMBER} Enter a car number\n < Press ENTER to skip > ")
        if cno.isdigit():
            cursor.execute("SELECT cno FROM cars WHERE cno = \"" +cno+ "\"")
            cars = cursor.fetchall()
            if len(cars) == 0:
                print("***\n*** That car was not found. Try again\n*** ")
                continue
            elif len(cars) == 1:
                trueCar = True
            else:
                print("***\n*** Something went wrong. Try again\n*** ")
                continue
        elif cno == "":
            trueCar= True
            cno = "NULL"
        else:
            print("***\n*** Something went wrong. Try again\n***")
            continue

    cursor.execute("INSERT INTO rides VALUES (\""+rno+"\", \""+pricePerSeat+"\", \""+date+"\", \""+noSeats+"\", \""+luggage+"\", \""+str(src)+"\", \""+str(dst)+"\", \""+driver+"\", \""+cno+"\")")
    for item in enrouteStops:
        cursor.execute("INSERT INTO enroute VALUES (\"" +rno+"\", \""+item[0]+"\")")
    clearScreen()