import quz.model
import tests.t_util
from quz.persistence import FilePersistence
from quz.model import create_domain_object

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
QUIZ_FILE_PFX = 'quiz'
CONFIG = {'LOG_DIR': TMP_DIR, 'QUIZZES_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL', 'QUIZ_FILE_PFX': QUIZ_FILE_PFX}

quz.util.set_logger(CONFIG)


def test_invalid_directories():
    FilePersistence(None, None)
    assert FilePersistence.file_storage_err_msg == 'JsonFileStorage failed - missing save_dir'

    FilePersistence(save_dir = '/non-dir/fake-dir', file_pfx= 'quiz')
    assert FilePersistence.file_storage_err_msg.find(
        "JsonFileStorage failed - [WinError 3] The system cannot find the path specified") > -1

    persistence = FilePersistence(save_dir = './xyz:\n', file_pfx = 'quiz')
    assert persistence.file_storage_err_msg.find(
        "JsonFileStorage failed - [WinError 267] The directory name is invalid") > -1


def test_obj_attrs():
    persistence = FilePersistence(TMP_DIR, QUIZ_FILE_PFX)
    assert persistence.file_storage_err_msg is None


def test_save():
    persistence = FilePersistence(TMP_DIR, QUIZ_FILE_PFX)

    quiz = {'fake..ques..': 'a'}
    msg = persistence.save(quiz)
    assert msg.endswith('quiz.1.json')

    quiz = {'fake2..ques..': 'a2'}
    msg = persistence.save(quiz)
    assert msg.endswith('quiz.2.json')


def test_get():
    persistence = FilePersistence(TMP_DIR, QUIZ_FILE_PFX)
    file_path, msg, quiz = persistence.get(create_domain_object)
    assert 'quiz.2.json' in file_path
    assert msg == '2.  quiz.2'
    assert quiz == {'fake2..ques..': 'a2'}


def test_get_previous():
    persistence = FilePersistence(TMP_DIR, QUIZ_FILE_PFX)
    file_path, msg, quiz = persistence.get_previous(create_domain_object)
    assert 'quiz.1.json' in file_path
    assert msg == '1.  quiz.1'
    assert quiz == {'fake..ques..': 'a'}
    file_path, msg, quiz = persistence.get_previous(create_domain_object)
    assert 'quiz.1.json' in file_path
    assert msg == '1.  quiz.1'
    assert quiz == {'fake..ques..': 'a'}


def test_get_next():
    persistence = FilePersistence(TMP_DIR, QUIZ_FILE_PFX)
    file_path, msg, quiz = persistence.get_next(create_domain_object)
    assert 'quiz.2.json' in file_path
    assert msg == '2.  quiz.2'
    assert quiz == {'fake2..ques..': 'a2'}
    file_path, msg, quiz = persistence.get_next(create_domain_object)
    assert 'quiz.2.json' in file_path
    assert msg == '2.  quiz.2'
    assert quiz == {'fake2..ques..': 'a2'}


def test_delete():
    persistence = FilePersistence(TMP_DIR, QUIZ_FILE_PFX)
    persistence.delete()

    file_path, msg, quiz = persistence.get(create_domain_object)
    assert 'quiz.1.json' in file_path
    assert msg == '1.  quiz.1'
    assert quiz == {'fake..ques..': 'a'}


def test_update():
    persistence = FilePersistence(TMP_DIR, QUIZ_FILE_PFX)
    quiz_new = {'real?..ques..': 'A'}
    persistence.update(quiz_new)

    file_path, msg, quiz = persistence.get(create_domain_object)
    assert 'quiz.1.json' in file_path
    assert msg == '1.  quiz.1'
    assert quiz == quiz_new
