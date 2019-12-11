from ltrans.model import Model
from ltrans.reference import LANGUAGE_ABBRS_NAMES
from ltrans.reference import LANGUAGE_NAMES_ABBRS
from ltrans.reference import TRANSLITERATE_LANGUAGE_NAMES
from ltrans.userinput import UserInput
from ltrans.util import Config
from ltrans.util import set_logger
from ltrans.view import View
import googletrans
import json
import langdetect
import logging
import ltrans.view
import os
import tkinter
import tkinter.ttk
import traceback

log = logging.getLogger(__name__)


class UserInputError(Exception):
    pass


class Controller:
    def __init__(self, config_trans: dict, view: View, model: Model):
        self._config_trans = config_trans
        self.view = view
        self.model = model
        self.source_lang_keys_typed = ''
        self.destination_lang_keys_typed = ''

    @property
    def config_trans(self):
        return self._config_trans

    def _handle_error(self, msg: str, exc=None):
        if exc is None:
            log.error(msg)
            self.update_status(msg, True)
        else:
            msg_exc = msg + ' ' + str(exc)
            msg_trace = msg_exc + '\n\t' + traceback.format_exc()
            if type(exc) is not UserInputError:
                log.error(msg + '\n\t' + msg_trace)
            self.update_status(msg_exc, True)

    def clear_input(self, event: tkinter.Event):
        self.view.input_frame.delete('1.0', tkinter.END)
        self.view.output_frame.delete('1.0', tkinter.END)
        self.view.src_language.set('')
        self.view.destination_language.set('')
        self.view.trans_bt.config(state=tkinter.DISABLED)
        self.view.add_transliteration_check_button.config(state=tkinter.DISABLED)
        self.view.add_source_check_button.deselect()
        self.update_status(Config.TRANSLATE_INSTRUCTIONS)

    def update_status(self, text: str, is_err=False):
        self.view.status_or_description_entry.delete(0, tkinter.END)
        self.view.status_or_description_entry.insert(0, text)
        background = "#ffeeee" if is_err else "#eeffee"
        self.view.status_or_description_entry.config(bg=background)

    def find_src_language(self, _):
        self.update_status('Determining source language')
        src_text = self.view.input_frame.get('1.0', tkinter.END).strip()
        if len(src_text) == 0:
            self.update_status('No source text - language not detected')
            return
        try:
            src_lang_abbr = langdetect.detect(src_text)
            src_language = LANGUAGE_ABBRS_NAMES.get(src_lang_abbr)
            self.view.src_language.set('')
            if src_language is None:
                self.update_status(src_lang_abbr + " is UNK ABBR, check: language_ABBRs.json")
            else:
                for index, lang_name in enumerate(self.view.language_names):
                    if src_language == lang_name:
                        self.view.src_language.current(index)
                        if src_language in TRANSLITERATE_LANGUAGE_NAMES:
                            self.view.add_transliteration_check_button.configure(state=tkinter.NORMAL)
                        break
                self._possibly_recommend_dest_language(src_language)
            self.model.save_dictionary()
            self.update_status(Config.SAVE_INSTRUCTIONS)
        except Exception as e:
            self._handle_error('', e)

    def _possibly_recommend_dest_language(self, src_language: str):
        dest_language = self.view.destination_language.get()
        if len(dest_language) == 0:
            try:
                top_languages = self.config_trans.get('TOP_OF_LIST_LANGUAGES').split(',')
                index = self.view.language_names.index(top_languages[1])
                if src_language == top_languages[1]:
                    index = self.view.language_names.index(top_languages[0])
                self.view.destination_language.current(index)
                dest_language = self.view.destination_language.get()
                if dest_language in TRANSLITERATE_LANGUAGE_NAMES:
                    self.view.add_transliteration_check_button.configure(state=tkinter.NORMAL)
                self.view.trans_bt.config(state=tkinter.NORMAL)
            except Exception as e:
                self._handle_error('src_language=' + src_language, e)

    def set_source_language(self, event: tkinter.Event):
        print ('$$$$',type(event))
        self.source_lang_keys_typed = \
            self._update_typed_keys(event, self.source_lang_keys_typed, self.view.source_language)

    def set_dest_language(self, event: tkinter.Event):
        self.destination_lang_keys_typed = \
            self._update_typed_keys(event, self.destination_lang_keys_typed, self.view.destination_language)

    def _update_typed_keys(self, event: tkinter.Event, keys_typed: str, combobox: tkinter.ttk.Combobox) -> str:
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
                    # if  LANGUAGE_ABBRS_NAMES[lang_name] in
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
        try:
            user_input = self._get_user_input()
            self.view.output_frame.delete('1.0', tkinter.END)
            trans_text = self.model.translate(user_input)
            self.view.output_frame.insert(tkinter.END, trans_text)
            self.update_status(Config.SAVE_INSTRUCTIONS)
            self.view.save_bt.config(state='normal')
        except Exception as e:
            self._handle_error('', e)

    def _get_user_input(self) -> UserInput:
        text = self.view.input_frame.get("1.0", tkinter.END)
        if text.strip() == '':
            raise UserInputError('Source text not entered')
        src_language = self.view.src_language.get()
        dest_language = self.view.destination_language.get()
        is_add_source = self.view.is_add_src.get()
        is_add_transliteration = self.view.is_add_transliteration.get()
        if Config.SAVE_INSTRUCTIONS == Config.SAVE_INSTRUCTIONS:
            description = ''
        else:
            description = self.update_status.get()
        return UserInput(text, src_language, dest_language, is_add_source, is_add_transliteration, description)

    def phoneticize_and_tranlate(self, _):
        self.view.input_frame.delete('1.0', tkinter.END)
        self.update_status(Config.TRANSLATE_INSTRUCTIONS)

    def save_translation(self, _):
        user_input = self._get_user_input()
        trans_text = self.view.output_frame.get("1.0", tkinter.END)
        filepath = self.model.persistence.save_translation(user_input, trans_text)
        self.update_status(f'Translation saved in: {filepath}')

    def next_translation(self, _):
        filepath, translation = self.model.persistence.next_translation()
        self._pouplate_screen(translation)
        self.update_status(text=filepath)

    def previous_translation(self, _):
        filepath, translation = self.model.persistence.previous_translation()
        self._pouplate_screen(translation)
        self.update_status(text=filepath)

    def _pouplate_screen(self, translation):
        print('---------', translation)

    def delete_translation(self, _):
        filepath = self.model.persistence.delete_translation()
        self.update_status(f'Deleted translation file: {filepath}')

    def on_closing(self):
        self.model.save_dictionary()
        self.view.stop()

    def bind_view_controls(self):
        self.view.clear_bt.bind("<Button-1>", self.clear_input)
        self.view.destination_language.bind("<KeyRelease>", self.set_dest_language)
        self.view.trans_bt.bind("<Button-1>", self.translate_text)
        self.view.swap_languages_bt.bind("<Button-1>", self.swap_languages)

        self.view.save_bt.bind("<Button-1>", self.save_translation)
        self.view.next_bt.bind("<Button-1>", self.next_translation)
        self.view.previous_bt.bind("<Button-1>", self.previous_translation)
        self.view.delete_bt.bind("<Button-1>", self.delete_translation)

        self.view.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        if log.isEnabledFor(logging.DEBUG):
            log.debug('controller methods bound to view widgets')


def language_names(config: dict) -> list:
    lang_names = [v for v, _ in LANGUAGE_NAMES_ABBRS.items()]
    top_of_list = config.get('TOP_OF_LIST_LANGUAGES').split(',')
    return top_of_list + [x for x in lang_names if x not in top_of_list]


def main():
    try:
        with open(os.path.dirname(__file__) + "/config_trans.json") as f:
            config = json.load(f)
        set_logger(config)
        if log.isEnabledFor(logging.DEBUG):
            log.info(f'Transliterate languages: {TRANSLITERATE_LANGUAGE_NAMES}')

        lang_names = language_names(config)
        v = ltrans.view.View(lang_names, Config.TRANSLATE_INSTRUCTIONS)
        google_translator = googletrans.Translator()
        m = Model(config, google_translator)
        c = Controller(config, v, m)
        c.bind_view_controls()
        log.info('>>> Starting view')
        c.view.start()
    except Exception as exc:
        exc_trace = str(exc) + '\n\t' + traceback.format_exc()
        log.error(exc_trace)


if __name__ == '__main__':
    main()
