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


def test_multiple_lines():
    text_lines = 'Today is a fine day.\nIs today a fine day?'
    user_input = ltrans.model.UserInput(text_lines, 'English',  'French', is_add_src=False, is_add_transliteration=False)
    dictionary = english_french_dict()
    trans_text = ltrans.model.translate_text(user_input, dictionary, translator=None)
    assert trans_text == "Aujourd'hui est une bien journée.\nEst Aujourd'hui une bien journée?"

def test_empty_lines():
    text_lines = 'Today\n\nfine'
    user_input = ltrans.model.UserInput(text_lines, 'English',  'French', is_add_src=False, is_add_transliteration=False)
    dictionary = english_french_dict()
    trans_text = ltrans.model.translate_text(user_input, dictionary, translator=None)
    assert trans_text == "Aujourd'hui\nbien?"


def english_french_dict():
    english_french_dict = ltrans.model.Dictionary(CONFIG, 'English', 'French')
    english_french_dict['Today'] = "Aujourd'hui"
    english_french_dict['is'] = 'est'
    english_french_dict['a'] = 'une'
    english_french_dict['fine'] = 'bien'
    english_french_dict['day'] = 'journée'
    assert len(english_french_dict) == 5
    return english_french_dict
