import quz
import quz.model
import tests.t_util
from quz.persistence import Persistence

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'SAVED_QUIZES_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
QUESTION1_ANSWERS = {'answer1': {'is_correct': False,
                                 'is_selected': False,
                                 'answer': 'is 4'},
                     'answer2': {'is_correct': True,
                                 'is_selected': False,
                                 'answer': 'is 5'},
                     'comment': 'addition',
                     'num_of_answers': 2}
QUESTION2_ANSWERS = {'answer1': {'is_correct': False,
                                 'is_selected': False,
                                 'answer': ' = 1'},
                     'answer2': {'is_correct': True,
                                 'is_selected': False,
                                 'answer': ' = 2'},
                     'answer3': {'is_correct': False,
                                 'is_selected': False,
                                 'answer': ' = 4'},
                     'num_of_answers': 3}
QUIZ = {'latest_question_num': 1,
        'num_of_completed_questions': 0,
        'num_of_questions': 2,
        'question1': 'What is 2+3',
        'question1_answers': QUESTION1_ANSWERS,
        'question2': '1*2 = ?',
        'question2_answers': QUESTION2_ANSWERS}
quz.util.set_logger(CONFIG)


def test_invalid_directories():
    config = {}
    persistence = Persistence(config)
    assert Persistence.file_storage_err_msg == 'FileStorage failed - config missing parameter "SAVED_QUIZES_DIR"'

    config = {'SAVED_QUIZES_DIR': '/non-dir/fake-dir'}
    persistence = Persistence(config)
    assert Persistence.file_storage_err_msg.find(
        "FileStorage failed - [WinError 3] The system cannot find the path specified") > -1

    config = {'SAVED_QUIZES_DIR': './xyz:\n'}
    persistence = Persistence(config)
    assert persistence.file_storage_err_msg.find(
        "FileStorage failed - [WinError 267] The directory name is invalid") > -1


def test_obj_attrs():
    persistence = Persistence(CONFIG)
    assert persistence.file_storage_err_msg is None


def test_save():
    persistence = Persistence(CONFIG)

    quiz = {'fake..ques..': 'fake--answer...'}
    quiz = {'ques...': 'What is..'}
    print('+=======+\n', quiz)

    msg = persistence.save(quiz)
    print('+=======+\n',msg)
    # assert msg.startswith('Saved translation in:') and msg.endswith('English-French.1.json')
    #
    # user_input = quz.model.UserInput('This is\na test', 'English', 'French', 0, 0)
    # translated_text = 'Cette est\nune tester'
    # msg = persistence.save_quiz(user_input, translated_text)
    # assert msg.endswith('English-French.2.json')
    #
    # user_input = quz.model.UserInput('This\ntest', 'English', 'French', 0, 1)
    # translated_text = 'This\nCette\n\ntest\ntester'
    # msg = persistence.save_quiz(user_input, translated_text)
    # assert msg.endswith('English-French.3.json')


def test_get_next_and_get_previous():
    persistence = Persistence(CONFIG)
    translation_1 = {'dest_language': 'French',
                     'is_add_src': 0,
                     'is_add_transliteration': 0,
                     'src_language': 'English',
                     'text_lines': 'This is',
                     'translated_text': 'Cette est'}
    translation_2 = {'dest_language': 'French',
                     'is_add_src': 0,
                     'is_add_transliteration': 0,
                     'src_language': 'English',
                     'text_lines': 'This is\na test',
                     'translated_text': 'Cette est\nune tester'}
    translation_3 = {'dest_language': 'French',
                     'is_add_src': 0,
                     'is_add_transliteration': 1,
                     'src_language': 'English',
                     'text_lines': 'This\ntest',
                     'translated_text': 'This\nCette\n\ntest\ntester'}

    file_path, msg, quiz = persistence.get_next()
    assert file_path.endswith('English-French.3.json')
    assert_dictionaries_equal(quiz, translation_3)

    file_path, msg, quiz = persistence.get_previous()
    assert file_path.endswith('English-French.2.json')
    assert_dictionaries_equal(quiz, translation_2)

    file_path, msg, quiz = persistence.get_previous()
    assert file_path.endswith('English-French.1.json')
    assert_dictionaries_equal(quiz, translation_1)

    file_path, msg, quiz = persistence.get_previous()
    assert file_path.endswith('English-French.1.json')
    assert_dictionaries_equal(quiz, translation_1)

    # test next:
    file_path, msg, quiz = persistence.get_next()
    assert file_path.endswith('English-French.2.json')
    assert_dictionaries_equal(quiz, translation_2)

    file_path, msg, quiz = persistence.get_next()
    assert file_path.endswith('English-French.3.json')
    assert_dictionaries_equal(quiz, translation_3)

    file_path, msg, quiz = persistence.get_next()
    assert file_path.endswith('English-French.3.json')
    assert_dictionaries_equal(quiz, translation_3)

    user_input = quz.model.UserInput('One', 'Italian', 'Dutch', 0, 1)
    translated_text = 'Cette 123'
    persistence.update(user_input, translated_text)
    file_path, msg, trans2 = persistence.get_next()
    assert file_path.endswith('English-French.3.json')
    assert trans2['translated_text'] == 'Cette 123'
    assert trans2['dest_language'] == 'Dutch'
    assert trans2['text_lines'] == 'One'


def test_delete():
    persistence = Persistence(CONFIG)
    persistence.delete()


def assert_dictionaries_equal(dict1: dict, dict2: dict):
    keys1 = dict1.keys()
    assert len(keys1) == len(dict2.keys())
    for key in keys1:
        assert dict2.get(key) is not None
        assert dict1[key] == dict2[key]
