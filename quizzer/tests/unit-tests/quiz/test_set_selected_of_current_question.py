from quz.quiz import MultipleChoiceAnswer
from quz.quiz import MultipleChoiceQuestion
from quz.quiz import Quiz
from quz.util import set_logger
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)

CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)

def test_is_same_as():
    marked_user_input = '?What is 2+3\n-is 4\n+is 5\n\n=addition\n\n' \
                        '?1*2 = ?\n- = 1\n+ = 2\n- = 400\n\n'
    quiz = Quiz(marked_user_input=marked_user_input)
    print('---cc-')
    print(quiz.is_any_question_answered())
    assert not quiz.is_any_question_answered()
    quiz.set_selected_of_current_question(1, True)
    assert str(quiz.current_question()) == 'MultipleChoiceQuestion("What is 2+3", "addition", [MultipleChoiceAnswer("is 4", False, False), MultipleChoiceAnswer("is 5", True, True)])'
    print('---cc-')
    assert quiz.is_any_question_answered()
    print(quiz.is_any_question_answered())
