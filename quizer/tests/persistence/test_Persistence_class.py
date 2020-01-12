import quz.model
import tests.t_util
from quz.persistence import Persistence

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'QUIZZES_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}

quz.util.set_logger(CONFIG)


def test_invalid_directories():
    config = {}
    Persistence(config)
    assert Persistence.file_storage_err_msg == 'FileStorage failed - config missing parameter "QUIZZES_DIR"'

    config = {'QUIZZES_DIR': '/non-dir/fake-dir'}
    Persistence(config)
    assert Persistence.file_storage_err_msg.find(
        "FileStorage failed - [WinError 3] The system cannot find the path specified") > -1

    config = {'QUIZZES_DIR': './xyz:\n'}
    persistence = Persistence(config)
    assert persistence.file_storage_err_msg.find(
        "FileStorage failed - [WinError 267] The directory name is invalid") > -1


def test_obj_attrs():
    persistence = Persistence(CONFIG)
    assert persistence.file_storage_err_msg is None


def test_save():
    persistence = Persistence(CONFIG)

    quiz = {'fake..ques..': 'a'}
    msg = persistence.save(quiz)
    assert msg.endswith('quiz.1.json')

    quiz = {'fake2..ques..': 'a2'}
    msg = persistence.save(quiz)
    assert msg.endswith('quiz.2.json')


def test_get():
    persistence = Persistence(CONFIG)
    file_path, msg, quiz = persistence.get()
    assert 'quiz.2.json' in file_path
    assert msg == '2.  quiz.2'
    assert quiz == {'fake2..ques..': 'a2'}


def test_get_previous():
    persistence = Persistence(CONFIG)
    file_path, msg, quiz = persistence.get_previous()
    assert 'quiz.1.json' in file_path
    assert msg == '1.  quiz.1'
    assert quiz == {'fake..ques..': 'a'}
    file_path, msg, quiz = persistence.get_previous()
    assert 'quiz.1.json' in file_path
    assert msg == '1.  quiz.1'
    assert quiz == {'fake..ques..': 'a'}


def test_get_next():
    persistence = Persistence(CONFIG)
    file_path, msg, quiz = persistence.get_next()
    assert 'quiz.2.json' in file_path
    assert msg == '2.  quiz.2'
    assert quiz == {'fake2..ques..': 'a2'}
    file_path, msg, quiz = persistence.get_next()
    assert 'quiz.2.json' in file_path
    assert msg == '2.  quiz.2'
    assert quiz == {'fake2..ques..': 'a2'}


def test_delete():
    persistence = Persistence(CONFIG)
    persistence.delete()

    file_path, msg, quiz = persistence.get()
    assert 'quiz.1.json' in file_path
    assert msg == '1.  quiz.1'
    assert quiz == {'fake..ques..': 'a'}


def test_update():
    persistence = Persistence(CONFIG)
    quiz_new = {'real?..ques..': 'A'}
    persistence.update(quiz_new)

    file_path, msg, quiz = persistence.get()
    assert 'quiz.1.json' in file_path
    assert msg == '1.  quiz.1'
    assert quiz == quiz_new
