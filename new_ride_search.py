def ride_search():
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
        match_list = []
        master_list = []
        for each in prompt:
            print("KEYWORD:")
            keyword = "%" + each + "%"

            # a list of sequences for each possible match

            keyword = (keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword,)

            # execute query for each keyword

            cursor.execute(
                "SELECT distinct r.rno, r.price, r.rdate, r.seats, r.lugDesc,r.src, r.dst, r.driver, r.cno, c.make, c.model, c.year, c.seats FROM rides AS r LEFT OUTER JOIN enroute e on r.rno = e.rno LEFT OUTER JOIN locations l1 on r.src = l1.lcode LEFT OUTER JOIN locations l2 on r.dst = l2.lcode LEFT OUTER JOIN cars c on r.cno = c.cno WHERE r.src LIKE ? COLLATE NOCASE or r.dst LIKE ? COLLATE NOCASE or e.lcode LIKE ? COLLATE NOCASE or l1.lcode LIKE ? COLLATE NOCASE or l1.city LIKE ? COLLATE NOCASE or l1.prov LIKE ? COLLATE NOCASE or l1.address LIKE ? COLLATE NOCASE or l2.lcode LIKE ? COLLATE NOCASE or l2.city LIKE ? COLLATE NOCASE or l2.prov LIKE ? COLLATE NOCASE or l2.address LIKE ? COLLATE NOCASE GROUP BY r.rno;",
                keyword)

            # fetch all the matches for each keyword
            ride_matches = cursor.fetchall()
            
            if len(master_list) == 0:
                for each in ride_matches:
                    master_list.append(each)
            else:
                master_list[:] = [each for each in ride_matches if each in master_list]
                
        master_list = list(master_list)
        for each, ride in enumerate(master_list):
            ride = list(ride)
            master_list[each] = ride
            for each, value in enumerate(ride):
                if value is None:
                    ride[each] = ""
       
        stop_list = False
        print("\n{:^5}{:^5}{:^12}{:^5}{:^15}{:^6}{:^6}{:^20}{:^3}{:^10}{:^10}{:^4}{:^10}".format("rno", "price","date","seats","LugDesc","src","dst","driver","cno","make","model","year","seats"))
        while stop_list == False:
            for count, each in enumerate(master_list):
                print("\n{:^5}{:^5}{:^10}{:^5}{:^15}{:^6}{:^6}{:^20}{:^3}{:^10}{:^10}{:^4}{:^10}".format(each[0],each[1],each[2],each[3],each[4],each[5],each[6],each[7],each[8],each[9],each[10],each[11],each[12],))
                if (count == len(master_list)-1) or count > 0 and (count % 4) == 0:
                    prompt = input("\nEnter a ride number or return to see more: ").strip()
                    if prompt == "":
                        print("\n{:^5}{:^5}{:^12}{:^5}{:^15}{:^6}{:^6}{:^20}{:^3}{:^10}{:^10}{:^4}{:^10}".format("rno", "price","date","seats","LugDesc","src","dst","driver","cno","make","model","year","seats"))
                        continue
                    elif prompt.isdigit():
                        stop_list == True
                        message()
                    elif prompt == 'exit':
                        stop_list == True
                        exit()           
    return True


