from quz.persistence import FilePersistence
from quz.util import set_logger
from quz.view import View
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_view_set_up():
    persistence = FilePersistence(TMP_DIR)
    v = View(persistence.latest_topic(), persistence.topics(), 'instructions....')
    #  v._root.update() # disabled because screen flashes
