def ride_search(cursor):
    # Searches for a ride
    # Keyword can match either the location code or substring of the city, province
    # or the address fields of the location
    # display all ride details and car details

    # recieve input from user and split using blankspace
    prompt = input("\nEnter keywords or 'exit': ").split()

    if prompt == "exit":
        return False
    else:
        # for each keyword given, make a sequence ins SQLite

        for each in prompt:
            keyword = "%" + each + "%"
            print(keyword)

            # a list of sequences for each possible match

            keyword = (keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword)

            # execute query for each keyword

            cursor.execute(
                "SELECT distinct r.rno, r.price, r.rdate, r.seats, r.lugDesc,r.src, r.dst, r.driver, r.cno, c.cno, c.make, c.model, c.seats, c.owner FROM rides AS r LEFT OUTER JOIN enroute e on r.rno = e.rno LEFT OUTER JOIN locations l1 on r.src = l1.lcode LEFT OUTER JOIN locations l2 on r.dst = l2.lcode LEFT OUTER JOIN cars c on r.cno = c.cno WHERE r.src LIKE ? or r.dst LIKE ? or e.lcode LIKE ? or l1.lcode LIKE ? or l1.city LIKE ? or l1.prov LIKE ? or l1.address LIKE ? or l2.lcode LIKE ? or l2.city LIKE ? or l2.prov LIKE ? or l2.address LIKE ? GROUP BY r.rno;",
                keyword)

            # fetch all the matches for each keyword
            ride_matches = cursor.fetchall()

            # if there is none, provide message and ask again

            if not ride_matches:
                print("\nNo Matches")
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
                        print("\nNo More Results")
                        break
                    elif j == (num_columns - 1):
                        break
                    else:

                        # print the first 5 results

                        while j < limit and prompt != "Exit":
                            try:
                                print(*ride_matches[j])
                                j += 1
                                i += 1
                            except IndexError:
                                print("\nNo More Results")
                                return False

                        # if there are more results, ask the user
                        # if they want to see more or exit the list

                        prompt = input("\nPress Enter For More or 'exit': ")

                        # if they press enter to see more
                        # increase the limit and list the next 5
                        # matches until all matches are listed

                        if len(prompt) == 0:
                            limit += 5
                            print("\n")

                        # if they exit the list, return to search prompt
                        elif prompt == "exit":
                            ride_search(cursor)

    return True