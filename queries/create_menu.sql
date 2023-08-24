CREATE TABLE menu_items (
    item_id INT IDENTITY(1,1) PRIMARY KEY,
    item_name VARCHAR(255),
    item_price VARCHAR(255),
    item_description TEXT,
    menu_category VARCHAR(255),
    restaurant_id INT FOREIGN KEY REFERENCES restaurants(restaurant_id)
);