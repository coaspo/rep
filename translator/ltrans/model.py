import json
import unicodedata
import re
import ltrans.reference
import os.path
import logging
import ltrans.util
import transliterate
import random

LOG = logging.getLogger(__name__)


class Model:
    def __init__(self, config, google_translator):
        self._dictionary = None
        self._config = config
        self._translator = google_translator

    def translate(self, text, src_language, dest_language, is_add_source, is_add_transliteration):
        if self._dictionary is None or src_language != self._dictionary.src_language or dest_language != self._dictionary.dest_language:
            self._dictionary = Dictionary(self._config, src_language, dest_language)
        user_input = UserInput(text, src_language, dest_language, is_add_source, is_add_transliteration)
        if __debug__:
            LOG.debug(user_input)
        translated_text = translate_text(user_input, self._dictionary, self._translator)
        return translated_text

    def save_dictionary(self):
        if self._dictionary is not None:
            self._dictionary.save()


class UserInput:
    def __init__(self, text_lines, src_language, dest_language, is_add_src, is_add_transliteration):
        self._text_lines = text_lines
        self._src_language = src_language
        self._dest_language = dest_language
        self._is_add_src = is_add_src
        self._is_add_transliteration = is_add_transliteration

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

    @property
    def is_add_transliteration(self):
        return self._is_add_transliteration


def translate_text(user_input, dictionary, translator):
    if __debug__:
        LOG.debug(f'user_input={user_input}, dictionary={str(dictionary)}')
    input_lines = user_input.text_lines.split('\n')
    translated_lines = [translate_line(line, dictionary, translator) for line in input_lines]
    translated_lines = possibly_add_extra_lines(input_lines, translated_lines, user_input)
    trans_text = '\n'.join(translated_lines).strip()
    if __debug__:
        LOG.debug(f'trans_text={trans_text}')
    return trans_text

def possibly_add_extra_lines(input_lines, translated_lines, user_input):
    output_lines = None
    if user_input.is_add_src:
        output_lines = input_lines.copy()
        if user_input.is_add_transliteration:
            trasliteration_lines = transliterate_lines(input_lines, user_input.src_language)
            if trasliteration_lines is not None:
                output_lines = [a + '\n' + b for a, b in zip(output_lines, trasliteration_lines)]

    if output_lines is None:
        output_lines = translated_lines
    else:
        output_lines = [a + '\n' + b for a, b in zip(output_lines, translated_lines)]

    if user_input.is_add_transliteration:
        trasliteration_lines = transliterate_lines(translated_lines, user_input.dest_language)
        if trasliteration_lines is not None:
            output_lines = [a + '\n' + b for a, b in zip(output_lines, trasliteration_lines)]

    if output_lines != translated_lines:
        output_lines = [line + '\n' for line  in output_lines]
    return output_lines



def transliterate_lines(lines, lines_language):
    if __debug__:
        LOG.debug(f'  lines_language={lines_language}')
    if lines_language == 'English' or lines_language not in ltrans.reference.TRANSLITERATE_LANGUAGE_NAMES:
        return
    lang_abbr = ltrans.reference.LANGUAGE_NAMES_ABBRS[lines_language]
    return [transliterate.translit(line, lang_abbr, reversed=True) for line in lines]


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
        trans_line = re.sub(word, translated_word, trans_line, 1)
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
        # translation.transliteration is always none , need google account?
    if word[0:1].isupper():
        print(translated_word[0:1],'----', translated_word[1:])
        w = translated_word[0:1].upper() + translated_word[1:]
        translated_word = w  # to avoid repeating firstr ltr (?)
    print('----', translated_word)
    if __debug__:
        LOG.debug(f'     translated_word={translated_word}')
    return translated_word


def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')


class Dictionary(dict):
    def __init__(self, config, src_language, dest_language):
        self._src_language = src_language
        self._dest_language = dest_language
        self._set_file_path(config, src_language, dest_language)

        if os.path.isfile(self._dict_file_path):
            with open(self._dict_file_path, "r", encoding='utf8') as f:
                dictionary = json.load(f)
        else:
            dictionary = {}
        super(Dictionary, self).__init__(dictionary)

        self._initial_len = len(self.keys())

    def _set_file_path(self, config, src_language, dest_language):
        if config == None or config.get('DICTIONARY_DIR') == None:
            raise Exception('config missing config parameter "DICTIONARY_DIR"')
        dictionary_dir = config['DICTIONARY_DIR']

        if dictionary_dir.startswith("./"):
            dictionary_dir = os.path.dirname(__file__) + dictionary_dir[1:]
            if not os.path.exists(dictionary_dir):
                os.mkdir(dictionary_dir, 0o755);
        elif not os.path.isdir(dictionary_dir):
            raise Exception(f'config parameter DICTIONARY_DIR={dictionary_dir} is and invalid directory')
        self._dict_file_path = dictionary_dir + '/' + src_language + dest_language+ '-dict.json'
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
        current_len = len(self.keys())
        len_diff = current_len - self._initial_len
        if len_diff > 0:
            with open(self._dict_file_path, "w", encoding='utf8') as f:
                json.dump(self, f, ensure_ascii=False, sort_keys=True, indent=0)
            if __debug__:
                sample_words = random.sample(self.items(), 2)
                LOG.debug(f'initial/current word count: {self._initial_len}/{current_len}  2-word random sample: {sample_words}')
            self._initial_len = len(self.keys())

