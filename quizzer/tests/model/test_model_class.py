from quz.model import Model
from quz.persistence import FilePersistence
from quz.util import set_logger
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_model_set_up():
    persistence = FilePersistence(TMP_DIR)
    Model(persistence)
