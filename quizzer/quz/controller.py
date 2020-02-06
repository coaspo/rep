import json
import logging
import os
import tkinter
import tkinter.ttk
import traceback
from tkinter import ACTIVE, messagebox

from quz.model import Model
from quz.quiz import QuizError
from quz.util import Config, set_logger
from quz.view import View

log = logging.getLogger(__name__)


class AbstractController:
    def __init__(self, view: View, model: Model):
        self.view = view
        self.model = model

    def handle_exception(self, msg: str, exc: Exception = None):
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

    def _update_status(self, text: str, is_err=False):
        self.view.status_label['text'] = text
        background = "#ffeeee" if is_err else "#eeffee"
        self.view.status_label.config(bg=background)

    def _populate_quiz_widgets(self):
        if self.model.quiz is None:
            self.view.clear_screen()
        else:
            self.view.input_marked_text_area.delete('1.0', tkinter.END)
            self.view.input_marked_text_area.insert(tkinter.END, self.model.quiz.marked_user_input)
            self.view.quiz_description_label['text'] = self.model.quiz_description
            self._populate_question_widgets()
            self.view.next_question_bt.configure(state=ACTIVE)
            self.view.previous_question_bt.configure(state=ACTIVE)
            self.view.submit_bt.configure(state=ACTIVE)
        self._update_status(self.model.status_msg)

    def _populate_question_widgets(self):
        question = self.model.quiz.current_question()
        self.view.question_label['text'] = AbstractController._make_multiple_lines(question.question)
        cmt = '' if question.comment is None else question.comment
        self.view.question_comment_label['text'] = cmt
        self._populate_answers_widgets()

    def _populate_answers_widgets(self):
        [chk_bt.destroy() for (_, chk_bt) in self.view.answer_check_buttons]
        self.view.answer_check_buttons.clear()

        for i, answer in enumerate(self.model.quiz.current_question().answers):
            is_set = 1 if answer.is_selected else 0
            is_selected = tkinter.IntVar(value=is_set)
            chk_bt = tkinter.Checkbutton(self.view.question_area,
                                         text=AbstractController._make_multiple_lines(answer.answer), bg='white',
                                         variable=is_selected, padx=15)
            chk_bt.grid(row=i + 1, column=0, sticky=tkinter.W, pady=2)
            self.view.answer_check_buttons.append((is_selected, chk_bt))

    @staticmethod
    def _make_multiple_lines(line: str) -> str:
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


class QuizController(AbstractController):

    def __init__(self, view: View, model: Model):
        AbstractController.__init__(self, view, model)
        quiz = self.model.get_quiz()
        if quiz is not None:
            self._populate_quiz_widgets()

    def clear_entire_screen(self, _):
        self.view.clear_screen()
        self._update_status(Config.APP_INSTRUCTIONS)

    def update_quiz(self, _):
        try:
            topic = self.view.quiz_topics.get().strip()
            if len(topic) == 0:
                raise QuizError('Topic drop down is empty')
            self._update_combo_box_topics(topic)
            marked_user_input = self.view.input_marked_text_area.get("1.0", tkinter.END).strip()
            print('------self.model.quiz-------', self.model.quiz
                  )
            if self.model.quiz is None:
                self._create_new_quiz(marked_user_input)
            elif marked_user_input != self.model.quiz.marked_user_input:
                print('------is_any_question_answered-------', self.model.quiz.is_any_question_answered())
                if self.model.quiz.is_any_question_answered():
                    n_original = len(self.model.quiz.marked_user_input)
                    n_current = len(marked_user_input)
                    self._update_status(f"Original/current marked text are {n_original}/{n_current} characters long."
                                        "Original quiz can be updated on closing the APP.")
                else:
                    self.model.update_quiz(marked_user_input)
        except Exception as e:
            self._update_status(str(e), True)
            if str(e) != Config.MARKED_TEXT_ERR:
                self.handle_exception('Unexpected error: ', e)

    def _create_new_quiz(self, marked_user_input):
        self.model.create_new_quiz(marked_user_input)
        topic = self.view.quiz_topics.get().strip()
        self.model.save_quiz(topic)
        self._populate_quiz_widgets()

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
        marked_user_input = self.view.input_marked_text_area.get("1.0", tkinter.END).strip()
        n_original = len(self.model.quiz.marked_user_input)
        n_current = len(marked_user_input)
        print('---- ---')
        print(n_original, n_current)
        if n_original != n_current:
            is_to_recreate = messagebox.askyesno(title="Quiz inconsistency",
                                                 message=f"Original/current marked text are {n_original}/{n_current}"
                                                         "characters long."
                                                         "Marked text and the quiz are not consistent.\n"
                                                         "Would you like to update the quiz with the new mark-up?\n"
                                                         "This erases any entered answers.",
                                                 default=messagebox.NO, parent=self.view.root)
            if is_to_recreate:
                self.model.update_quiz(marked_user_input)
        else:
            self.model.update_quiz()
        self.view.stop()

    def reset_quiz_topic(self, _):
        topic = self.view.quiz_topics.get()
        self.model.reset_quiz_topic(topic)
        self._populate_quiz_widgets()

    def _next_quiz(self, _):
        try:
            self.model.set_to_next_quiz()
            self._populate_quiz_widgets()
        except Exception as e:
            self.handle_exception('Unexpected err', e)

    def _previous_quiz(self, _):
        try:
            self.model.set_to_previous_quiz()
            self._populate_quiz_widgets()
        except Exception as e:
            self.handle_exception('Unexpected err', e)

    def bind_controls(self):
        self.view.clear_bt.bind("<Button-1>", self.clear_entire_screen)
        self.view.input_marked_text_area.bind("<Leave>", self.update_quiz)
        self.view.quiz_topics.bind("<<ComboboxSelected>>", self.reset_quiz_topic)
        self.view.root.protocol("WM_DELETE_WINDOW", self.on_close_window)
        self.view.next_quiz_bt.bind("<Button-1>", self._next_quiz)
        self.view.previous_quiz_bt.bind("<Button-1>", self._previous_quiz)
        if log.isEnabledFor(logging.DEBUG):
            log.debug('controller methods bound to view widgets')


class QuizQuestionController(AbstractController):

    def next_question(self, _):
        if self.view.next_question_bt['state'] != 'disabled':
            try:
                self.model.quiz.next_question()
                self._populate_quiz_widgets()
            except Exception as e:
                super().handle_exception('Next question err', e)

    def previous_question(self, _):
        if self.view.previous_question_bt['state'] != 'disabled':
            try:
                self.model.quiz.previous_question()
                self._populate_quiz_widgets()
            except Exception as e:
                self.handle_exception('Previous question err', e)

    def submit_question_answer(self, _):
        if self.view.submit_bt['state'] != 'disabled':
            try:
                answers = self.model.quiz.current_question().answers
                print('---', answers)
                for i, (is_selected, _) in enumerate(self.view.answer_check_buttons):
                    answers[i].is_selected = is_selected.get()
                print(answers)
                self.model.quiz.next_question()
                self._populate_quiz_widgets()
                print(answers)
            except Exception as e:
                self.handle_exception('Previous question err', e)

    def bind_controls(self):
        self.view.next_question_bt.bind("<ButtonRelease-1>", self.next_question)
        self.view.previous_question_bt.bind("<Button-1>", self.previous_question)
        self.view.submit_bt.bind("<Button-1>", self.submit_question_answer)
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

        c = QuizController(v, m)
        c.bind_controls()
        c2 = QuizQuestionController(v, m)
        c2.bind_controls()

        log.info('>>> Starting view')
        v.start()
    except Exception as exc:
        exc_trace = str(exc) + '\n\t' + traceback.format_exc()
        print(exc_trace)
        log.error(exc_trace)
