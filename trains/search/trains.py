import json
import requests
import datetime

from itertools import product

from search.train import Train
from search.city import City


HEADERS = {'User-Agent':  'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}


class Trains:
    def __init__(self):
        self._trains = set()
        self.search_methods = (self.get_by_fixed_date, self.get_by_date_range)

    @staticmethod
    def loads(data):
        trains = []
        data = data.get('data').get('list')
        for train in data:
            _train = Train().load(train)
            trains.append(_train)
        return trains

    def get_cheapest_ticket(self, trains, *args, **kwargs):
        train = None
        if trains:
            sorted(trains, key=lambda train: train.price)
            train = trains[0]
            place = sorted(train.places, key=lambda place: place.price)[0]
            train.places = [place]

        return train

    def get_by_lowest_price(self, price_up_to, trains, *args, **kwargs):
        return [train for train in trains if train.price and train.price <= price_up_to]

    def get_by_fixed_date(self, form_data, date, *args, **kwargs):
        departure_from = City.get_citiest_by_name(form_data.get('from'))
        arrive_to = City.get_citiest_by_name(form_data.get('to'))
        results = []

        for _from, _to in product(departure_from, arrive_to):

            data = {'from': _from.code,
                    'to': _to.code,
                    'date': date.strftime('%Y-%m-%d'),
                    'time': "00:00"}

            response = requests.post(Train.REQUEST_TO_SEARCH_TRAIN, data=data, headers=HEADERS)

            if 'error' not in response.text:
                results.extend(self.loads(json.loads(response.text)))

        return results

    def get_by_date_range(self, form_data, date_from, date_to, *args, **kwargs):
        results = []

        departure_from = City.get_citiest_by_name(form_data.get('from'))[0]
        arrive_to = City.get_citiest_by_name(form_data.get('to'))[0]

        while date_from < date_to:

            data = {'from': departure_from.code,
                    'to': arrive_to.code,
                    'date': date_from.strftime('%Y-%m-%d'),
                    'time': "00:00"}

            response = requests.post(Train.REQUEST_TO_SEARCH_TRAIN, data=data, headers=HEADERS)
            results.extend(self.loads(json.loads(response.text)))
            date_from = date_from + datetime.timedelta(days=1)
        return results




