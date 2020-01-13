from quz.model import Model
from quz.persistence import FilePersistence
from quz.quiz import QuizDataError, Quiz
from quz.util import Config, set_logger
from quz.view import View
import json
import logging
import os
import tkinter
import tkinter.ttk
import traceback

log = logging.getLogger(__name__)


class Controller:
    def __init__(self, view: View, model: Model):
        self.delete_bt_click_count = 0
        self.view = view
        self.model = model
        self.delete_bt_click_count = 0

    def update_status(self, text: str, is_err=False):
        self.view.status_label['text'] = text
        background = "#ffeeee" if is_err else "#eeffee"
        self.view.status_label.config(bg=background)

    def clear_screen(self, _):
        self.delete_bt_click_count = 0
        self.update_status(Config.APP_INSTRUCTIONS)
        self.view.delete_bt.config(state=tkinter.DISABLED)
        self.view.update_bt.config(state=tkinter.DISABLED)
        self.view.input_frame.delete('1.0', tkinter.END)
        # self.view.output_frame.delete('1.0', tkinter.END)
        self.view.persistence_status['text'] = ''

    def handle_exception(self, msg: str, exc=None):
        if exc is None:
            log.error(msg)
            self.update_status(msg, True)
        else:
            msg_exc = msg + ' ' + str(exc)
            msg_trace = msg_exc + '\n\t' + traceback.format_exc()
            if type(exc) is not QuizDataError:
                log.error(msg + '\n\t' + msg_trace)
            self.update_status(msg_exc, True)

    @staticmethod
    def set_check_button(button: tkinter.Checkbutton, value: int):
        if value == 1:
            button.select()
        else:
            button.deselect()


class QuizController(Controller):

    def _save_quiz(self, _):
        if self.view.save_bt['state'] == tkinter.DISABLED:
            return
        try:
            # self.view.output_frame.delete('1.0', tkinter.END)
            text = self.view.input_frame.get("1.0", tkinter.END)
            status_msg = self.model.save_quiz(text)
            super().update_status(status_msg)
        except Exception as e:
            self.handle_exception('Save error: ', e)

    def _on_closing(self):
        # text = self.view.input_frame.get("1.0", tkinter.END)
        # self.model.save_quiz(text)
        self.view.stop()

    def bind_quiz_controls(self):
        self.view.clear_bt.bind("<Button-1>", super().clear_screen)
        self.view.save_bt.bind("<Button-1>", self._save_quiz)
        self.view.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        if log.isEnabledFor(logging.DEBUG):
            log.debug('controller methods bound to view widgets')


class PersistenceController(Controller):
    def _handle_persistence_error(self, e):
        self.handle_exception('AbstractPersistence error: ', e)
        self.view.persistence_status['text'] = 'See error below or in log file'

    def _populate_all_widgets(self, status_msg: str, persistence_msg: str, quiz: Quiz):
        self.view.input_frame.delete('1.0', tkinter.END)
        # self.view.save_bt.config(state=tkinter.DISABLED)
        self.view.input_frame.insert(tkinter.END, quiz.marked_user_input())
        status_msg = status_msg + ';  may change text and click Update, or click Delete'
        super().update_status(status_msg)

        self.delete_bt_click_count = 0
        self.view.persistence_status['text'] = persistence_msg
        self.view.delete_bt.config(state=tkinter.NORMAL)
        self.view.update_bt.config(state=tkinter.NORMAL)

    def _next_quiz(self, _):
        try:
            status_msg, persistence_msg, quiz = self.model.next_quiz()
            self._populate_all_widgets(status_msg, persistence_msg, quiz)
        except Exception as e:
            self._handle_persistence_error(e)

    def _previous_quiz(self, _):
        try:
            status_msg, persistence_msg, quiz = self.model.previous_quiz()
            self._populate_all_widgets(status_msg, persistence_msg, quiz)
        except Exception as e:
            self._handle_persistence_error(e)

    def _update_quiz(self, _):
        if self.view.delete_bt['state'] == tkinter.DISABLED:
            return
        try:
            marked_user_input = self.view.input_frame.get("1.0", tkinter.END)
            status_msg, persistence_msg = self.model.update_quiz(marked_user_input)
            super().update_status(status_msg)
            self.view.persistence_status['text'] = persistence_msg
        except Exception as e:
            self._handle_persistence_error(e)

    def _delete_quiz(self, _):
        if self.view.update_bt['state'] == tkinter.DISABLED:
            return
        self.delete_bt_click_count += 1
        try:
            if self.delete_bt_click_count == 1:
                self.view.persistence_status['text'] = f'Click Delete again, \u25BA \u25C4 Clear to cancel.'
            else:
                status_msg, persistence_msg = self.model.persistence.delete()
                assert status_msg in self.view.status_label['text']
                self.view.status_label['text'] = status_msg
                self.view.persistence_status['text'] = persistence_msg
                self.delete_bt_click_count = 0
        except Exception as e:
            self._handle_persistence_error(e)

    def bind_persistence_controls(self):
        self.view.next_bt.bind("<Button-1>", self._next_quiz)
        self.view.previous_bt.bind("<Button-1>", self._previous_quiz)
        self.view.update_bt.bind("<Button-1>", self._update_quiz)
        self.view.delete_bt.bind("<Button-1>", self._delete_quiz)
        if log.isEnabledFor(logging.DEBUG):
            log.debug('controller methods bound to view widgets')


def main():
    try:
        with open(os.path.dirname(__file__) + "/config_quizzer.json") as f:
            config = json.load(f)
        set_logger(config)
        if log.isEnabledFor(logging.DEBUG):
            log.info(f'config: {config}')

        v = View(Config.APP_INSTRUCTIONS)

        persistence = FilePersistence(config['QUIZZES_DIR'], config['QUIZ_FILE_PFX'])
        m = Model(persistence)

        c = QuizController(v, m)
        c.bind_quiz_controls()
        c2 = PersistenceController(v, m)
        c2.bind_persistence_controls()

        log.info('>>> Starting view')
        v.start()
    except Exception as exc:
        exc_trace = str(exc) + '\n\t' + traceback.format_exc()
        log.error(exc_trace)


if __name__ == '__main__':
    main()
