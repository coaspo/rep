import tests.t_util
from ltrans.view import _create_html_page
from ltrans.userinput import UserInput

TMP_DIR = tests.t_util.recreate_tmp_dir(__file__)


def test_create_html_page():
    user_input = UserInput('This is', 'English', 'French', 0, 0, 0, 'test 1')
    translation = {'dest_language': 'French',
                     'is_add_src': 0,
                     'is_add_transliteration': 0,
                     'translate_one_word_at_a_time': 0,
                     'src_language': 'English',
                     'text_lines': 'This is',
                     'translated_text': 'Cette est',
                     'description': 'test 1'}
    html = _create_html_page(user_input, translation)
    print ('$$\n$$\n', html)