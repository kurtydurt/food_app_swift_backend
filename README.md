# food_app_swift_backend
 
I started this project during my time at the MSU x Apple Developer Foundation summer program. I handled the backend while my other group members worked on the front end. We were new to swift and lots of other concepts so the front end and back end did not end up being compatible, but I want to make a front end for this data some day. The front end code they created will likely be published on a repo on user trickwithatwist's profile soon. 

This backend starts in python with the selenium library. I used it to scrape restaurant and menu item data from East Lansing restaurants using the eatstreet.com website. From there I take the python dictionary generated by the scraper and upload to an Azure MSSQL database. Ideally I wanted to have this run as the backend for an API call in swift, but with time constraints and poor Azure documentation it was not a reality. In any case, I also made a series of functions to turn the Python dict into JSON and vice versa so the webscraper does not need to run for 20 minutes every time you want to run a test. 
From there I use the nice table structure with foreign key association and so on in SQL to turn the uploaded back into JSON to be used with some Codable structs I defined in Swift. 
