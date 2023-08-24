import pyodbc
from file_conversion import json_to_dict

terms_to_category = {

    "Chinese": 'Asian',

    "Indian": 'Asian',

    "Japanese": 'Asian',

    "Korean": 'Asian',

    "Thai": 'Asian',

    "Sushi": 'Asian',

    "Cantonese": 'Asian',

    "Vietnamese": 'Asian',

    "Subs": 'Sandwiches',

    "Sandwiches": 'Sandwiches',

    "Deli": 'Sandwiches',

    "Seafood": 'Seafood',

    "Pizza": 'Pizza',

    "Italian": 'Italian',

    "Pasta": 'Italian',

    "Wings": 'Wings',

    "Chicken": 'Wings',

    "Fast": 'Fast_Food',

    "Mexican": 'Mexican',

    "Dessert": 'Dessert',

    'Desserts': 'Dessert',

    "Ice": 'Dessert',

    "Frozen": 'Dessert',

    "American": 'American',

    "Diner": 'American',

    "Southern": 'American',

    "BBQ": 'American',

    "Breakfast": 'Breakfast',

    "Mediterranean": 'Mediterranean',

    "Middle": 'Mediterranean',

    "Eastern": 'Mediterranean',

    "Lebanese": 'Mediterranean',

    "Greek": 'Mediterranean',

    "Burgers": 'Burgers',

    "Hotdogs": 'Burgers'

}


def azure_connect():
    server = 'tcp:grub.database.windows.net'
    database = 'grub'
    username = 'grubbington'
    password = 'mommalovegrub123!'
    driver = '{ODBC Driver 17 for SQL Server}'

    cnxn = pyodbc.connect('DRIVER=' + driver +
                          ';SERVER=' + server +
                          ';DATABASE=' + database +
                          ';UID=' + username +
                          ';PWD=' + password)

    print('Connection established')
    return cnxn


def create_table(connection):
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE restaurants (restaurant_id int primary key AUTOINCREMENT ,
                                                restaurant_name varchar(255),
                                                price int)''')

    connection.commit()


def category_assign(cuisine_string):
    cuisine_string = cuisine_string.replace("•", ",")
    cuisine_list = cuisine_string.split(',')
    categories = []
    for cuisine in cuisine_list:
        for key in terms_to_category.keys():
            if cuisine in key or key in cuisine:
                categories.append(terms_to_category[key])
    return categories


def extract_insert_restaurant(connection=azure_connect(), rest_dict=json_to_dict()):
    cursor = connection.cursor()
    count = 1
    for k, v in rest_dict.items():
        # p_ to prevent overlap in var names, 'parameter'
        p_restaurant_name = k
        p_restaurant_link = v.get('link', 'NA')
        p_yelp_rating = v.get('rating', '0')
        p_rating_count = v.get('rating_count', '0')
        p_location_address = v.get('location', 'No address provided')
        cursor.execute(f'''INSERT INTO restaurants(restaurant_name, link, yelp_rating, yelp_rating_count, location_address)
VALUES (?,?,?,?,?)''', p_restaurant_name, p_restaurant_link, p_yelp_rating, p_rating_count, p_location_address)
        print(f'Row Inserted ({count})')
        count += 1

    connection.commit()


def extract_insert_items(connection=azure_connect(), rest_dict=json_to_dict()):
    cursor = connection.cursor()
    count = 1
    for k, v in rest_dict.items():
        # p_ to prevent overlap in var names, 'parameter'
        p_restaurant_name = k
        p_restaurant_link = v.get('link', 'NA')
        p_yelp_rating = v.get('rating', '0')
        p_rating_count = v.get('rating_count', '0 ratings')
        p_location_address = v.get('location', 'No address provided')
        p_cuisine = v.get('cuisine')
        p_categories = ", ".join(category_assign(p_cuisine))
        cursor.execute(f'''INSERT INTO restaurants(restaurant_name, link, yelp_rating, yelp_rating_count, location_address, cuisines, categories)
VALUES (?,?,?,?,?,?,?)''', p_restaurant_name, p_restaurant_link, p_yelp_rating, p_rating_count, p_location_address,
                       p_cuisine, p_categories)
        try:
            for category, info_dict in v['menu'].items():
                for p_item_name, info_list in info_dict['items'].items():
                    p_price = info_list[0]
                    p_description = info_list[1]
                    cursor.execute(
                        f'''INSERT INTO menu_items(item_name, item_description, item_price, menu_category, restaurant_id) VALUES (?,?,?,?,IDENT_CURRENT('restaurants'))''',
                        p_item_name, p_description, p_price, category)
                    print("Item inserted")
        except AttributeError:
            continue
        print(f'Row Inserted ({count})')
        count += 1

    connection.commit()


if __name__ == '__main__':
    extract_insert_items()
