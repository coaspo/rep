import ltrans
import os
import shutil

CONFIG = {'LOG_DIR': '../../../tmp', 'DICTIONARY_DIR': '../../../tmp', 'LOG_LEVEL': 'INFO'}
try:
    if os.path.isdir('../../../tmp'):
        shutil.rmtree('../../../tmp')
except:
    print('a file in tmp is use - did not remove tmp directory')

ltrans.util.set_logger(CONFIG)


def test_add_nothing():
    user_input = ltrans.model.UserInput('...', 'English',  'French', is_add_src=False, is_add_transliteration=False)
    input_lines = ['Good morning', 'goodbye']
    translated_lines = ['Доброе утро', 'Прощайς']
    output_lines = ltrans.model.possibly_add_extra_lines(input_lines, translated_lines, user_input)
    assert input_lines == ['Good morning', 'goodbye']
    assert translated_lines == ['Доброе утро', 'Прощайς']
    assert output_lines == translated_lines
    print('-----', output_lines)


def test_add_source():
    user_input = ltrans.model.UserInput('...', 'English', 'Russian', is_add_src=True, is_add_transliteration=False)
    input_lines = ['Good morning', 'goodbye']
    translated_lines = ['Доброе утро', 'Прощайς']
    output_lines = ltrans.model.possibly_add_extra_lines(input_lines, translated_lines, user_input)
    assert output_lines == ['Good morning\nДоброе утро\n', 'goodbye\nПрощайς\n']


def test_transliterate():
    user_input = ltrans.model.UserInput('...', 'English', 'Russian', is_add_src=False, is_add_transliteration=True)
    input_lines = ['Good morning', 'goodbye']
    translated_lines = ['Доброе утро', 'Прощайς']
    output_lines = ltrans.model.possibly_add_extra_lines(input_lines, translated_lines, user_input)
    assert output_lines == ['Доброе утро\nDobroe utro\n', 'Прощайς\nProschajς\n']


def test_add_source_and_transliterate():
    user_input = ltrans.model.UserInput('...', 'English', 'Russian', is_add_src=True, is_add_transliteration=True)
    input_lines = ['Good', 'goodbye']
    translated_lines = ['Хороший', 'Прощайς']
    output_lines = ltrans.model.possibly_add_extra_lines(input_lines, translated_lines, user_input)
    assert input_lines == ['Good', 'goodbye']
    assert translated_lines == ['Хороший', 'Прощайς']
    assert output_lines == ['Good\nХороший\nHoroshij\n', 'goodbye\nПрощайς\nProschajς\n']
