from quz.controller import MainController
from quz.model import Model
from quz.util import set_logger, Config
from quz.view import View
from tests.t_util import recreate_tmp_dir

TMP_DIR = recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_missing_marked_text():
    m = Model(TMP_DIR)
    v = View(m.latest_quiz_topic, m.quiz_topics, '<UI instructions>')
    assert v.quiz_topics.get() == 'quiz'
    assert v.status_label.cget('text') == '<UI instructions>'
    c = MainController(v, m)
    v.input_marked_text_area.insert('insert', 'aaaa')
    c.update_quiz(1)
    assert v.status_label.cget('text') == Config.MARKED_TEXT_ERR


def test_save_marked_text():
    m = Model(TMP_DIR)
    v = View(m.latest_quiz_topic, m.quiz_topics, 'fake instructions')
    c = MainController(v, m)
    v.input_marked_text_area.insert('insert', '?What is 2+3\n'
                                              '-is 4\n'
                                              '+is 5\n\n'
                                              '=addition\n\n'
                                              '?1*2 = ?\n'
                                              '- = 1\n'
                                              '+ = 2\n'
                                              '- = 4\n\n')
    c.update_quiz('fake-event')
    assert v.status_label.cget('text').startswith('Saved quiz')
    assert v.quiz_description_label.cget('text').startswith('1/1  quiz.1.json')
    assert v.question_label.cget('text') == 'What is 2+3'
    assert v.question_comment_label.cget('text') == 'addition'
