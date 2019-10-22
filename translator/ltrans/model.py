import json
import unicodedata
import re
import ltrans.reference
import os.path
import logging
import ltrans.util

LOG = logging.getLogger(__name__)


class Model:
    def __init__(self, config, google_translator):
        self._dictionary = None
        self._config = config
        self._translator = google_translator

    def translate(self, text, src_language, dest_language, is_add_source, is_add_pronunciation):
        if self._dictionary is None or src_language != self._dictionary.src_language or dest_language != self._dictionary.dest_language:
            self._dictionary = Dictionary(self._config, src_language, dest_language)
        user_input = UserInput(text, src_language, dest_language, is_add_source)
        if __debug__:
            LOG.debug(user_input)
        translated_text = translate_text(user_input, self._dictionary, self._translator)
        return translated_text

    def save_dictionary(self):
        if self._dictionary is not None:
            self._dictionary.save()


class UserInput:
    def __init__(self, text_lines, src_language, dest_language, is_add_src):
        self._text_lines = text_lines
        self._src_language = src_language
        self._dest_language = dest_language
        self._is_add_src = is_add_src

    @property
    def text_lines(self):
        return self._text_lines

    @property
    def dest_language(self):
        return self._dest_language

    @property
    def src_language(self):
        return self._src_language

    @property
    def is_add_src(self):
        return self._is_add_src

    def __repr__(self):
        return f'{self.__class__.__name__}: src_language={self._src_language}, dest_language={self._dest_language}, is_add_src={self._is_add_src}, \ntext_lines=\n {self._text_lines}'


def translate_text(user_input, dictionary, translator):
    if __debug__:
        LOG.debug(f'user_input={user_input}, dictionary={str(dictionary)}')
    input_lines = user_input.text_lines.split('\n')
    translated_lines = [translate_line(line, dictionary, translator) for line in input_lines]

    trans_text = '\n'.join(translated_lines)
    if __debug__:
        LOG.debug(f'trans_text={trans_text}')
    return trans_text


def translate_line(line, dictionary, translator):
    if __debug__:
        LOG.debug(f'  line={line}, translator={str(translator)}')
    line_w_lrs_and_spaces = re.sub(ltrans.util.non_ltrs_regex, '', line.rstrip())
    words = line_w_lrs_and_spaces.split()
    words = [x for x in words if len(x) > 0]
    trans_line = re.sub("'([^ ]+)", r'\1', line)
    new_translated_words = None
    for word in words:
        translated_word = translate_word(word, dictionary, translator)
        trans_display = translated_word
        if word[0:1].isupper():
            trans_display = trans_display[0:1].upper() + trans_display[1:]
        trans_line = re.sub(word, trans_display, trans_line, 1)
    if __debug__:
        LOG.debug(f'   trans_line={trans_line}')
    return trans_line


def translate_word(word, dictionary, translator):
    if __debug__:
        LOG.debug(
            f'    word={word}, src_language={dictionary.src_language}, dest_language={dictionary.dest_language}, translator={str(translator)}')
    no_accent_word = strip_accents(word)
    translated_word = dictionary.get(no_accent_word)
    if translated_word is None:
        translated_word = dictionary.get(no_accent_word[0:1].upper() + no_accent_word[1:])
    if translated_word is None:
        translated_word = dictionary.get(no_accent_word[0:1].lower() + no_accent_word[1:])
    if translated_word is None:
        is_new_word = True
        src_language_abbr = ltrans.reference.LANGUAGE_NAMES_ABBRS[dictionary.src_language]
        dest_language_abbr = ltrans.reference.LANGUAGE_NAMES_ABBRS[dictionary.dest_language]
        translation = translator.translate(word, src=src_language_abbr, dest=dest_language_abbr)
        if __debug__:
            LOG.debug(f'      translation={translation}')
        translated_word = translation.text
        if word != translated_word:
            dictionary[word] = translated_word
        # translation.pronunciation is always none , need google account?
        # if pronunciation is None and dest_language_abbr in transliterate.get_available_language_codes():
        #     pronunciation = transliterate.translit(translated_word, dest_language_abbr, reversed=True)
    if __debug__:
        LOG.debug(f'     translated_word={translated_word}')
    if word[0:1].isupper():
        translated_word = translated_word[0:1].upper() + translated_word[1:]
    return translated_word


def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')


class Dictionary(dict):
    def __init__(self, config, src_language, dest_language):
        self._src_language = src_language
        self._dest_language = dest_language
        langs = [src_language, dest_language]
        langs.sort()
        self._is_reversed = langs[0] != src_language
        self._set_file_path(config, src_language, dest_language)

        if os.path.isfile(self._dict_file_path):
            with open(self._dict_file_path, "r", encoding='utf8') as f:
                dictionary = json.load(f)
            if self._is_reversed:
                reverse_dictionary = {v: k for k, v in dictionary.items()}
                super(Dictionary, self).__init__(reverse_dictionary)
            else:
                super(Dictionary, self).__init__(dictionary)
        else:
            super(Dictionary, self).__init__({})

        self._initial_len = len(self)

    def _set_file_path(self, config, src_language, dest_language):
        if config == None or config.get('DICTIONARY_DIR') == None:
            raise Exception('config missing config parameter "DICTIONARY_DIR"')
        dict_dir = config['DICTIONARY_DIR']

        if dict_dir.startswith("./"):
            dict_dir = os.path.dirname(__file__) + dict_dir[1:]
            print('---', dict_dir)
            if not os.path.exists(dict_dir):
                os.mkdir(dict_dir, 0o755);
        elif not os.path.isdir(dict_dir):
            raise Exception(f'config parameter DICTIONARY_DIR={dict_dir} is and invalid directory')
        langs = [src_language, dest_language]
        langs.sort()
        self._dict_file_path = dict_dir + '/' + langs[0] + langs[1] + '-dict.json'
        if __debug__:
            LOG.debug(f'dict_file_path={self._dict_file_path}')

    @property
    def src_language(self):
        return self._src_language

    @property
    def dest_language(self):
        return self._dest_language

    def is_Source_Target(self, src_language, dest_language):
        return self._src_language == src_language and \
               self._dest_language == dest_language

    def words(self):
        return {k: v for k, v in self.items()}

    def save(self):
        len_diff = len(self) - self._initial_len
        if len_diff > 0:
            dict_save = self.copy()
            if self._is_reversed:
                dict_save = {v: k for k, v in dict_save.items()}

            with open(self._dict_file_path, "w", encoding='utf8') as f:
                json.dump(dict_save, f, ensure_ascii=False, sort_keys=True, indent=0)
            if __debug__:
                LOG.debug('4 sample words saved:', {k: dict_save[k] for k in list(dict_save)[:4]})

    def __repr__(self):
        return f' src_languaget={self._src_language} dest_language={self._dest_language} is_reversed={self._is_reversed}'
