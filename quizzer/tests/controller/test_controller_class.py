from quz.controller import MainController, PersistenceController
from quz.model import Model
from quz.persistence import FilePersistence
from quz.util import set_logger
from quz.view import View
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_controller_set_up():
    persistence = FilePersistence(TMP_DIR)
    v = View(persistence.latest_topic(), persistence.topics(), '<UI intructions>')

    persistence = FilePersistence(TMP_DIR)
    m = Model(persistence)

    c = MainController(v, m)
    c.bind_main_controls()
    c2 = PersistenceController(v, m)
    c2.bind_persistence_controls()
