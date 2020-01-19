from quz.quiz import MultipleChoiceAnswer
from quz.quiz import MultipleChoiceQuestion
from quz.util import set_logger
from tests.t_util import recreate_tmp_dir
import quz.quiz

TMP_DIR = recreate_tmp_dir(__file__)

CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_create_questions():
    question1_answers = {'answer1': {'is_correct': False, 'is_selected': False, 'answer': 'is 4'},
                         'answer2': {'is_correct': True, 'is_selected': False, 'answer': 'is 5'},
                         'comment': 'addition',
                         'num_of_answers': 2}
    question2_answers = {'answer1': {'is_correct': False, 'is_selected': False, 'answer': ' = 1'},
                         'answer2': {'is_correct': True, 'is_selected': False, 'answer': ' = 2'},
                         'answer3': {'is_correct': False, 'is_selected': False, 'answer': ' = 4'},
                         'num_of_answers': 3}
    quiz_data_dict = {'current_question_num': 2,
                      'num_of_questions': 2,
                      'marked_user_input': '?aaa/n+bbb/n-ccc...',
                      'question1': 'What is 2+3',
                      'question1_answers': question1_answers,
                      'question2': '1*2 = ?',
                      'question2_answers': question2_answers}

    questions = quz.quiz._create_questions(quiz_data_dict)
    assert len(questions) == 2

    expected = MultipleChoiceQuestion("What is 2+3", "addition", [MultipleChoiceAnswer("is 4", False, False),
                                                                  MultipleChoiceAnswer("is 5", True, False)])
    assert questions[0] == expected

    expected = MultipleChoiceQuestion("1*2 = ?", None, [MultipleChoiceAnswer(" = 1", False, False),
                                                        MultipleChoiceAnswer(" = 2", True, False),
                                                        MultipleChoiceAnswer(" = 4", False, False)])
    assert questions[1] == expected
