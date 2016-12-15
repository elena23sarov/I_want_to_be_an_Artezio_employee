"""Final task."""
import sys
from re import search
import json
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


def to_list(str_1, str_2, lst):
    """Create proper list from strings and list."""
    final_list = [str_1, str_2]
    final_list.extend(lst)
    return final_list


def finder(departure, destination, outbound_date, return_date=''):
    """Find routes."""
    if departure == destination:
        sys.exit('IATA-codes cannot be same')
    return_valid = search(r'^\d{4}-\d{2}-\d{2}$',
                          return_date) if return_date != '' else True
    if not (search(r'^[A-Z]{3}$', departure)
            and search(r'^[A-Z]{3}$', destination)
            and search(r'^\d{4}-\d{2}-\d{2}$', outbound_date)
            and return_valid):
        sys.exit('Wrong format. IATA format: XYZ. Date format: YYYY-MM-DD.')
    oneway = 1 if not return_date else 0
    oneway_flag = 'on' if not return_date else ''

    data = {'departure': departure,
            'destination': destination,
            'outboundDate': outbound_date,
            'returnDate': return_date,
            'oneway': oneway,
            'openDateOverview': 0,
            'adultCount': 1,
            'childCount': 0,
            'infantCount': 0}

    ajax_form = {'_ajax[templates][]': 'main',
                 '_ajax[requestParams][departure]': departure,
                 '_ajax[requestParams][destination]': destination,
                 '_ajax[requestParams][returnDeparture]': '',
                 '_ajax[requestParams][returnDestination]': '',
                 '_ajax[requestParams][outboundDate]': outbound_date,
                 '_ajax[requestParams][returnDate]': return_date,
                 '_ajax[requestParams][adultCount]': 1,
                 '_ajax[requestParams][childCount]': 0,
                 '_ajax[requestParams][infantCount]': 0,
                 '_ajax[requestParams][openDateOverview]': '',
                 '_ajax[requestParams][oneway]': oneway_flag}

    sess = requests.Session()
    get_sid = sess.get('http://www.flyniki.com/ru/booking/'
                       'flight/vacancy.php', params=data)
    HEADERS['Referer'] = get_sid.url
    page = sess.post(get_sid.url, data=ajax_form, headers=HEADERS).json()
    try:
        tree = html.fromstring(page['templates']['main'])
    except KeyError:
        sys.exit('No routes found. Date or IATA-code is incorrect.')

    print '-----OUTBOUND FLIGHT-----'
    show_flights('outbound', tree)
    if oneway_flag == '':
        print '-----RETURN FLIGHT-----'
        show_flights('return', tree)


def show_flights(flag, tree):
    """Find a route and print the table with results."""
    flight_table = [to_list('Flight Time', 'Duration',
                            tree.xpath('.//*[@class="{} block"]/div[2]/'
                                       'table/thead/tr/td/div/label[@id]'
                                       '/p/text()'.format(flag)))]
    for row in tree.xpath('.//*[@class="{} block"]/div[2]/table/'
                          'tbody/tr[@role]'.format(flag)):
        time = '-'.join(row.xpath('.//span[contains(@id,'
                                  '"lightDepartureFi_")]'
                                  '/time[1]/text() | .//span[contains(@id,'
                                  '"flightDepartureFi_")]/time[2]/text()'))
        duration = row.xpath('string(.//span[contains(@id,'
                             '"flightDurationFi_")])')
        prices = row.xpath('.//label/div[1]/span/text() | '
                           './/span[@class="notbookable"]/text()')
        for i, item in enumerate(prices):
            prices[i] = item + 'RUB' if search(r'^[.,\d]+$', item) else '-'
        flight_data = to_list(time, duration, prices)
        flight_table.append(flight_data)
    if len(flight_table) == 1:
        sys.exit('No routes found. Please, choose another date.')
    flights = Texttable()
    flights.add_rows(flight_table)
    print flights.draw()


def main():
    """Give the results."""
    args = sys.argv[1:]
    if not args:
        print "Usage: routes.py <from> <to> <outbound_date> " \
              "<return_date>*   *optional"
        sys.exit(1)
    finder(*args)


if __name__ == '__main__':
    main()
