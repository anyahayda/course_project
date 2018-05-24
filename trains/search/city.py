import json
import requests

HEADERS = {'User-Agent':  'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}


class City:
    REQUEST_TO_GET_STATION = 'https://booking.uz.gov.ua/train_search/station/'

    def __init__(self, name=None, code=None):
        self.name = name
        self.code = code

    @staticmethod
    def loads(response):
        result = []
        for city in response:
            result.append(
                City(city.get('title'), city.get('value'))
            )
        return result


    @staticmethod
    def get_name_by_code():
        pass

    @staticmethod
    def get_citiest_by_name(name):
        params = {'term': name}
        response = requests.get(City.REQUEST_TO_GET_STATION, params=params, headers=HEADERS)
        return City.loads(json.loads(response.text))