import ltrans
import os
import shutil

CONFIG = {'LOG_DIR': '../../../tmp', 'DICTIONARY_DIR': '../../../tmp', 'LOG_LEVEL': 'DEBUG'}
try:
    if os.path.isdir('../../../tmp'):
        shutil.rmtree('../../../tmp')
except:
    print('a file in tmp is use - did not remove tmp directory')

ltrans.util.set_logger(CONFIG)


def test_no_new_words():
    dictionary = english_french_dict()
    int_len = len(dictionary)

    trans_line = ltrans.model.translate_line('Today is a fine day.', dictionary,  None)
    assert trans_line == "Aujourd'hui est une bien journée."
    assert len(dictionary) == int_len


def test_w_non_ltrs():
    dictionary = english_french_dict()
    int_len = len(dictionary)

    trans_line = ltrans.model.translate_line('Today, $10 is; a **fine** day.!?', dictionary, None)
    assert trans_line == "Aujourd'hui, $10 est; une **bien** journée.!?"
    assert len(dictionary) == int_len


def english_french_dict():
    english_french_dict = ltrans.model.Dictionary(CONFIG, 'English', 'French')
    english_french_dict['Today'] = 'Aujourd\'hui'
    english_french_dict['is'] = 'est'
    english_french_dict['a'] = 'une'
    english_french_dict['fine'] = 'bien'
    english_french_dict['day'] = 'journée'
    assert len(english_french_dict) == 5
    return english_french_dict;
