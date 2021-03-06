import pytest

from quz.quiz import MultipleChoiceAnswer
from quz.quiz import MultipleChoiceQuestion
from quz.quiz import Quiz
from quz.util import set_logger
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)

CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)

marked_user_input = '?What is 2+3\n-is 4\n+is 5\n\n=addition\n\n' \
                    '?1*2 = ?\n- = 1\n+ = 2\n- = 4\n\n'

question_1_answers = {'answer1': {'is_correct': False, 'is_selected': False, 'answer': 'is 4'},
                      'answer2': {'is_correct': True, 'is_selected': True, 'answer': 'is 5'},
                      'comment': 'addition',
                      'num_of_answers': 2}
question_2_answers = {'answer1': {'is_correct': False, 'is_selected': False, 'answer': ' = 1'},
                      'answer2': {'is_correct': True, 'is_selected': False, 'answer': ' = 2'},
                      'answer3': {'is_correct': False, 'is_selected': False, 'answer': ' = 4'},
                      'num_of_answers': 3}
quiz_data_dict = {'current_question_num': 2,
                  'num_of_questions': 2,
                  'marked_user_input': marked_user_input,
                  'question1': 'What is 2+3',
                  'question1_answers': question_1_answers,
                  'question2': '1*2 = ?',
                  'question2_answers': question_2_answers}

question_1 = MultipleChoiceQuestion("What is 2+3", "addition", [MultipleChoiceAnswer("is 4", False, False),
                                                                MultipleChoiceAnswer("is 5", True, False)])
question_2 = MultipleChoiceQuestion("1*2 = ?", None, [MultipleChoiceAnswer(" = 1", False, False),
                                                      MultipleChoiceAnswer(" = 2", True, False),
                                                      MultipleChoiceAnswer(" = 4", False, False)])

question_1_answered = MultipleChoiceQuestion("What is 2+3", "addition", [MultipleChoiceAnswer("is 4", False, False),
                                                                         MultipleChoiceAnswer("is 5", True, True)])


def test_initialize_with_test_marked_user_input():
    quiz = Quiz( marked_user_input=marked_user_input)

    assert quiz.marked_user_input == marked_user_input

    assert quiz.current_question() == question_1

    assert quiz.next_question() == question_2
    assert quiz.next_question() == question_2

    assert quiz.previous_question() == question_1
    assert quiz.previous_question() == question_1
    assert quiz.score() == ('0/2', '0%')


def test_initialize_with_quiz_data_dict():
    quiz = Quiz(quiz_data_dict=quiz_data_dict)
    assert quiz.marked_user_input == marked_user_input

    assert quiz.current_question() == question_2

    assert quiz.previous_question() == question_1_answered
    assert quiz.previous_question() == question_1_answered

    assert quiz.next_question() == question_2
    assert quiz.next_question() == question_2
    assert quiz.score() == ('1/2', '50%')
