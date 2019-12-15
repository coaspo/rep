from ltrans.model import Model
from ltrans.reference import LANGUAGE_NAMES_ABBRS
from ltrans.reference import TRANSLITERATE_LANGUAGE_NAMES
from ltrans.userinput import UserInput
from ltrans.userinput import UserInputError
from ltrans.util import Config
from ltrans.util import set_logger
from ltrans.view import View
import calendar
import datetime
import googletrans
import json
import logging
import ltrans.view
import os
import tkinter
import tkinter.ttk
import traceback

log = logging.getLogger(__name__)


class Controller:
    def __init__(self, config_trans: dict, view: View, model: Model):
        self._config_trans = config_trans
        self.view = view
        self.model = model
        self.delete_bt_click_count = 0

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
        self.view.src_language.set(self.view.language_names[0])
        self.view.destination_language.set(self.view.language_names[1])
        self.view.add_transliteration_check_bt.config(state=tkinter.DISABLED)
        self.view.add_source_check_bt.deselect()
        self.update_status(Config.TRANSLATE_INSTRUCTIONS)

    def update_status(self, text: str, is_err=False):
        self.view.status_label['text'] = text
        background = "#ffeeee" if is_err else "#eeffee"
        self.view.status_label.config(bg=background)

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
        return UserInput(text, src_language, dest_language, is_add_source, is_add_transliteration)

    def update_transliteration(self, _):
        try:
            src_language = self.view.src_language.get()
            dest_language = self.view.destination_language.get()
            if src_language in TRANSLITERATE_LANGUAGE_NAMES or dest_language in TRANSLITERATE_LANGUAGE_NAMES:
                self.view.add_transliteration_check_bt.configure(state=tkinter.NORMAL)
            else:
                self.view.add_transliteration_check_bt.configure(state=tkinter.DISABLED)
                Controller._set_check_button(self.view.add_transliteration_check_bt, 0)
        except Exception as e:
            self._handle_error('', e)

    def save_translation(self, _):
        try:
            user_input = self._get_user_input()
            trans_text = self.view.output_frame.get("1.0", tkinter.END)
            filepath = self.model.persistence.save_translation(user_input, trans_text)
            self.update_status(f'Translation saved in: {filepath}')
        except Exception as e:
            self._handle_error('', e)

    def next_translation(self, _):
        try:
            file_path, translation = self.model.persistence.next_translation()
            info = Controller._file_info(file_path)
            self._populate_screen(info, translation)
        except Exception as e:
            self._handle_error('', e)

    def previous_translation(self, _):
        try:
            file_path, translation = self.model.persistence.previous_translation()
            info = Controller._file_info(file_path)
            self._populate_screen(info, translation)
        except Exception as e:
            self._handle_error('', e)

    def _populate_screen(self, info, translation):
        self.delete_bt_click_count = 0
        self.view.input_frame.delete('1.0', tkinter.END)
        self.view.output_frame.delete('1.0', tkinter.END)
        Controller._set_check_button(self.view.add_transliteration_check_bt, translation['is_add_transliteration'])
        Controller._set_check_button(self.view.add_source_check_bt, translation['is_add_src'])
        self.view.input_frame.insert(tkinter.END, translation['text_lines'])
        self.view.output_frame.insert(tkinter.END, translation['translated_text'])
        self.update_status(info)

    @staticmethod
    def _set_check_button(button: tkinter.Checkbutton, value: int):
        if value == 1:
            button.select()
        else:
            button.deselect()

    @staticmethod
    def _file_info(file_path: str):
        seconds_since_created = os.path.getmtime(file_path)
        create_ts = datetime.datetime.utcfromtimestamp(seconds_since_created).isoformat()[:22]
        # remove T in, for example, create_ts = 2019-12-11T19:20:48.85
        create_ts = create_ts[:10] + ' ' + create_ts[11:]
        day_index = datetime.datetime.utcfromtimestamp(seconds_since_created).weekday()
        info = file_path + ' created at: ' + create_ts + ' ' + calendar.day_name[day_index]
        return info

    def delete_translation(self, _):
        self.delete_bt_click_count += 1
        file_path = self.model.persistence.current_file_path()
        info = Controller._file_info(file_path)
        if self.delete_bt_click_count == 1:
            self.update_status(f'Click Delete button again, to delete file: {info} or \u25BA \u25C4 to cancel')
        else:
            try:
                file_path = self.model.persistence.delete_translation()
                self.update_status(f'Deleted translation file: {info}')
                self.delete_bt_click_count == 0
            except Exception as e:
                self._handle_error('', e)

    def on_closing(self):
        self.model.save_dictionary()
        self.view.stop()

    def bind_view_controls(self):
        self.view.clear_bt.bind("<Button-1>", self.clear_input)
        self.view.src_language.bind("<<ComboboxSelected>>", self.update_transliteration)
        self.view.destination_language.bind("<<ComboboxSelected>>", self.update_transliteration)
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
