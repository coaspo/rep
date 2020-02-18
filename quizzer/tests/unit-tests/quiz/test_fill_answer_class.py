from quz.quiz import FillAnswer
from quz.util import set_logger
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)

CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_correct_answer():
    answer = FillAnswer('2', ' 5 ')
    assert not answer.is_correct()
    answer.answer = ' 2 '
    assert answer.is_correct()


def test_incorrect_answer():
    answer = FillAnswer(' 2', '  2')
    assert answer.is_correct()
    answer.answer = '3'
    assert not answer.is_correct()
