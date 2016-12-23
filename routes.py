"""Final task."""
import sys
from re import search
import datetime as dt
import itertools
from lxml import html
import requests
from texttable import Texttable

HEADERS = {'Accept': 'application/json, text/javascript, */*',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'ru,en-US;q=0.8,en;q=0.6,ja;q=0.4',
           'Cache-Control': 'max-age=0',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Host': 'www.flyniki.com',
           'Origin': 'http://www.flyniki.com',
           'Proxy-Connection': 'keep-alive',
           'X-Requested-With': 'XMLHttpRequest'}

DATA = {'openDateOverview': 0,
        'adultCount': 1,
        'childCount': 0,
        'infantCount': 0}

AJAX_FORM = {'_ajax[templates][]': 'main',
             '_ajax[requestParams][returnDeparture]': '',
             '_ajax[requestParams][returnDestination]': '',
             '_ajax[requestParams][adultCount]': 1,
             '_ajax[requestParams][childCount]': 0,
             '_ajax[requestParams][infantCount]': 0,
             '_ajax[requestParams][openDateOverview]': ''}


def to_list(str_1, str_2, lst):
    """Create proper list from strings and list."""
    final_list = [str_1, str_2]
    final_list.extend(lst)
    return final_list


def format_price(value):
    """Change price type to float."""
    if value == '-':
        return 0
    value = value.replace('.', '').replace(',', '.')
    price_float = float(value[:-3])
    return price_float


def arg_validator(departure, destination, outbound_date, return_date=''):
    """Check if arguments are correct or not."""
    if departure == destination:
        sys.exit('IATA-codes cannot be same')
    return_valid = search(r'^\d{4}-\d{2}-\d{2}$',
                          return_date) if return_date != '' else True
    if not (search(r'^[A-Z]{3}$', departure)
            and search(r'^[A-Z]{3}$', destination)
            and search(r'^\d{4}-\d{2}-\d{2}$', outbound_date)
            and return_valid):
        sys.exit('Wrong format. IATA format: XYZ. Date format: YYYY-MM-DD.')
    date_today = dt.datetime.combine(dt.date.today(), dt.time(0, 0))
    date_border = date_today.replace(year=date_today.year + 1)
    out_date = dt.datetime.strptime(outbound_date, "%Y-%m-%d")
    if not date_today <= out_date <= date_border:
        sys.exit('Entered date is out of the range we can search in.')
    if return_date:
        in_date = dt.datetime.strptime(return_date, "%Y-%m-%d")
        if not date_today <= in_date <= date_border:
            sys.exit('Entered date is out of the range we can search in.')
    prepare_request(departure, destination, outbound_date, return_date)


def prepare_request(departure, destination, outbound_date, return_date):
    """Make dicts for request."""
    DATA['departure'] = departure
    DATA['destination'] = destination
    DATA['outboundDate'] = outbound_date
    DATA['returnDate'] = return_date
    DATA['oneway'] = 0 if return_date else 1

    AJAX_FORM['_ajax[requestParams][departure]'] = departure
    AJAX_FORM['_ajax[requestParams][destination]'] = destination
    AJAX_FORM['_ajax[requestParams][outboundDate]'] = outbound_date
    AJAX_FORM['_ajax[requestParams][returnDate]'] = return_date
    AJAX_FORM['_ajax[requestParams][oneway]'] = '' if return_date else 'on'


def route_finder():
    """Make request to the www.flyniki.com."""
    sess = requests.Session()
    get_sid = sess.get('http://www.flyniki.com/ru/booking/'
                       'flight/vacancy.php', params=DATA)
    HEADERS['Referer'] = get_sid.url
    page = sess.post(get_sid.url, data=AJAX_FORM, headers=HEADERS).json()

    try:
        tree = html.fromstring(page['templates']['main'])
    except KeyError:
        sys.exit('No routes found. Date or IATA-code is incorrect.')

    if DATA['oneway'] == 1:
        print '-----ONEWAY FLIGHT-----'
        final = route_parser('outbound', tree, 1)[0]
    else:
        print '-----ROUND FLIGHT-----'
        out = route_parser('outbound', tree)[0][1:]
        inb = route_parser('return', tree)[0][1:]
        final = [['Time Out', 'Duration', 'Time In', 'Duration', 'Price']]
        cur = route_parser('outbound', tree)[1]
        for pair in itertools.product(out, inb):
            sums_out = [format_price(i) for i in pair[0][2]]
            sums_in = [format_price(i) for i in pair[1][2]]
            for price in itertools.product(sums_out, sums_in):
                if 0 not in price:
                    final.append([pair[0][0], pair[0][1], pair[1][0],
                                  pair[1][1], '{} {}'.format(sum(price), cur)])
    return final


def route_parser(way, tree, flag=None):
    """Find a route and print the table with results."""
    flight_table = [to_list('Flight Time', 'Duration',
                            tree.xpath('.//*[@class="{} block"]/div[2]/'
                                       'table/thead/tr/td/div/label[@id]'
                                       '/p/text()'.format(way)))]
    currency = tree.xpath('string(.//*[@id="flighttables"]/div[1]/div[2]/'
                          'table/thead/tr[2]/th[@id][1])').strip()
    for row in tree.xpath('.//*[@class="{} block"]/div[2]/table/'
                          'tbody/tr[@role]'.format(way)):
        time = '-'.join(row.xpath('.//span[contains(@id,'
                                  '"lightDepartureFi_")]'
                                  '/time[1]/text() | .//span[contains(@id,'
                                  '"flightDepartureFi_")]/time[2]/text()'))
        duration = row.xpath('string(.//span[contains(@id,'
                             '"flightDurationFi_")])')
        prices = row.xpath('.//label/div[1]/span/text() | '
                           './/span[@class="notbookable"]/text()')
        for i, item in enumerate(prices):
            prices[i] = item + currency if search(r'^[.,\d]+$', item) else '-'
        flight_data = to_list(time, duration, prices) if flag \
            else [time, duration, prices]
        flight_table.append(flight_data)
    if len(flight_table) == 1:
        sys.exit('No routes found. Please, choose another date.')
    return flight_table, currency


def main():
    """Give the results."""
    args = sys.argv[1:]
    if not 3 <= len(args) <= 4:
        print "Usage: routes.py <from> <to> <outbound_date> " \
              "<return_date>*   *optional"
        sys.exit(1)
    arg_validator(*args)
    final = route_finder()
    flights = Texttable()
    flights.add_rows(final)
    print flights.draw()


if __name__ == '__main__':
    main()
