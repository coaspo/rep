import json
import logging
import os
import tkinter
import tkinter.ttk
import traceback
from tkinter import messagebox

from quz.model import Model
from quz.quiz import QuizError, Quiz, MultipleChoiceQuestion
from quz.util import Config, set_logger
from quz.view import View

log = logging.getLogger(__name__)


class Controller:
    def __init__(self, view: View, model: Model):
        self.delete_bt_click_count = 0
        self.view = view
        self.model = model
        self.delete_bt_click_count = 0

    def _update_status(self, text: str, is_err=False):
        self.view.status_label['text'] = text
        background = "#ffeeee" if is_err else "#eeffee"
        self.view.status_label.config(bg=background)

    def clear_screen(self, _):
        self.view.clear_screen()
        self.delete_bt_click_count = 0
        self._update_status(Config.APP_INSTRUCTIONS)

    def handle_exception(self, msg: str, exc=None):
        if exc is None:
            log.error(msg)
            self._update_status(msg, True)
        else:
            msg_exc = msg + ' ' + str(exc)
            msg_trace = msg_exc + '\n\t' + traceback.format_exc()
            print(msg + '\n\t' + msg_trace)
            if type(exc) is not QuizError:
                log.error(msg + '\n\t' + msg_trace)
            self._update_status(msg_exc, True)

    def _populate_quiz_widgets(self):
        self.view.input_marked_text_area.delete('1.0', tkinter.END)
        # self.view.save_bt.config(state=tkinter.DISABLED)
        self.view.input_marked_text_area.insert(tkinter.END, self.model.quiz.marked_user_input)
        self._update_status(self.model.status_msg)
        self.delete_bt_click_count = 0
        self.view.quiz_description_label['text'] = self.model.description
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

    def __init__(self, view: View, model: Model):
        Controller.__init__(self, view, model)
        status_msg, persistence_msg, quiz = self.model.current_quiz()
        if quiz is not None:
            self._populate_quiz_widgets(status_msg, persistence_msg, quiz)
            self._display_question(quiz.current_question())

    def update_quiz(self, _):
        try:
            topic = self.view.quiz_topics.get().strip()
            if len(topic) == 0:
                raise QuizError('Topic drop down is empty')
            self._update_combo_box_topics(topic)
            marked_user_input = self.view.input_marked_text_area.get("1.0", tkinter.END).strip()
            if self.model.quiz is None:
                self.model.create_new_quiz(marked_user_input)
                topic = self.view.quiz_topics.get().strip()
                self.model.save_quiz(topic)
                self._populate_quiz_widgets()
            else:
                if marked_user_input != self.model.quiz.marked_user_input:
                    if len(marked_user_input) == 0:
                        is_to_delete = messagebox.askokcancel(title="Delete quiz",
                                                              message="With marked text removed,\n"
                                                                      "the quiz will be deleted.",
                                                              default=messagebox.CANCEL, parent=self.view.root)
                        if is_to_delete:
                            status_msg = self.model.delete_quiz()
                            self._populate_quiz_widgets(status_msg, self.model.quiz_description_old(), self.model.quiz)
                    else:
                        is_to_recreate= messagebox.askyesno(title="Quiz inconsistency",
                                                            message="Marked text and the quiz are not consistent.\n" \
                                                                    "Would you like to recreate the quiz?\n" \
                                                                    "This erases any entered answers.\n\n" \
                                                                    "If not, marked text area will be reset",
                                                            default=messagebox.NO, parent=self.view.root)
                        if is_to_recreate:
                            self.model.create_new_quiz(marked_user_input)
                        else:
                            self.view.input_marked_text_area.insert('insert', self.model.quiz.marked_user_input)
        except Exception as e:
            self._update_status(str(e), True)
            if str(e) != Config.MARKED_TEXT_ERR:
                self.handle_exception('Unexpected error: ', e)

    def _update_combo_box_topics(self, topic):
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

    def on_close_window(self):
        self.view.stop()

    def reset_topic(self, _):
        topic = self.view.quiz_topics.get()
        status_msg, persistence_msg, quiz = self.model.reset_quiz_topic(topic)
        self._populate_quiz_widgets(status_msg, persistence_msg, quiz)

    def next_question(self, _):
        try:
            question = self.model.current_quiz()[2].next_question()
            self._display_question(question)
        except Exception as e:
            super().handle_exception('Next question err', e)

    def previous_question(self, _):
        try:
            question = self.model.current_quiz()[2].previous_question()
            self._display_question(question)
        except Exception as e:
            self.handle_exception('Previous question err', e)

    def bind_main_controls(self):
        self.view.clear_bt.bind("<Button-1>", super().clear_screen)
        self.view.quiz_topics.bind("<<ComboboxSelected>>", self.reset_topic)
        self.view.input_marked_text_area.bind("<FocusOut>", self.update_quiz)

        self.view.input_marked_text_area.bind("<Leave>", self.update_quiz)
        self.view.next_question_bt.bind("<Button-1>", self.next_question)
        self.view.previous_question_bt.bind("<Button-1>", self.previous_question)

        self.view.root.protocol("WM_DELETE_WINDOW", self.on_close_window)
        if log.isEnabledFor(logging.DEBUG):
            log.debug('controller methods bound to view widgets')


class PersistenceController(Controller):
    def _handle_persistence_error(self, e):
        self.handle_exception('PersistenceController error: ', e)
        self.view.quiz_description_label['text'] = 'See error below or in log file'

    def _next_quiz(self, _):
        try:
            status_msg, persistence_msg, quiz = self.model.next_quiz()
            self._populate_quiz_widgets(status_msg, persistence_msg, quiz)
            self._display_question(quiz.current_question())
        except Exception as e:
            self._handle_persistence_error(e)

    def _previous_quiz(self, _):
        try:
            status_msg, persistence_msg, quiz = self.model.previous_quiz()
            self._populate_quiz_widgets(status_msg, persistence_msg, quiz)
            self._display_question(quiz.current_question())
        except Exception as e:
            self._handle_persistence_error(e)

    def _update_quiz(self, _):
        if self.view.delete_quiz_bt['state'] == tkinter.DISABLED:
            return
        try:
            marked_user_input = self.view.input_marked_text_area.get("1.0", tkinter.END)
            status_msg, persistence_msg = self.model.update_quiz(marked_user_input)
            super()._update_status(status_msg)
            self.view.quiz_description_label['text'] = persistence_msg
        except Exception as e:
            self._handle_persistence_error(e)

    def _delete_quiz(self, _):
        if self.view.update_bt['state'] == tkinter.DISABLED:
            return
        self.delete_bt_click_count += 1
        try:
            if self.delete_bt_click_count == 1:
                self.view.quiz_description_label['text'] = f'Click Delete again, \u25BA \u25C4 Clear to cancel.'
            else:
                status_msg, persistence_msg = self.model.delete_quiz()
                assert status_msg in self.view.status_label['text']
                self.view.status_label['text'] = status_msg
                self.view.quiz_description_label['text'] = persistence_msg
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
