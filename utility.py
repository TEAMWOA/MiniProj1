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

def will_validate_date(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d')
        if date >= (datetime.now() - timedelta(days=1)):
            return True
    except:
        return False

def clear_screen():
    # Function to clear the screen - less clutter
    os.system("clear")


def db_exit(db_connection):
    # Commits to database, closes connection and clears screen prior to quitting
    print_logo("See you again!")
    print('\n    . . . .... .... ..\n                ... . ..... .. .. ') 
    sleep(2)
    
    db_connection.commit()
    db_connection.close()
    clear_screen()
    quit()


# Prints a logo containing the specifiec string at the top of the console
def print_logo(string_to_print):
    width = len(string_to_print) + 14
    str1 = "  " + ("#" * width)
    str2 = "  " + ("#" * 4) + (" " * (width - 8)) + ("#" * 4)
    str3 = "  " + ("#" * 4) + (" " * 3) + string_to_print + (" " * 3) + ("#" * 4)
    clear_screen()
    print("\n")
    print(str1)
    print(str2)
    print(str3)
    print(str2)
    print(str1)
    print("\n")
    return


# Sends a message to a member
def message_member(db_connection, cursor, recipient, sender, message, rno):
    new_message = (recipient, sender, message, rno)
    
    cursor.execute("INSERT INTO inbox VALUES(?, datetime('now'), ?, ?, ?, 'n');", new_message)
    print("\nMESSAGE SENT")
    db_connection.commit()
    
    return True


# Checks whether the given member is valid
def valid_user(member_to_book,cursor):
    valid_user = False
    user = (member_to_book,)
    cursor.execute("SELECT name from members where email = ? ",user)
    if cursor.fetchone():
        valid_user = True
        
    return valid_user


# Validates the given lcode
def valid_lcode(lcode,cursor):
    valid = False
    location = (lcode,)
    cursor.execute("SELECT address from locations where lcode = ? ", location)
    if cursor.fetchone():
        valid = True
    return valid
