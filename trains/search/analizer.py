import datetime
from search.trains import Trains


class IncorrectDate(Exception):
    pass


class Searcher:
    def validate_date_data(self, data):
        try:
            date = {}
            now = datetime.datetime.now()
            if data.get('from_date') and data.get('to_date'):
                from_date = datetime.datetime.strptime(data.get('from_date'), '%Y-%m-%d')
                to_date = datetime.datetime.strptime(data.get('to_date'), '%Y-%m-%d')

                if from_date.date() >= now.date() and from_date < to_date:
                    date['date_range'] = {'date_from': from_date,
                                          'date_to': to_date}
                else:
                    raise Exception("Date range should be correct, "
                                    "date from should be >= now date")
            elif data.get('fixed_date'):
                fixed_date = datetime.datetime.strptime(data.get('fixed_date'), '%Y-%m-%d')

                if fixed_date.date() >= now.date():
                    date['fixed_date'] = fixed_date
                else:
                    raise Exception("Date should be correct and  >= now date")
            return date
        except Exception as e:
            raise IncorrectDate("Incorrect date format. Date range should be correct, date from should be >= now date")

    def search(self, form_data, *args, **kwargs):
        result = {}
        error = None
        cheapest_ticket = None
        trains = []

        try:

            date = self.validate_date_data(form_data)

            if date.get('date_range'):
                result['date range'] = Trains().get_by_date_range(form_data, date.get('date_range').get('date_from'),
                                                                  date.get('date_range').get('date_to'))

            if date.get('fixed_date'):
                result['fixed date'] = Trains().get_by_fixed_date(form_data, date.get('fixed_date'))

            if result.get('date range'):
                trains = result['date range']
            elif result.get('fixed date'):
                trains = result['fixed date']

            cheapest_ticket = Trains().get_cheapest_ticket(trains)

            price_up_to = float(form_data.get('price_up_to')) if form_data.get('price_up_to') else None

            if price_up_to:
                price_up_to = float(form_data.get('price_up_to')) if form_data.get('price_up_to') else 150

                result['Price up to {}'.format(price_up_to)] = \
                    Trains().get_by_lowest_price(price_up_to, trains, *args, **kwargs)

        except IncorrectDate as e:
            error = str(e)

        except Exception as e:
            print('Exception while trying to get trains by price. Price = {}; {}'.format(form_data.get('price_up_to'),
                                                                                         str(e)))

        return result, cheapest_ticket, error
