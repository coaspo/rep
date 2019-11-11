import ltrans.controller
import ltrans.model
import ltrans.reference
import ltrans.util
import ltrans.view
# use this file to test code
CONFIG = {'LOG_DIR': 'tmp', 'LOG_LEVEL': 'DEBUG', 'SAVED_TRANSLATIONS_DIR': 'tmp'}
try:
    if os.path.isdir('tmp'):
        shutil.rmtree('tmp')
except:
    print('a file in tmp is use - did not remove tmp directory')
ltrans.util.set_logger(CONFIG)


def test_set_dir():
    savedTranslations = ltrans.model.SavedTranslations(CONFIG)
    print (savedTranslations._save_dir)
    a = ['a.3.e', 'a.2.e', 'a.x.e']
    v = [x.split('.')[1] for x in a if x.split('.')[1].isnumeric()]
    print('-----'+str(123))

#     assert(savedTranslations._save_dir =='../../../tmp')
#     assert(os.path.isdir('../../../tmp'))
#
# def test_write():
#     savedTranslations = ltrans.model.SavedTranslations(CONFIG)
#     user_input = ltrans.model.UserInput('This is\na test', 'English', 'French', 0, 1)
#     translated_text = 'This is\nCette est\n\na test\nune tester'
#     savedTranslations.write(user_input, translated_text)