# Utility functions for the program
# (1) validate_date(date)
# (2) clear_screen()
# (3) db_exit()
#
#
import os
from time import sleep
from datetime import datetime, timedelta
import sys


def validate_date(date):
    now = datetime.datetime.now()
    todaysDATE = now.strftime("%Y-%m-%d")
    if date >= todaysDATE:
        return True
    else:
        return False


def clear_screen():
    # Function to clear the screen - less clutter
    os.system("clear")


def db_exit(db_connection):
    # Commits to database, closes connection and clears screen prior to quitting
    clear_screen()
    print('\n\n   .. .. .... .... .. .\n.. ... .. \nQuitting Program ..... \n\n')
    print("    ###################")
    print("    ####           ####")
    print("    ##  SeeYouAgain  ##")
    print("    ####           ####")    
    print("    ###################\n")
    print('\n    . . . .... .... ..\n                ... . ..... .. .. ') 
    sleep(2)
    
    db_connection.commit()
    db_connection.close()
    clear_screen()
    quit()


def message_member(db_connection, cursor, recipient, sender, message, rno):
    new_message = (recipient, sender, message, rno)
    
    cursor.execute("INSERT INTO inbox VALUES(?, datetime('now'), ?, ?, ?, 'n');", new_message)
    print("\nMESSAGE SENT")
    db_connection.commit()
    
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
