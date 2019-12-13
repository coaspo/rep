import ltrans
import ltrans.model
import tests.t_util
from ltrans.persistence import Persistence

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'SAVED_TRANSLATIONS_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
TRANSLATION = {'dest_language': 'French',
                'is_add_src': 0,
                'is_add_transliteration': 1,
                'src_language': 'English',
                'text_lines': 'This is\na test',
                'translated_text': 'This is\nCette est\n\na test\nune tester'}

ltrans.util.set_logger(CONFIG)


def test_invalid_directories():
    config = {}
    persistence = Persistence(config)
    assert Persistence.err_msg == 'FileStorage failed - config missing parameter "SAVED_TRANSLATIONS_DIR"'

    config = {'SAVED_TRANSLATIONS_DIR': '/non-dir/fake-dir'}
    persistence = Persistence(config)
    assert Persistence.err_msg.find("FileStorage failed - [WinError 3] The system cannot find the path specified") > -1

    config = {'SAVED_TRANSLATIONS_DIR': './xyz:\n'}
    persistence = Persistence(config)
    assert persistence.err_msg.find("FileStorage failed - [WinError 267] The directory name is invalid") > -1


def test_obj_attrs():
    persistence = Persistence(CONFIG)
    assert persistence.err_msg is None


def test_save_translation():
    persistence = Persistence(CONFIG)

    user_input = ltrans.model.UserInput('This is', 'English', 'French', 0, 0, 0, 'test 1')
    translated_text = 'Cette est'
    msg = persistence.save_translation(user_input, translated_text)
    assert msg.startswith('Saved translation in:') and msg.endswith('English-French.1.json')

    user_input = ltrans.model.UserInput('This is\na test', 'English', 'French', 0, 0, 0, 'test 2')
    translated_text = 'Cette est\nune tester'
    msg = persistence.save_translation(user_input, translated_text)
    assert msg.endswith('English-French.2.json')

    user_input = ltrans.model.UserInput('This\ntest', 'English', 'French', 0, 1, 0, 'test 3')
    translated_text = 'This\nCette\n\ntest\ntester'
    msg = persistence.save_translation(user_input, translated_text)
    assert msg.endswith('English-French.3.json')


def test_next_and_previous_translation():
    persistence = Persistence(CONFIG)
    translation_1 = {'dest_language': 'French',
                    'is_add_src': 0,
                    'is_add_transliteration': 0,
                    'translate_one_word_at_a_time': 0,
                    'src_language': 'English',
                    'text_lines': 'This is',
                    'translated_text': 'Cette est',
                    'description': 'test 1'}
    translation_2 = {'dest_language': 'French',
                    'is_add_src': 0,
                    'is_add_transliteration': 0,
                    'translate_one_word_at_a_time': 0,
                    'src_language': 'English',
                    'text_lines': 'This is\na test',
                    'translated_text': 'Cette est\nune tester',
                    'description': 'test 2'}
    translation_3 = {'dest_language': 'French',
                    'is_add_src': 0,
                    'is_add_transliteration': 1,
                    'translate_one_word_at_a_time': 0,
                    'src_language': 'English',
                    'text_lines': 'This\ntest',
                    'translated_text': 'This\nCette\n\ntest\ntester',
                    'description': 'test 3'}

    file_path, trans = persistence.next_translation()
    assert file_path.endswith('English-French.3.json')
    assert_dictionaries_equal(trans, translation_3)

    file_path, trans = persistence.previous_translation()
    assert file_path.endswith('English-French.2.json')
    assert_dictionaries_equal(trans, translation_2)

    file_path, trans = persistence.previous_translation()
    assert file_path.endswith('English-French.1.json')
    assert_dictionaries_equal(trans, translation_1)

    file_path, trans = persistence.previous_translation()
    assert file_path.endswith('English-French.1.json')
    assert_dictionaries_equal(trans, translation_1)

    # test next:
    file_path, trans = persistence.next_translation()
    assert file_path.endswith('English-French.2.json')
    assert_dictionaries_equal(trans, translation_2)

    file_path, trans = persistence.next_translation()
    assert file_path.endswith('English-French.3.json')
    assert_dictionaries_equal(trans, translation_3)

    file_path, trans = persistence.next_translation()
    assert file_path.endswith('English-French.3.json')
    assert_dictionaries_equal(trans, translation_3)


def test_delete_translation():
    persistence = Persistence(CONFIG)
    persistence.delete_translation()


def assert_dictionaries_equal(dict1:dict , dict2:dict):
    keys1 = dict1.keys()
    assert len(keys1) == len(dict2.keys())
    for key in keys1:
        assert dict2.get(key) is not None
        assert dict1[key] == dict2[key]