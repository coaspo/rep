from ltrans.model import Model
from ltrans.view import View
import googletrans
import json
import langdetect
import logging
import ltrans.reference
import ltrans.util
import os
import tkinter
import tkinter.ttk
import traceback

LOG = logging.getLogger(__name__)


class Controller:
    def __init__(self, config_trans, view, model):
        self._config_trans = config_trans
        self.view = view
        self.model = model
        self.source_lang_keys_typed = ''
        self.destination_lang_keys_typed = ''

    @property
    def config_trans(self):
        return self._config_trans

    def _handle_error(self, msg, exc=None):
        if exc is None:
            LOG.error(msg)
            self.update_status(msg)
        else:
            msg_exc = msg + ' ' + str(exc)
            msg_trace = msg_exc + '\n\t' + traceback.format_exc()
            LOG.error(msg + '\n\t' + msg_trace)
            self.update_status(msg_exc)

    def clear_input(self, _):
        self.view.input_frame.delete('1.0', tkinter.END)
        self.view.output_frame.delete('1.0', tkinter.END)
        self.view.src_language.set('')
        self.view.destination_language.set('')
        self.view.trans_bt.config(state=tkinter.DISABLED)
        self.view.add_transliteration_check_button.config(state=tkinter.DISABLED)
        self.view.add_source_check_button.deselect()
        self.update_status(ltrans.util.Config.TRANSLATE_INSTRUCTIONS)

    def update_status(self, text):
        self.view.status_label.delete(0, tkinter.END)
        self.view.status_label.insert(0, text)

    def find_src_language(self, _):
        self.update_status('Determining source language')
        src_text = self.view.input_frame.get('1.0', tkinter.END).strip()
        if len(src_text) == 0:
            self.update_status('No source text - language not detected')
            return
        try:
            src_lang_abbr = langdetect.detect(src_text)
            src_language = ltrans.reference.LANGUAGE_ABBRS_NAMES.get(src_lang_abbr)
            self.view.src_language.set('')
            if src_language is None:
                self.update_status(src_lang_abbr + " is UNK ABBR, check: language_ABBRs.json")
            else:
                for index, lang_name in enumerate(self.view.language_names):
                    if src_language == lang_name:
                        self.view.src_language.current(index)
                        if src_language in ltrans.reference.TRANSLITERATE_LANGUAGE_NAMES:
                            self.view.add_transliteration_check_button.configure(state=tkinter.NORMAL)
                        break
                self._possibly_recommend_dest_language(src_language)
            self.model.save_dictionary()
            self.update_status('May change source language or click "Translate"')
        except Exception as e:
            self._handle_error('', e)

    def _possibly_recommend_dest_language(self, src_language):
        dest_language = self.view.destination_language.get()
        if len(dest_language) == 0:
            try:
                top_languages = self.config_trans.get('TOP_OF_LIST_LANGUAGES').split(',')
                index = self.view.language_names.index(top_languages[1])
                if src_language == top_languages[1]:
                    index = self.view.language_names.index(top_languages[0])
                self.view.destination_language.current(index)
                dest_language = self.view.destination_language.get()
                if dest_language in ltrans.reference.TRANSLITERATE_LANGUAGE_NAMES:
                    self.view.add_transliteration_check_button.configure(state=tkinter.NORMAL)
                self.view.trans_bt.config(state=tkinter.NORMAL)
            except Exception as e:
                self._handle_error('src_language=' + src_language, e)

    def set_source_language(self, event):
        self.source_lang_keys_typed = \
            self._update_typed_keys(event, self.source_lang_keys_typed, self.view.source_language)

    def set_dest_language(self, event):
        self.destination_lang_keys_typed = \
            self._update_typed_keys(event, self.destination_lang_keys_typed, self.view.destination_language)

    def _update_typed_keys(self, event, keys_typed, combobox):
        try:
            keypress = event.char
            is_not_return_key = not keypress.encode(encoding='UTF-8', errors='strict') == b'\r'
            if is_not_return_key:
                keys_typed += keypress
                keys_typed = keys_typed.title()
            else:
                keys_typed = ''
            for index, lang_name in enumerate(self.view.language_names):
                if lang_name.startswith(keys_typed):
                    combobox.current(index)
                    # if  ltrans.reference.LANGUAGE_ABBRS_NAMES[lang_name] in
                    break
            return keys_typed
        except Exception as e:
            self._handle_error(f' keys_typed= {keys_typed}', e)

    def swap_languages(self, _):
        src_language = self.view.src_language.get()
        dest_language = self.view.destination_language.get()

        for index, lang_name in enumerate(self.view.language_names):
            if lang_name == src_language:
                self.view.destination_language.current(index)
                break

        for index, lang_name in enumerate(self.view.language_names):
            if lang_name == dest_language:
                self.view.src_language.current(index)
                break

        src_text = self.view.input_frame.get("1.0", tkinter.END).strip()
        dest_text = self.view.output_frame.get("1.0", tkinter.END).strip()
        self.view.input_frame.delete('1.0', tkinter.END)
        self.view.output_frame.delete('1.0', tkinter.END)
        self.view.input_frame.insert(tkinter.INSERT, dest_text)
        self.view.output_frame.insert(tkinter.INSERT, src_text)

    def translate_text(self, _):
        if self.view.trans_bt['state'] == 'normal':
            self.view.output_frame.delete('1.0', tkinter.END)
            try:
                user_input = self._get_user_input()
                trans_text = self.model.translate(user_input)
                self.view.output_frame.insert(tkinter.END, trans_text)
                self.update_status(ltrans.util.Config.SAVE_INSTRUCTIONS)
            except Exception as e:
                self._handle_error('', e)

    def _get_user_input(self):
        text = self.view.input_frame.get("1.0", tkinter.END)
        src_language = self.view.src_language.get()
        dest_language = self.view.destination_language.get()
        is_add_source = self.view.is_add_src.get()
        is_add_transliteration = self.view.is_add_transliteration.get()
        return ltrans.model.UserInput(text, src_language, dest_language, is_add_source, is_add_transliteration)

    def phoneticize_and_tranlate(self, _):
        self.view.input_frame.delete('1.0', tkinter.END)
        self.update_status(ltrans.util.Config.TRANSLATE_INSTRUCTIONS)

    def save_translation(self, _):
        user_input = self._get_user_input()
        trans_text = self.view.output_frame.get("1.0", tkinter.END)
        status = self.model.persistence.save_translation(user_input, trans_text)
        self.update_status(status)
        self.view.persistence_status_label.config(text=status)

    def next_translation(self, _):
        count = self.model.persistence.read_next()
        self.view.persistence_status_label.config(text=count)

    def previous_translation(self, _):
        count = self.model.persistence.read_prev()
        self.view.persistence_status_label.config(text=count)

    def delete_translation(self, _):
        status = self.model.persistence.delete_translation()
        self.update_status(status)

    def on_closing(self):
        self.model.save_dictionary()
        self.view.stop()

def language_names(config):
    lang_names = [v for v, _ in ltrans.reference.LANGUAGE_NAMES_ABBRS.items()]
    top_of_list = config.get('TOP_OF_LIST_LANGUAGES').split(',')
    return top_of_list + [x for x in lang_names if x not in top_of_list]


def main():
    try:
        with open(os.path.dirname(__file__) + "/config_trans.json") as f:
            config = json.load(f)
        ltrans.util.set_logger(config)
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug('active....')

        lang_names = language_names(config)
        v = View(lang_names, ltrans.util.Config.TRANSLATE_INSTRUCTIONS)
        google_translator = googletrans.Translator()
        m = Model(config, google_translator)
        c = Controller(config, v, m)
        v.bind_controls(c)
        LOG.info('Starting Translator APP')
        c.view.start()
    except Exception as exc:
        exc_trace = str(exc) + '\n\t' + traceback.format_exc()
        LOG.error(exc_trace)


if __name__ == '__main__':
    main()
