import quz
import tests.t_util

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'DICTIONARY_DIR': TMP_DIR, 'LOG_LEVEL': 'INFO'}
quz.util.set_logger(CONFIG)


def test_model():
    pass
    # model = quz.model.Model(CONFIG, None, None)
