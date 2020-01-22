from quz.persistence import FilePersistence
import quz.model
import tests.t_util

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
QUIZ_FILE_PFX = 'quiz'
CONFIG = {'LOG_DIR': TMP_DIR, 'QUIZZES_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}

quz.util.set_logger(CONFIG)


def _create_fake_domain_object(data_dict: dict) -> dict:
    return data_dict


def test_invalid_directories():
    FilePersistence('/non-dir/fake-dir')
    assert "The system cannot find the path specified" in FilePersistence.file_storage_err_msg

    FilePersistence('./xyz:\n')
    assert "The directory name is invalid" in FilePersistence.file_storage_err_msg


def test_obj_attrs():
    persistence = FilePersistence(TMP_DIR)
    assert persistence.file_storage_err_msg is None


def test_save():
    persistence = FilePersistence(TMP_DIR)

    quiz = {'fake..ques..': 'a'}
    msg = persistence.save(quiz)
    assert msg.endswith('quiz.1.json')

    quiz = {'fake2..ques..': 'a2'}
    msg = persistence.save(quiz)
    assert msg.endswith('quiz.2.json')


def test_get():
    persistence = FilePersistence(TMP_DIR)
    file_path, msg, quiz = persistence.get(_create_fake_domain_object)
    assert 'quiz.2.json' in file_path
    assert msg == '2.  quiz.2'
    assert quiz == {'fake2..ques..': 'a2'}


def test_get_previous():
    persistence = FilePersistence(TMP_DIR)
    file_path, msg, quiz = persistence.get_previous(_create_fake_domain_object)
    assert 'quiz.1.json' in file_path
    assert msg == '1.  quiz.1'
    assert quiz == {'fake..ques..': 'a'}
    file_path, msg, quiz = persistence.get_previous(_create_fake_domain_object)
    assert 'quiz.1.json' in file_path
    assert msg == '1.  quiz.1'
    assert quiz == {'fake..ques..': 'a'}


def test_get_next():
    persistence = FilePersistence(TMP_DIR)
    file_path, msg, quiz = persistence.get_next(_create_fake_domain_object)
    assert 'quiz.2.json' in file_path
    assert msg == '2.  quiz.2'
    assert quiz == {'fake2..ques..': 'a2'}
    file_path, msg, quiz = persistence.get_next(_create_fake_domain_object)
    assert 'quiz.2.json' in file_path
    assert msg == '2.  quiz.2'
    assert quiz == {'fake2..ques..': 'a2'}


def test_delete():
    persistence = FilePersistence(TMP_DIR)
    persistence.delete()

    file_path, msg, quiz = persistence.get(_create_fake_domain_object)
    assert 'quiz.1.json' in file_path
    assert msg == '1.  quiz.1'
    assert quiz == {'fake..ques..': 'a'}


def test_update():
    persistence = FilePersistence(TMP_DIR)
    quiz_new = {'real?..ques..': 'A'}
    persistence.update(quiz_new)

    file_path, msg, quiz = persistence.get(_create_fake_domain_object)
    assert 'quiz.1.json' in file_path
    assert msg == '1.  quiz.1'
    assert quiz == quiz_new
