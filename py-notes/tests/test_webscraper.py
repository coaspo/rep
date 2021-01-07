import tests.t_util
from skrp.webscraper import get_table_rows, row_data

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)


def test_aaa():
    print('aaaaaa')
    url = 'http://pokemondb.net/pokedex/all'
    table_rows = get_table_rows(url)
    print('==========', table_rows)
    column_names = []
    country_stats = row_data(table_rows, column_names)
