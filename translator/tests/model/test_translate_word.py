import googletrans
import ltrans
import os
import shutil

TRANSLATOR = googletrans.Translator()

CONFIG = {'LOG_DIR': '../../../tmp', 'DICTIONARY_DIR': '../../../tmp', 'LOG_LEVEL': 'INFO'}
try:
    if os.path.isdir('../../../tmp'):
        shutil.rmtree('../../../tmp')
except:
    print('a file in tmp is use - did not remove tmp directory')

ltrans.util.set_logger(CONFIG)


def test_new_word():
    dictionary = english_french_dict()
    trans_word = ltrans.model.translate_word('funny', dictionary, TRANSLATOR)
    assert trans_word == 'drôle' or trans_word == 'marrant'


def test_existing_word():
    dictionary = english_french_dict()
    int_len = len(dictionary)
    trans_word = ltrans.model.translate_word('hello', dictionary,TRANSLATOR)
    assert trans_word == 'bonjour'
    assert len(dictionary) == int_len


def test_word_upper_case():
    dictionary = english_french_dict()
    int_len = len(dictionary)
    trans_word = ltrans.model.translate_word('Hello', dictionary,TRANSLATOR)
    assert trans_word == 'Bonjour'
    assert len(dictionary) == int_len


def test_word_w_delimiter():
    dictionary = french_english_dict()
    int_len = len(dictionary)
    trans_word = ltrans.model.translate_word("Aujourd'hui", dictionary,TRANSLATOR)
    assert trans_word == "Today"
    if len(dictionary) == int_len:
        print('words: ', dictionary.words())
    assert len(dictionary) == int_len


def french_english_dict():
    french_english_dict = ltrans.model.Dictionary(CONFIG, 'French', 'English')
    french_english_dict['Aujourd\'hui'] = 'Today'
    french_english_dict['Bonjour'] = 'hello'
    return french_english_dict;


def english_french_dict():
    english_french_dict = ltrans.model.Dictionary(CONFIG, 'English', 'French')
    english_french_dict['Today'] = 'Aujourd\'hui'
    english_french_dict['hello'] = 'bonjour'
    return english_french_dict;
