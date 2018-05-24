from flask import Flask, render_template, url_for, request
from search.analizer import Searcher

app = Flask(__name__, static_url_path='/static')
DEFAULT_FORM_DATA = {'from': '',
                     'to': '',
                     'price_up_to': 'Any',
                     'fixed_date': '',
                     'from_date': '',
                     'to_date': ''}


@app.route('/')
def home():
    return render_template('index.html', result={}, error=None,
                           form_data=DEFAULT_FORM_DATA, cheapest_ticket=None)


@app.route('/search', methods=['GET', 'POST'])
def search():
    result = {}
    error = None
    cheapest_ticket = None

    form_data = request.form

    if form_data:
        result, cheapest_ticket, error = Searcher().search(form_data)
    else:
        form_data = DEFAULT_FORM_DATA

    return render_template('index.html', result=result,
                           error=error, form_data=form_data,
                           cheapest_ticket=cheapest_ticket)


if __name__ == '__main__':
    app.run()
