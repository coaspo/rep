import quz
import tests.t_util

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)
CONFIG = {'LOG_DIR': TMP_DIR, 'DICTIONARY_DIR': TMP_DIR, 'LOG_LEVEL': 'INFO'}
quz.util.set_logger(CONFIG)


def test_model():
    create_dictionary()
    model = quz.model.Model(CONFIG, None, None)
    user_input = quz.model.UserInput(text_lines='Today is a fine day.\nIs today a fine day?',
                                     src_language='English',
                                     dest_language='French',
                                     is_add_src=False,
                                     is_add_transliteration=False)
    trans_text = model.create_quiz(user_input)
    assert trans_text == "Aujourd'hui est une bien journée.\nEst Aujourd'hui une bien journée?"


def create_dictionary():
    english_french_dict = quz.model.Dictionary(CONFIG, 'English', 'French')
    english_french_dict['Today'] = "Aujourd'hui"
    english_french_dict['is'] = 'est'
    english_french_dict['a'] = 'une'
    english_french_dict['fine'] = 'bien'
    english_french_dict['day'] = 'journée'
    english_french_dict.save()
