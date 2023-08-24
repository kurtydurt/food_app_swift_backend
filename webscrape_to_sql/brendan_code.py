import json
import sqlite3

con = sqlite3.connect('FoodAppData.db')
cur = con.cursor()

def insert_data(r_dict) -> None:
    for k, v in r_dict.items():
        name = k
        if v['menu'] == 'Error Up In This Ho':
            continue
        cuisine = v['cuisine']
        link = v['link']
        rating = v['rating']
        delivery_eta = v['delivery_eta']
        delivery_min = v['delivery_min']
        delivery_only = v['delivery_only?']
        location = v['location']
        rating_count = v['rating_count']
        delivery_cost = v['delivery_cost']
        deliv_hrs = v['delivery_hours']
        if deliv_hrs == "NA":
            dsun = deliv_hrs
            dmon = deliv_hrs
            dtu = deliv_hrs
            dw = deliv_hrs
            dth = deliv_hrs
            dfr = deliv_hrs
            dsat = deliv_hrs
        else:
            if "SUNDAY" in deliv_hrs.keys():
                dsun = deliv_hrs['SUNDAY']
            if "MONDAY" in deliv_hrs.keys():
                dmon = deliv_hrs['MONDAY']
            if "TUESDAY" in deliv_hrs.keys():
                dtu = deliv_hrs['TUESDAY']
            if "WEDNESDAY" in deliv_hrs.keys():
                dw = deliv_hrs['WEDNESDAY']
            if "THURSDAY" in deliv_hrs.keys():
                dth = deliv_hrs['THURSDAY']
            if "FRIDAY" in deliv_hrs.keys():
                dfr = deliv_hrs['FRIDAY']
            if "SATURDAY" in deliv_hrs.keys():
                dsat = deliv_hrs['SATURDAY']
        take_hrs = v['takeout_hours']
        if take_hrs == "NA":
            tsun = take_hrs
            tmon = take_hrs
            ttu = take_hrs
            tw = take_hrs
            tth = take_hrs
            tfr = take_hrs
            tsat = take_hrs
        else:
            #############COME BACK HERE
            if "SUNDAY" in take_hrs.keys():
                tsun = take_hrs['SUNDAY']
            if "MONDAY" in take_hrs.keys():
                tmon = take_hrs['MONDAY']
            if "TUESDAY" in take_hrs.keys():
                ttu = take_hrs['TUESDAY']
            if "WEDNESDAY" in take_hrs.keys():
                tw = take_hrs['WEDNESDAY']
            if "THURSDAY" in take_hrs.keys():
                tth = take_hrs['THURSDAY']
            if "FRIDAY" in take_hrs.keys():
                tfr = take_hrs['FRIDAY']
            if "SATURDAY" in take_hrs.keys():
                tsat = take_hrs['SATURDAY']
        cur.execute('''INSERT INTO Restaurants
            (Restaurant, Cuisine, Link, Rating, Delivery_ETA,
            Delivery_Minimum, Delivery_Only, Location, Rating_Count, Delivery_Cost)
            Values (?,?,?,?,?,?,?,?,?,?)''',
            (name, cuisine, link, rating, delivery_eta,
            delivery_min, delivery_only, location, rating_count, delivery_cost))
        rest_id = cur.lastrowid
        con.commit()
        cur.execute('''INSERT INTO Delivery_Hours
            (Restaurant_ID, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (rest_id, dsun, dmon, dtu, dw, dth, dfr, dsat))
        con.commit()
        cur.execute('''INSERT INTO Take_Out_Hours
                                (Restaurant_ID, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                        (rest_id, tsun, tmon, ttu, tw, tth, tfr, tsat))
        con.commit()
        for ik, iv in v['menu'].items():
            item_category = ik
            ic_description = iv['description']
            for iik, iiv in iv['items'].items():
                item = iik
                price, item_description = iiv
                cur.execute('''INSERT INTO Menu_Categories
                        (Restaurant_ID, Category, Description)
                        VALUES (?, ?, ?)''',
                        (rest_id, item_category, ic_description))
                ic_id = cur.lastrowid
                con.commit()
                cur.execute('''INSERT INTO Menu_Items
                        (Restaurant_ID, Category_ID, Item_Name, Description, Price)
                                VALUES (?, ?, ?, ?, ?)''',
                        (rest_id, ic_id, item, item_description, price))
                con.commit()

with open('JSON Data.json') as json_file:
    data = json.load(json_file)
    insert_data(data)
