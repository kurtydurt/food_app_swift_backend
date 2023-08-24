CREATE TABLE restaurants (
    restaurant_id INT IDENTITY(1,1) PRIMARY KEY ,
    restaurant_name VARCHAR(255),
    link VARCHAR(255),
    yelp_rating VARCHAR(255),
    yelp_rating_count VARCHAR(255),
    location_address VARCHAR(255)
);