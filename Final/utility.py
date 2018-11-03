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
