import traceback

from quz.persistence import JsonFileStorage
import pytest
import quz
import tests.t_util
from quz.quiz import Quiz

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'QUIZZES_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
quz.util.set_logger(CONFIG)


def test_invalid_directories():
    with pytest.raises(Exception, match=r".*The system cannot find the path specified:"):
        JsonFileStorage('/non-dir/fake-dir', '', None)


def test_valid_config():
    try:
        JsonFileStorage(TMP_DIR, 'quizCat1', None)
    except Exception as e:
        pytest.fail("Unexpected error: " + str(e) + '/n' + traceback.format_exc())


def test_latest_file_num():
    storage = JsonFileStorage(TMP_DIR, 'quizCat1', None)
    with open(storage._save_dir + '/quizCat1.3.json', 'w') as f:
        f.write('{"a":1}')
    with open(storage._save_dir + '/quizCat1.2.json', 'w') as f:
        f.write('{"b":2}')
    storage = JsonFileStorage(TMP_DIR, 'quizCat1', None)
    assert storage._latest_file_number == 3
    assert storage._active_file_index == 1
    assert len(storage._files_paths) == 2


def test_save():
    storage = JsonFileStorage(TMP_DIR, 'quizCat1', None)
    dict4 = {'ques...': 'What is..'}
    msg = storage.save_file(dict4)
    assert 'quizCat1.4.json' in msg
    assert storage._latest_file_number == 4
    assert storage._active_file_index == 2
    assert len(storage._files_paths) == 3


def test_read():
    storage = JsonFileStorage(TMP_DIR, 'quizCat1', None)
    dict4 = {'ques...': 'What is..'}
    dict3 = {'a': 1}
    dict2 = {'b': 2}

    # decrement_file_path_index(self):

    assert storage._active_file_index == 2
    file_path, msg, a_dict = storage.read_active_file()
    assert a_dict == dict4
    #
    storage.decrement_file_index()
    file_path, msg, a_dict = storage.read_active_file()
    assert a_dict == dict3
    storage.decrement_file_index()
    file_path, msg, a_dict = storage.read_active_file()
    assert a_dict == dict2
    storage.decrement_file_index()
    file_path, msg, a_dict = storage.read_active_file()
    assert a_dict == dict2

    storage.increment_file_index()
    file_path, msg, a_dict = storage.read_active_file()
    assert a_dict == dict3
    storage.increment_file_index()
    file_path, msg, a_dict = storage.read_active_file()
    assert a_dict == dict4
    storage.increment_file_index()
    file_path, msg, a_dict = storage.read_active_file()
    assert a_dict == dict4
    a_dict['ques...'] = 123
    storage.update_file(a_dict)
    file_path, msg, a_dict = storage.read_active_file()
    assert a_dict == {'ques...': 123}


def test_file_name():
    storage = JsonFileStorage(TMP_DIR, 'quizCat1', latest_file_name='quizCat1.3.json')
    assert storage._latest_file_number == 4
    assert storage._active_file_index == 1
    assert len(storage._files_paths) == 3


def test_save_quiz():
    marked_user_input = '?What is 2+3\n-is 4\n+is 5\n\n=addition\n\n' \
                        '?1*2 = ?\n- = 1\n+ = 2\n- = 4\n\n'
    quiz = Quiz(quiz_topic='test', marked_user_input=marked_user_input)

    storage = JsonFileStorage(TMP_DIR, 'quizCat1', None)
    msg = storage.save_file(quiz.data_dict())
    assert 'quizCat1' in msg
