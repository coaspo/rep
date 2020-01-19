from quz.quiz import MultipleChoiceAnswer
from quz.util import set_logger
from tests.t_util import recreate_tmp_dir
import quz.quiz

TMP_DIR = recreate_tmp_dir(__file__)

CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_create_answers():
    answers_dict = {'answer1': {'is_correct': False,
                                'is_selected': True,
                                'answer': 'is 4'},
                    'answer2': {'is_correct': True,
                                'is_selected': False,
                                'answer': 'is 5'},
                    'comment': 'addition',
                    'num_of_answers': 2}
    answers = quz.quiz._create_answers(answers_dict)
    assert len(answers) == 2
    a1 = MultipleChoiceAnswer('is 4', False, True)
    assert answers[0] == a1
    a1 = MultipleChoiceAnswer('is 5', True, False)
    assert answers[1] == a1
