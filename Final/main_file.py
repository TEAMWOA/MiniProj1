import sqlite3
import sys

from menus import *
from utility import *


def main():
    # Setup connection to database
    if len(sys.argv) != 2:
        print("Please pass the database file as a command line argument (dbname.db)")
        exit()

    path = "./{}".format(sys.argv[1])
    db_connection = sqlite3.connect(path)
    cursor = db_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    db_connection.commit()

    # Start user at login menu
    login_menu(db_connection, cursor)
    db_exit(db_connection)


if __name__ == "__main__":
    main()
