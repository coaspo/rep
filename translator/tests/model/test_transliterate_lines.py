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

def test_tranliteration():
    lines = ['Αυτό είναι ένα τεστ', 'Μεταφράστε και μεταγράψτε λέξεις']
    transliterated_lines = ltrans.model.transliterate_lines(lines, 'Greek')
    assert transliterated_lines[0] == 'Auto einai ena test'
    assert transliterated_lines[1] == 'Metafraste kai metagrapste lexeis'


def test_tranliteration_one_line():
    lines = ['шоколад']
    transliterated_lines = ltrans.model.transliterate_lines(lines, 'Russian')
    assert transliterated_lines[0] == 'shokolad'

def test_non_tranliteration():
    lines = ['Good', 'Morning']
    transliterated_lines = ltrans.model.transliterate_lines(lines, 'English')
    assert transliterated_lines is None

