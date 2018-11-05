import os
from datetime import *


def validate_date(date):
    # Checks whether the date is valid according to the format YYYY-MM-DD
    # Returns True if valid, False otherwise
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
    db_connection.commit()
    db_connection.close()
    clear_screen()
    quit()
def message_member(db_connection, cursor,recipient,sender, message, rno):
    
    seen = 'n'
    new_message = (recipient,sender, message, rno,seen,)
    
    cursor.execute("INSERT INTO inbox VALUES(?,datetime('now'),?,?,?,?) ", new_message)
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
