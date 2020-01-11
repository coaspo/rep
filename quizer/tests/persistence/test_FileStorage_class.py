import quz
import tests.t_util
import pytest
from quz.persistence import FileStorage

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'SAVED_QUIZES_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
quz.util.set_logger(CONFIG)


def test_invalid_directories():
    config = {}
    with pytest.raises(Exception, match=r'config missing parameter "SAVED_QUIZES_DIR"'):
        FileStorage(config)

    config = {'SAVED_QUIZES_DIR': '/non-dir/fake-dir'}
    with pytest.raises(Exception, match=r".*\[WinError 3] The system cannot find the path specified: 'C:\\\\non-dir\\\\fake-dir'"):
        FileStorage(config)


def test_valid_config():
    try:
        FileStorage(CONFIG)
    except Exception as e:
        pytest.fail("Unexpected error: " + str(e))


def test_latest_file_num():
    storage = FileStorage(CONFIG)
    with open(storage._save_dir + '/quiz.3.json', 'w') as f:
        f.write('{"a":1}')
    with open(storage._save_dir + '/quiz.2.json', 'w') as f:
        f.write('{"b":2}')
    storage = FileStorage(CONFIG)
    assert storage._latest_file_number == 3
    assert storage._file_paths_index == 1
    assert len(storage._files_paths) == 2


def test_save():
    storage = FileStorage(CONFIG)
    dict4 = {'ques...': 'What is..'}
    msg = storage.save(dict4)
    assert msg.endswith('quiz.4.json')
    assert storage._latest_file_number == 4
    assert storage._file_paths_index == 2
    assert len(storage._files_paths) == 3


def test_read():
    storage = FileStorage(CONFIG)
    dict4 = {'ques...': 'What is..'}
    dict3 = {'a': 1}
    dict2 = {'b': 2}

    #decrement_file_path_index(self):

    assert storage._file_paths_index == 2
    file_path, msg, a_dict = storage.read()
    assert a_dict == dict4
    #
    storage.decrement_file_index()
    file_path, msg, a_dict = storage.read()
    assert a_dict == dict3
    storage.decrement_file_index()
    file_path, msg, a_dict = storage.read()
    assert a_dict == dict2
    storage.decrement_file_index()
    file_path, msg, a_dict = storage.read()
    assert a_dict == dict2

    storage.increment_file_index()
    file_path, msg, a_dict = storage.read()
    assert a_dict == dict3
    storage.increment_file_index()
    file_path, msg, a_dict = storage.read()
    assert a_dict == dict4
    storage.increment_file_index()
    file_path, msg, a_dict = storage.read()
    assert a_dict == dict4
    a_dict['ques...'] = 123
    storage.update(a_dict)
    file_path, msg, a_dict = storage.read()
    assert a_dict == {'ques...': 123}

