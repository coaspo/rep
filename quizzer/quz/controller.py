import json
import logging
import os
import tkinter
import tkinter.ttk
import traceback

from quz.model import Model
from quz.quiz import QuizDataError, Quiz, MultipleChoiceQuestion
from quz.util import Config, set_logger
from quz.view import View

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
        self.view.clear_screen()
        self.delete_bt_click_count = 0
        self.update_status(Config.APP_INSTRUCTIONS)

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

    def _populate_all_widgets(self, status_msg: str, persistence_msg: str, quiz: Quiz):
        self.view.input_marked_text_area.delete('1.0', tkinter.END)
        # self.view.save_bt.config(state=tkinter.DISABLED)
        self.view.input_marked_text_area.insert(tkinter.END, quiz.marked_user_input)
        status_msg = status_msg + ';  may change text and click Update, or click Delete'
        self.update_status(status_msg)

        self.delete_bt_click_count = 0
        self.view.persistence_status_label['text'] = persistence_msg
        self.view.delete_quiz_bt.config(state=tkinter.NORMAL)
        self.view.update_bt.config(state=tkinter.NORMAL)

    @staticmethod
    def set_check_button(button: tkinter.Checkbutton, value: int):
        if value == 1:
            button.select()
        else:
            button.deselect()

    def _display_question(self, question: MultipleChoiceQuestion):
        self.view.question_label['text'] = make_multiple_lines(question.question)
        self.view.question_comment_label['text'] = '' if question.comment is None else make_multiple_lines(
            question.comment)

        [chk_bt.destroy() for (_, chk_bt) in self.view.answer_check_buttons]
        self.view.answer_check_buttons.clear()

        for i, answer in enumerate(question.answers):
            is_set = 1 if answer.is_selected else 0
            is_selected = tkinter.IntVar(value=is_set)
            chk_bt = tkinter.Checkbutton(self.view.question_area, text=make_multiple_lines(answer.answer), bg='white',
                                         variable=is_selected, padx=15)

            chk_bt.grid(row=i + 1, column=0, sticky=tkinter.W, pady=2)
            self.view.answer_check_buttons.append((is_selected, chk_bt))


class MainController(Controller):

    def _save_quiz(self, _):
        try:
            text = self.view.input_marked_text_area.get("1.0", tkinter.END)
            topic = self.view.quiz_topics.get().strip()
            combo_values = self.view.quiz_topics['values']
            if topic not in combo_values:
                if isinstance(combo_values, str):
                    if len(combo_values.strip()):
                        combo_values = topic
                    else:
                        combo_values = (combo_values, topic)
                else:
                    combo_values += (topic,)
                self.view.quiz_topics['values'] = combo_values
            status_msg = self.model.save_quiz(topic, text)
            super().update_status(status_msg)
        except Exception as e:
            self.handle_exception('Save error: ', e)

    def bind_main_controls(self):
        self.view.clear_bt.bind("<Button-1>", super().clear_screen)
        self.view.quiz_topics.bind("<<ComboboxSelected>>", self.reset_persistence)
        self.view.input_marked_text_area.bind("<FocusOut>", self._save_quiz)

        self.view.next_question_bt.bind("<Button-1>", self._next_question)
        self.view.previous_question_bt.bind("<Button-1>", self._previous_question)

        self.view.root.protocol("WM_DELETE_WINDOW", self.view.stop)
        if log.isEnabledFor(logging.DEBUG):
            log.debug('controller methods bound to view widgets')

    def reset_persistence(self, _):
        topic = self.view.quiz_topics.get()
        status_msg, persistence_msg, quiz = self.model.reset_quiz_topic(topic)
        self._populate_all_widgets(status_msg, persistence_msg, quiz)

    def _next_question(self, _):
        try:
            question = self.model.next_quiz().current_question()
            self._display_question(question)
        except Exception as e:
            super().handle_exception('Next question err', e)

    def _previous_question(self, _):
        try:
            question = self.model.previous_quiz().current_question()
            self._display_question(question)
        except Exception as e:
            self.handle_exception('Previous question err', e)


class PersistenceController(Controller):
    def _handle_persistence_error(self, e):
        self.handle_exception('PersistenceController error: ', e)
        self.view.persistence_status_label['text'] = 'See error below or in log file'

    def _next_quiz(self, _):
        try:
            status_msg, persistence_msg, quiz = self.model.next_quiz()
            self._populate_all_widgets(status_msg, persistence_msg, quiz)
            self._display_question(quiz.current_question())
        except Exception as e:
            self._handle_persistence_error(e)

    def _previous_quiz(self, _):
        try:
            status_msg, persistence_msg, quiz = self.model.previous_quiz()
            self._populate_all_widgets(status_msg, persistence_msg, quiz)
            self._display_question(quiz.current_question())
        except Exception as e:
            self._handle_persistence_error(e)

    def _update_quiz(self, _):
        if self.view.delete_quiz_bt['state'] == tkinter.DISABLED:
            return
        try:
            marked_user_input = self.view.input_marked_text_area.get("1.0", tkinter.END)
            status_msg, persistence_msg = self.model.update_quiz(marked_user_input)
            super().update_status(status_msg)
            self.view.persistence_status_label['text'] = persistence_msg
        except Exception as e:
            self._handle_persistence_error(e)

    def _delete_quiz(self, _):
        if self.view.update_bt['state'] == tkinter.DISABLED:
            return
        self.delete_bt_click_count += 1
        try:
            if self.delete_bt_click_count == 1:
                self.view.persistence_status_label['text'] = f'Click Delete again, \u25BA \u25C4 Clear to cancel.'
            else:
                status_msg, persistence_msg = self.model.delete_quiz()
                assert status_msg in self.view.status_label['text']
                self.view.status_label['text'] = status_msg
                self.view.persistence_status_label['text'] = persistence_msg
                self.delete_bt_click_count = 0
        except Exception as e:
            self._handle_persistence_error(e)

    def bind_persistence_controls(self):
        self.view.next_quiz_bt.bind("<Button-1>", self._next_quiz)
        self.view.previous_quiz_bt.bind("<Button-1>", self._previous_quiz)
        self.view.update_bt.bind("<Button-1>", self._update_quiz)
        self.view.delete_quiz_bt.bind("<Button-1>", self._delete_quiz)
        if log.isEnabledFor(logging.DEBUG):
            log.debug('controller methods bound to view widgets')


def main():
    try:
        with open(os.path.dirname(__file__) + "/config_quizzer.json") as f:
            config = json.load(f)
        set_logger(config)
        if log.isEnabledFor(logging.DEBUG):
            log.info(f'config: {config}')

        m = Model(config['QUIZZES_DIR'])

        v = View(m.latest_quiz_topic, m.quiz_topics, Config.APP_INSTRUCTIONS)

        c = MainController(v, m)
        c.bind_main_controls()
        c2 = PersistenceController(v, m)
        c2.bind_persistence_controls()

        log.info('>>> Starting view')
        v.start()
    except Exception as exc:
        exc_trace = str(exc) + '\n\t' + traceback.format_exc()
        log.error(exc_trace)


def make_multiple_lines(line: str) -> str:
    if len(line) < 5:
        return line
    paragraph = []
    is_new_line_added = False
    line_num = 1
    for i, c in enumerate(line):
        paragraph.append(c)
        if 75 * line_num < i < 90 * line_num and c == ' ':
            if not is_new_line_added:
                line_num += 1
                paragraph.append('\n')
                is_new_line_added = True
        else:
            is_new_line_added = False
    return ''.join(paragraph)


if __name__ == '__main__':
    main()
