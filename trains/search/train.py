import json
import requests
import datetime

from search.city import City


HEADERS = {'User-Agent':  'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}


class Places:
    def __init__(self, category=None, price=None, free=None):
        self.category = category
        self.price = price
        self.free = free

    def load(self, data):
        self.category = data.get('title')
        self.price = str(data.get('cost'))
        self.price = float('{}.{}'.format(self.price[:-2], self.price[-2:]))
        self.free = data.get('free')
        return self


class Train:
    REQUEST_TO_SEARCH_TRAIN = "https://booking.uz.gov.ua/train_search/"
    REQUEST_TO_SEARCH_WAGON = "https://booking.uz.gov.ua/train_wagons/"

    def __init__(self, _from=None, _to=None, departure_date=None, arrival_date=None,
                 price=None, places=[], train=None, available_places=None):
        self.departure_from = _from
        self.arrival_to = _to
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.train = train
        self.price = price
        self.places = places

    def convert_date(self, date):
        date = date.split(' ')
        date = '{} {}'.format(date[1], date[2])
        new_date = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M')
        return new_date

    def load(self, data):
        self.departure_from = City(data.get('from').get('station'), data.get('from').get('code'))
        self.departure_date = self.convert_date(data.get('from').get('date') + ' ' + data.get('from').get('time'))
        self.arrival_to = City(data.get('to').get('station'), data.get('to').get('code'))
        self.arrival_date = self.convert_date(data.get('to').get('date') + ' ' + data.get('to').get('time'))
        self.train = data.get('num')

        if data.get('types') and isinstance(data.get('types'), list):
            type = data.get('types').pop()
            self.get_wagon_details(type.get('id'))
        return self

    def set_price(self, price):
        # set price if it is less than self.price
        if not self.price:
            self.price = price
        elif price <= self.price:
            self.price = price

    def get_wagon_details(self, type='К'):
        results = []

        date = self.departure_date.strftime("%Y-%m-%d")
        data = {'train': self.train,
                'from': self.departure_from.code,
                'to': self.arrival_to.code,
                'date': date,
                'wagon_type_id': type,
                'get_tpl': 1}

        response = requests.post(Train.REQUEST_TO_SEARCH_WAGON, data=data, headers=HEADERS)

        if 'error' not in response.text:
            data = json.loads(response.text)

            for item in data.get('data').get('types'):
                place = Places().load(item)
                results.append(place)

            results = sorted(results, key=lambda place: place.price)
            self.places = results

            if self.places:
                self.set_price(self.places[0].price)

        return results