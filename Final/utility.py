# Utility functions for the program
# (1) validate_date(date)
# (2) clear_screen()
# (3) db_exit()
#
#
import os
import time 
import datetime
import sys


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
    print('\n\n\n   .. .. .... .... .. .\n.. ... .. \nQuitting Program ..... \n\n')
    print("    ###################")
    print("    ####           ####")
    print("    ##  SeeYouAgain  ##")
    print("    ####           ####")    
    print("    ###################\n")
    print('\n    . . . .... .... ..\n                ... . ..... .. .. ') 
    
    
    db_connection.commit()
    db_connection.close()
#     quit()
    time.sleep(1.5) 
    sys.exit()
