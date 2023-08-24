import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def process_hours(s):
    """
    Processes takeout and delivery hour strings into dictionary format
    :param s: takeout and delivery hour strings
    :return: a dict of all cap days of week as keys to the hours the restaurant is open as a string value
    """
    l = s.split('\n')
    l.pop(0)
    day_to_hours = {}
    for day_hours in l:
        day, hours = day_hours.split(maxsplit=1)
        day_to_hours[day] = hours
    day_to_hours.pop('Delivery', None)
    day_to_hours.pop('Takeout', None)
    return day_to_hours


def initiate_driver(headless=True):
    """
    Initiates chrome webdriver
    :param headless: determines whether to run in headless mode
    :return: driver instance
    """
    # instantiate options
    options = webdriver.ChromeOptions()
    # run browser in headless mode
    if headless:
        options.add_argument("--headless=new")
    options.add_argument('--disable-blink-features=AutomationControlled')
    # instantiate driver
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=options)
    return driver


def scrape_el_restaurants(driver, url='https://eatstreet.com/eastlansing-mi/restaurants'):
    """
    scrapes Eatstreet website for restaurant data
    :param driver: webdriver instance
    :param url: site to scrape
    :return: dictionary of all restaurant data in east lansing
    """
    # wait to load
    driver.implicitly_wait(1)
    # get the entire website content
    driver.get(url)
    # initialize dicts
    restaurant_dict = {}
    rest_to_link = {}

    # page navigation loop

    for i in range(1, 4):
        # select restaurant list items
        elements = driver.find_elements(By.CSS_SELECTOR,
                                        '.li.li--rest-list.border-bottom-last-1.ng-scope.ng-isolate-scope')

        for element in elements:

            # gather info
            try:
                restaurant = element.find_element(By.CSS_SELECTOR,
                                                  '.restaurant-header.restaurant-header--rest-list.ng-binding')
                name, link = restaurant.text, restaurant.get_attribute('href')
            except:
                continue
            try:
                cuisine = element.find_element(By.CSS_SELECTOR, '.restaurant-cuisine.ng-binding.ng-scope').text
            except:
                cuisine = 'Cuisine information not found'
            try:
                yelp_rating = element.find_element(By.CSS_SELECTOR, '#ESRating').get_attribute('title')
            except:
                yelp_rating = '0'
            try:
                delivery_eta = element.find_element(By.CSS_SELECTOR,
                                                    '.delivery-item-info.text-ellipsis.ng-binding.ng-scope').text
            except selenium.common.exceptions.NoSuchElementException:
                delivery_eta = 'Not Available'
            try:
                delivery_min = element.find_element(By.CSS_SELECTOR,
                                                    '.delivery-item-info.delivery-item-info--min.ng-binding').text
            except selenium.common.exceptions.NoSuchElementException:
                delivery_min = 'None'
            try:
                delivery_only = False
                if element.find_element(By.CSS_SELECTOR,
                                        '.featured-border.featured-border-left').text == 'Delivery Only':
                    delivery_only = True
            except selenium.common.exceptions.NoSuchElementException:
                delivery_only = False
                # build dict
            rest_to_link[name] = link
            restaurant_dict[name] = {'cuisine': cuisine, 'link': link, 'rating': yelp_rating,
                                     'delivery_eta': delivery_eta, 'delivery_min': delivery_min,
                                     'delivery_only?': delivery_only}
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        try:
            driver.find_element(By.CSS_SELECTOR,
                                '.pagination__btn.btn.btn-primary.float-right.visible_focus.ng-isolate-scope.active').click()
        except selenium.common.exceptions.NoSuchElementException:
            continue
    driver.quit()

    for name, link in rest_to_link.items():
        restaurant_dict[name]['menu'] = menu_scrape(initiate_driver(), link, restaurant_dict, name)
    return restaurant_dict


def menu_scrape(driver, restaurant_url, restaurant_dict, restaurant_name):
    """
    Scrapes data from supplied restaurants page to complete restaurant_dict
    :param driver: initialized chrome webdriver
    :param restaurant_url: url of restaurant page to scrape
    :param restaurant_dict: dict created in restaurant_scrape()
    :param restaurant_name: name of restaurant to be used as key in restaurant_dict
    :return: dictionary of menu items to be appended to respective entry in restaurant_dict
    """
    url = restaurant_url
    # get the entire website content
    driver.get(url)

    # initialize dict
    food_items_dict = {}
    try:
        rest_info = driver.find_element(By.CSS_SELECTOR, '.restaurant-info')
        location = rest_info.find_element(By.CSS_SELECTOR, '.address-text-rest-menu').text
        rating_count = rest_info.find_element(By.CSS_SELECTOR, '.es-dropdown.margin-top-10').text
        cuisine = rest_info.find_element(By.CSS_SELECTOR, ".cuisine-text-rest-menu.ng-scope").text
        delivery_fee = driver.find_element(By.CSS_SELECTOR,
                                           ".restaurant__info__list__item__detail.ng-binding.ng-scope").text
    except selenium.common.exceptions.NoSuchElementException:
        return 'Error Up In This Ho'
    restaurant_dict[restaurant_name].update(
        {'location': location, 'rating_count': rating_count, 'cuisine': cuisine, 'delivery_cost': delivery_fee})

    # select elements by class name
    categories = driver.find_elements(By.CSS_SELECTOR, '.list.ng-scope')
    for category in categories:
        cat_name = category.find_element(By.CSS_SELECTOR, '.list_title.ng-binding').text
        cat_description = category.find_element(By.CSS_SELECTOR, '.remove-margin.ng-binding').text
        cat_description = 'No description provided.' if not cat_description else cat_description

        food_items_dict[cat_name] = {'description': cat_description, 'items': {}}
        elements = category.find_elements(By.CLASS_NAME, 'product-container')
        for title in elements:
            price = title.find_element(By.CLASS_NAME, 'food-price').text
            food = title.find_element(By.CLASS_NAME, 'menu-item-name').text
            description = title.find_element(By.CLASS_NAME, 'restaurant-description').text
            description = 'No description provided.' if not description else description
            food_items_dict[cat_name]['items'][food] = [price, description]

    driver.find_element(By.ID, 'info').click()
    delivery_hours = driver.find_element(By.CSS_SELECTOR, '.widget.widget--menu-more-info').text
    try:
        hours_toggle = driver.find_element(By.CSS_SELECTOR, '.btn-group.btn-group--menu-more-info.ng-scope')
        hours_toggle.find_elements(By.TAG_NAME, 'label')[1].click()
        takeout_hours = driver.find_element(By.CSS_SELECTOR, '.widget.widget--menu-more-info').text
    except selenium.common.exceptions.NoSuchElementException:
        takeout_hours = 'NA'
    delivery_hours = process_hours(delivery_hours)
    takeout_hours = process_hours(takeout_hours)
    restaurant_dict[restaurant_name]['delivery_hours'] = delivery_hours if len(delivery_hours) else 'NA'
    restaurant_dict[restaurant_name]['takeout_hours'] = takeout_hours if len(takeout_hours) else 'NA'
    driver.quit()
    return food_items_dict


if __name__ == '__main__':
    print(scrape_el_restaurants(initiate_driver(), 'https://eatstreet.com/eastlansing-mi/restaurants'))

