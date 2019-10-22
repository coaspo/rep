import tkinter
import tkinter.ttk
import googletrans
import json
import langdetect
import os
import traceback
import ltrans.reference
from ltrans.model import Model
from ltrans.view import View
import ltrans.util
import logging

log = logging.getLogger(__name__)

class Controller():

    def __init__(self, config_trans, view, model):
        self._config_trans = config_trans
        self.view = view
        self.model = model
        self.keys_typed = ''

    @property
    def config_trans(self):
        return self._config_trans

    def _handle_error(self, msg, exc=None):
        if exc == None:
            log.error(msg)
            self.view.status_label.config(fg='red', text=msg)
        else:
            msg_exc =  msg + ' ' + str(exc)
            msg_trace = msg_exc + '\n\t' + traceback.format_exc()
            log.error(msg + '\n\t' + msg_trace)
            self.view.status_label.config(fg='red', text=msg_exc)

    def clear_input(self, event):
        self.view.input_frame.delete('1.0', tkinter.END)
        self.view.output_frame.delete('1.0', tkinter.END)
        self.view.src_language.set('')
        self.view.destination_language.set('')
        self.view.trans_bt.config(state=tkinter.DISABLED)
        self.view.add_source_check_box.deselect()
        self.view.add_pronunciation_check_box.deselect()
        self.view.status_label.config(fg='black', text='Enter text on left panel')

    def find_src_language(self, event):
        self.view.status_label.config(fg='black', text='Wait ... determining source language')
        src_text = self.view.input_frame.get('1.0', tkinter.END).strip()
        if len(src_text) == 0:
            self.view.status_label.config(fg='red', text='No source text - language not detected')
            return
        try:
            src_lang_abbr = langdetect.detect(src_text)
            src_language = ltrans.reference.LANGUAGE_ABBRS_NAMES.get(src_lang_abbr)
            self.view.src_language.set('')
            if src_language is None:
                self.view.status_label.config(fg='red', text=src_lang_abbr + " is UNK ABBR, check: language_ABBRs.json")
            else:
                for index, lang_name in enumerate(self.view.language_names):
                    if src_language == lang_name:
                        self.view.src_language.current(index)
                        break
                self._possibly_recommend_dest_language(src_language)
            self.view.status_label.config(fg='black', text='Click Translate button')
        except Exception as e:
            self._handle_error('', e)

    def _possibly_recommend_dest_language(self, src_language):
        dest_language = self.view.destination_language.get()
        if len(dest_language) == 0:
            try:
                primary_language = self.config_trans.get('PRIMARY_DESTINATION_LANGUAGE')
                index = self.view.language_names.index(primary_language)
                if src_language == primary_language:
                    index = self.view.language_names.index(self.config_trans.get('SECONDARY_DESTINATION_LANGUAGE'))
                self.view.destination_language.current(index)
                self.view.trans_bt.config(state=tkinter.NORMAL)
            except Exception as e:
                self._handle_error('src_language=' + src_language, e)

    def set_dest_language(self, event):
        try:
            keypress = event.char
            is_not_return_key = not keypress.encode(encoding='UTF-8', errors='strict') == b'\r'
            if is_not_return_key:
                self.keys_typed += keypress
                self.keys_typed = self.keys_typed.title()
            else:
                self.keys_typed = ''
            for index, lang_name in enumerate(self.view.language_names):
                if lang_name.startswith(self.keys_typed):
                    self.view.destination_language.current(index)
                    break
        except Exception as e:
            self._handle_error(' keys_typed= ' + self.keys_typed, e)

    def translate_text(self, event):
        if self.view.trans_bt['state'] == 'normal':
            self.view.output_frame.delete('1.0', tkinter.END)
            try:
                text = self.view.input_frame.get("1.0", tkinter.END)
                src_language = self.view.src_language.get()
                dest_language = self.view.destination_language.get()
                is_add_source = self.view.is_add_src.get()
                is_add_pronunciation = self.view.is_add_pronunciation.get()
                trans_text = self.model.translate(text, src_language, dest_language, is_add_source,
                                                  is_add_pronunciation)
                self.view.output_frame.insert(tkinter.END, trans_text)
                self.view.status_label.config(fg='green', text='translation done')
            except Exception as e:
                self._handle_error('', e)

    def phoneticize_and_tranlate(self, event):
        self.view.input_frame.delete('1.0', tkinter.END)
        self.view.status_label.config(text='Enter text on left panel')

    def txt_frame_key_press(self, event):
        kp = repr(event.char)
        print("pressed", kp)  # repr(event.char))

    def on_closing(self):
        self.model.save_dictionary()
        self.view.stop()


def main():
    print('wd=====', os.getcwd())
    print('filepath======', os.path.abspath(os.path.dirname(__file__)))
    try:
        with open(os.path.dirname(__file__) + "/config_trans.json") as f:
            config = json.load(f)
        ltrans.util.set_logger("DEBUG", config)
        if __debug__:
            log.debug('acive....')
        language_names = [v for v, _ in ltrans.reference.LANGUAGE_NAMES_ABBRS.items()]
        v = View(language_names)
        google_translator = googletrans.Translator()
        m = Model(config, google_translator)
        c = Controller(config, v, m)
        v.bind_controls(c, m)
        log.info('Starting Tranlator APP')
        c.view.start()
    except Exception as exc:
        exc_trace = str(exc) + '\n\t' + traceback.format_exc()
        log.error(exc_trace)


if __name__ == '__main__':
    main()
