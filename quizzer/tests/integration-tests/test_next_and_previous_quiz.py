import glob
import json
from tkinter import END, DISABLED, NORMAL

from quz.controller import QuizController
from quz.model import Model
from quz.util import set_logger, Config
from quz.view import View
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


m: Model
v: View
c: QuizController


def test_next_quiz():
    global m, v, c
    m = Model(TMP_DIR)
    v = View(m.latest_quiz_topic, m.quiz_topics, 'fake instructions')
    c = QuizController(v, m)
    v.input_marked_text_area.insert('insert', '?What is 2+3\n'
                                              '-is 4\n'
                                              '+is 5\n\n'
                                              '=addition\n\n'
                                              '?1*2 = ?\n'
                                              '- = 1\n'
                                              '+ = 2\n'
                                              '- = 4\n\n')
    c.update_quiz('fake-mouse-leave-event')
    assert v.status_label.cget('text').startswith('Saved quiz file')
    assert v.quiz_description_label.cget('text').startswith('1/1  quiz.1.json')
    c.update_quiz('fake-mouse-leave-event')
    assert v.status_label.cget('text').startswith('Saved quiz file')
    assert v.quiz_description_label.cget('text').startswith('1/1  quiz.1.json')
    assert 'What is 2+3' == v.question_label.cget('text')
    assert 'addition' == v.question_comment_label.cget('text')
    v.input_marked_text_area.insert('insert', '?What is 2+33333333\n'
                                              '-is 444444444\n'
                                              '+is 5444444444\n\n'
                                              '=additionnnnnnnnnn\n\n'
                                              '?1*2 = ?///////////\n'
                                              '- = 111111111111\n'
                                              '+ = 222222222222\n'
                                              '- = 44444444444\n\n')
    c.update_quiz('fake-mouse-leave-event')

