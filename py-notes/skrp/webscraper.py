import logging
import traceback

import lxml.html
import requests

log = logging.getLogger(__name__)


def get_table_rows(url: str):
    page = requests.get(url)
    doc = lxml.html.fromstring(page.content)
    return doc.xpath('//tr')


def row_data(table_rows: list, first_column_names: list):
    data = dict()
    for j in range(1, len(table_rows)):
        row_columns = table_rows[j]
        a = [t.text_content() for t in row_columns.iterchildren()]
        # print(a)
        if a[0] in first_column_names:
            a = [x.replace(',', '') for x in a]
            data[a[0]] = a[1:]
    return data


def main():
    try:
        print('start')
        # https://www.worldometers.info/coronavirus/
        # http://pokemondb.net/pokedex/all
        url = 'https://www.worldometers.info/coronavirus/'
        table_rows = get_table_rows(url)
        column_names = ['Total:', 'USA', 'Germany', 'Japan', 'Italy', 'World', 'UK', 'Greece']
        country_stats = row_data(table_rows, column_names)
        print(country_stats)

        url = 'https://www.worldometers.info/coronavirus/country/us/'
        table_rows = get_table_rows(url)
        column_names = ['Total:', 'Massachusetts', 'New York', 'California']
        state_stats = row_data(table_rows, column_names)
        print(state_stats)

    except Exception as exc:
        exc_trace = str(exc) + '\n\t' + traceback.format_exc()
        log.error(exc_trace)


if __name__ == '__main__':
    main()
