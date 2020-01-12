import quz
import tests.t_util

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'QUIZZES_DIR': TMP_DIR, 'LOG_LEVEL': 'DEBUG'}
quz.util.set_logger(CONFIG)

MARKED_USER_INPUT = '?What is 2+3\n' \
                    '-is 4\n' \
                    '+is 5\n\n' \
                    '=addition\n\n' \
 \
                    '?1*2 = ?\n' \
                    '- = 1\n' \
                    '+ = 2\n' \
                    '- = 4\n\n'
EXPECTED_QUESTION1_ANSWERS = {'answer1': {'is_correct': False,
                                          'is_selected': False,
                                          'answer': 'is 4'},
                              'answer2': {'is_correct': True,
                                          'is_selected': False,
                                          'answer': 'is 5'},
                              'comment': 'addition',
                              'num_of_answers': 2}
EXPECTED_QUESTION2_ANSWERS = {'answer1': {'is_correct': False,
                                          'is_selected': False,
                                          'answer': ' = 1'},
                              'answer2': {'is_correct': True,
                                          'is_selected': False,
                                          'answer': ' = 2'},
                              'answer3': {'is_correct': False,
                                          'is_selected': False,
                                          'answer': ' = 4'},
                              'num_of_answers': 3}
EXPECTED_DATA_DICT = {'latest_question_num': 1,
                      'num_of_completed_questions': 0,
                      'num_of_questions': 2,
                      'marked_user_input': MARKED_USER_INPUT,
                      'question1': 'What is 2+3',
                      'question1_answers': EXPECTED_QUESTION1_ANSWERS,
                      'question2': '1*2 = ?',
                      'question2_answers': EXPECTED_QUESTION2_ANSWERS}
QUIZ = quz.quiz.Quiz(marked_user_input=MARKED_USER_INPUT)


def test_class_initialize():
    assert QUIZ == EXPECTED_DATA_DICT
    question, question_answers = QUIZ.current_question()
    assert question == QUIZ['question1']
    assert question_answers == EXPECTED_QUESTION1_ANSWERS


def test_marked_user_input():
    assert QUIZ == EXPECTED_DATA_DICT
    assert QUIZ.marked_user_input() == MARKED_USER_INPUT


def test_next_question():
    question, question_answers = QUIZ.next_question()
    assert question == QUIZ['question2']
    assert question_answers == EXPECTED_QUESTION2_ANSWERS

    question, question_answers = QUIZ.next_question()
    assert question == QUIZ['question2']
    assert question_answers == EXPECTED_QUESTION2_ANSWERS


def test_latest_question():
    question, question_answers = QUIZ.current_question()
    assert question == QUIZ['question2']
    assert question_answers == EXPECTED_QUESTION2_ANSWERS


def test_previous_question():
    question, question_answers = QUIZ.previous_question()
    assert question == QUIZ['question1']
    assert question_answers == EXPECTED_QUESTION1_ANSWERS

    question, question_answers = QUIZ.previous_question()
    assert question == QUIZ['question1']
    assert question_answers == EXPECTED_QUESTION1_ANSWERS


def test_score():
    quiz = quz.quiz.Quiz(MARKED_USER_INPUT)
    assert quiz.score() == ('0/2', '0%')
    quiz['question1_answers']['answer2']['is_selected'] = True
    assert quiz.score() == ('1/2', '50%')
    quiz['question2_answers']['answer2']['is_selected'] = True
    assert quiz.score() == ('2/2', '100%')

    quiz['question2_answers']['answer3']['is_selected'] = True
    assert quiz.score() == ('1/2', '50%')
    quiz['question1_answers']['answer1']['is_selected'] = True
    assert quiz.score() == ('0/2', '0%')
