import ltrans
import os
import shutil

CONFIG = {'LOG_DIR': '../../../tmp', 'DICTIONARY_DIR': '../../../tmp'}
try:
    if os.path.isdir('../../../tmp'):
        shutil.rmtree('../../../tmp')
except:
    print('a file in tmp is use - did not remove tmp directory')
ltrans.util.set_logger('DEBUG', CONFIG)

def test_model():
    create_dictionary()
    model = ltrans.model.Model(CONFIG, None)
    text = 'Today is a fine day.\nIs today a fine day?'
    trans_text = model.translate(text, 'English', 'French', False, False)
    assert trans_text == "Aujourd'hui est une bien journée.\nEst Aujourd'hui une bien journée?"

def create_dictionary():
    english_french_dict = ltrans.model.Dictionary(CONFIG, 'English', 'French')
    english_french_dict['Today'] = "Aujourd'hui"
    english_french_dict['is'] = 'est'
    english_french_dict['a'] = 'une'
    english_french_dict['fine'] = 'bien'
    english_french_dict['day'] = 'journée'
    english_french_dict.save()



