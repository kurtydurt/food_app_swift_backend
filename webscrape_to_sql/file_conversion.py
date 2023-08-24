import json


def dict_to_json(dictionary):
    """
    Converts provided dict to json file
    """
    with open('convert.json', 'w') as convert_file:
        convert_file.write(json.dumps(dictionary))


def json_to_dict():
    """
    Opens scraped data that was converted from a python dict to json form.
    Turns json back into a python dict for testing without having to scrape.
    :return: dict of data
    """
    with open('convert.json') as json_file:
        data = json.load(json_file)
    return data


if __name__ == '__main__':
    data = json_to_dict()
    print(data)
