from quz.controller import QuizController, PersistenceController
from quz.model import Model
from quz.persistence import file_prefixes, FilePersistence
from quz.util import set_logger
from quz.view import View
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_model_set_up():
    latest_quiz_category, _ = file_prefixes(TMP_DIR)
    persistence = FilePersistence(TMP_DIR, latest_quiz_category)
    Model(persistence)
