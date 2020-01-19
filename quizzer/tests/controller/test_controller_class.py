from quz.controller import QuizController, PersistenceController
from quz.model import Model
from quz.persistence import file_prefixes, FilePersistence
from quz.util import set_logger
from quz.view import View
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_controller_set_up():
    latest_quiz_category, quiz_categories = file_prefixes(TMP_DIR)
    v = View(latest_quiz_category, quiz_categories, '<UI intructions>')

    persistence = FilePersistence(TMP_DIR, latest_quiz_category)
    m = Model(persistence)

    c = QuizController(v, m)
    c.bind_quiz_controls()
    c2 = PersistenceController(v, m)
    c2.bind_persistence_controls()
