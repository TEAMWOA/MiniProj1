# Ride Request Handling 
#
#
#
import menus
from time import sleep
from utility import *


def post_ride_request(db_connection, cursor, member_email):
    # The member can post a ride request by providing a date, a pick up location code,
    # a drop off location code, and the amount willing to pay per seat.
    # The request id is set to a unique number automatically
    # Can return by pressing enter at any time (except for when entering amount)

    clear_screen()

    print("\n")
    print("    ####################")
    print("    ####            ####")
    print("    ### POST REQUEST ###")
    print("    ####            ####")
    print("    ####################\n\n")

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
    while not validate_date(date):
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
        if len(pickup) == 0:
            return
        pickup = input("  Pickup location: ").lower()

    # Validate dropoff location (can't be the same as pickup)
    dropoff = input("  Dropoff location: ").lower()
    while dropoff not in location_codes or dropoff == pickup:
        if len(dropoff) == 0:
            return
        dropoff = input("  Dropoff location: ").lower()

    # Validate amount (non-negative integer)
    amount = -1
    while amount < 0:
        try:
            amount = int(input("  Amount per seat: "))
        except:
            pass

    # Insert ride request into database
    cursor.execute("INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?);", [rid, member_email, date, pickup, dropoff, amount])
    db_connection.commit()

    print("\nRequest successfully posted.")
    sleep(2)

    menus.main_menu(db_connection, cursor, member_email)
