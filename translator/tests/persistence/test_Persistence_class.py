import ltrans
import ltrans.model
import tests.t_util

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'SAVED_TRANSLATIONS_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
ltrans.util.set_logger(CONFIG)

def test_invalid_directories():
    config = {}
    persistence = ltrans.persistence.Persistence(config)
    assert(persistence._err_msg == 'config missing parameter "SAVED_TRANSLATIONS_DIR"')

    config = {'SAVED_TRANSLATIONS_DIR': '/non-dir/fake-dir'}
    persistence = ltrans.persistence.Persistence(config)
    assert(persistence._err_msg == r"[WinError 3] The system cannot find the path specified: 'C:\\non-dir\\fake-dir'")

    config = {'SAVED_TRANSLATIONS_DIR': './xx:\n'}
    persistence = ltrans.persistence.Persistence(config)
    assert (persistence._err_msg == r"[WinError 267] The directory name is invalid: 'C:\\Users\\coasp\\d\\rep\\translator\\ltrans\\xx:\n'")

def test_obj_attrs():
    persistence = ltrans.persistence.Persistence(CONFIG)
    assert 'tmp' in persistence._save_dir
    assert persistence._err_msg is None
    assert persistence._latest_trans_number == 0
    assert persistence._file_path_index == -1

def test_latest_trans_num():
    persistence = ltrans.persistence.Persistence(CONFIG)
    with open(persistence._save_dir + '/Italian-English.3.json', 'w') as f:
        f.write('{"a":1}')
    with open(persistence._save_dir + '/Spanish-English.1.json', 'w') as f:
        f.write('{"b":2}')
    persistence = ltrans.persistence.Persistence(CONFIG)
    assert persistence._latest_trans_number == 3
    assert persistence._file_path_index == 1
    assert len(persistence._files_paths) == 2

def test_save_tranlation():
    persistence = ltrans.persistence.Persistence(CONFIG)
    user_input = ltrans.model.UserInput('This is\na test', 'English', 'French', 0, 1,'test')
    print('$$$$$$$$', type(user_input))
    translated_text = 'This is\nCette est\n\na test\nune tester'
    msg = persistence.save_translation(user_input, translated_text, False)
    assert msg.startswith('Saved or replaced translation in:') and msg.endswith('English-French.4.json')
    assert persistence._latest_trans_number == 4
    assert persistence._file_path_index == 2
    assert len(persistence._files_paths) == 3

def test_read_next_and_prev():
    persistence = ltrans.persistence.Persistence(CONFIG)
    actual_trans = {'dest_language': 'French',
                    'is_add_src': 0,
                    'is_add_transliteration': 1,
                    'src_language': 'English',
                    'text_lines': 'This is\na test',
                    'translated_text': 'This is\nCette est\n\na test\nune tester'}
    json_doc1 = {'a': 1}
    json2 = {'b': 2}

    assert persistence._file_path_index == 2
    trans = persistence.read_next()
    assert trans == json2 and persistence._file_path_index == 2

    trans = persistence.read_prev()
    assert trans == json_doc1 and persistence._file_path_index == 1
    trans = persistence.read_prev()
    assert trans == actual_trans and persistence._file_path_index == 0
    trans = persistence.read_prev()
    assert trans == actual_trans and persistence._file_path_index == 0

    trans = persistence.read_next()
    assert trans == json_doc1 and persistence._file_path_index == 1
    trans = persistence.read_next()
    assert trans == json2 and persistence._file_path_index == 2
    trans = persistence.read_next()
    assert trans == json2 and persistence._file_path_index == 2

def test_filepath():
    persistence = ltrans.persistence.Persistence(CONFIG)
    user_input = ltrans.model.UserInput('This is\na test', 'English', 'French', 0, 1, 'testing')
    translated_text = 'This is\nCette est\n\na test\nune tester'
    msg = persistence.save_translation(user_input, translated_text)
    assert msg.startswith('Saved or replaced translation in:') and msg.endswith('English-French.5.json')
