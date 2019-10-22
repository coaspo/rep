import ltrans
import os

CONFIG = {'LOG_DIR': '../../../tmp', 'DICTIONARY_DIR': '../../../tmp'}
ltrans.util.set_logger('DEBUG', CONFIG)

def test_dict_file_path():
    dict_file_path = '../../../tmp/EnglishKlingon-dict.json'
    if os.path.isfile(dict_file_path):
        os.remove(dict_file_path)
    dicti = ltrans.model.Dictionary(CONFIG, 'Klingon', 'English')
    assert dicti._dict_file_path == dict_file_path
    assert len(dicti) == 0


def test_add_word():
    dicti = ltrans.model.Dictionary(CONFIG, 'Klingon', 'English')
    dicti['wa'] = 'one'
    assert dicti['wa'] == 'one'


def test_save():
    dicti = ltrans.model.Dictionary(CONFIG, 'Klingon', 'English')
    dicti['wa'] = 'one'
    dicti['cha'] = 'two'
    assert dicti.words() == {'wa': 'one', 'cha': 'two'}
    assert len(dicti) == 2
    dicti.save()

    dicti = ltrans.model.Dictionary(CONFIG, 'English', 'Klingon')
    assert dicti._initial_len == 2
    assert len(dicti) == 2
    assert dicti['one'] == 'wa'
    assert dicti['two'] == 'cha'

