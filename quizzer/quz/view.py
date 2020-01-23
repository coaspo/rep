import logging
import os
import tkinter.font
import tkinter.scrolledtext
import tkinter.ttk
import webbrowser

log = logging.getLogger(__name__)


class View:
    def __init__(self, latest_quiz_topic: str, quiz_topics: list, instructions: str):
        root = tkinter.Tk()
        root.title("Quiz maker/taker")
        self._quiz_answer_bts = []
        self._root = root
        self._init_menu(latest_quiz_topic, quiz_topics, root)
        self._init_text_areas(root)
        self._init_bottom(root, instructions)
        self._answer_check_buttons = None
        if log.isEnabledFor(logging.DEBUG):
            log.debug("Finished")

    @property
    def answer_check_buttons(self) -> list:
        return self._answer_check_buttons

    @property
    def clear_bt(self):
        return self._clear_bt

    @property
    def create_quiz_bt(self):
        return self._create_quiz_bt

    @property
    def input_frame(self):
        return self._input_frame

    @property
    def output_frame(self):
        return self._question_frame

    @property
    def save_bt(self):
        return self._save_bt

    @property
    def next_bt(self):
        return self._next_quiz_bt

    @property
    def previous_bt(self):
        return self._previous_quiz_bt

    @property
    def persistence_status(self):
        return self._persistence_status_label

    @property
    def update_bt(self):
        return self._update_bt

    @property
    def delete_bt(self):
        return self._delete_bt

    @property
    def question_frame(self):
        return self._question_frame

    @property
    def status_label(self):
        return self._status_label

    @property
    def quiz_topics(self):
        return self._quiz_topics

    @property
    def root(self):
        return self._root

    def _init_menu(self, latest_quiz_topic: str, quiz_topics: list, root: tkinter.Tk):
        light_yellow = '#ffffcc'
        frame = tkinter.Frame(root, height=500)
        menu_background_color = light_yellow
        frame.configure(background=menu_background_color)
        self._init_main_menu(latest_quiz_topic, quiz_topics, frame, menu_background_color)
        self._init_persistence_menu(frame, menu_background_color)
        frame.pack(fill=tkinter.BOTH, expand=False)

    def _init_main_menu(self, latest_quiz_topic: str, quiz_topics: list, frame, frame_color):
        self._clear_bt = tkinter.Button(frame, text="  Clear  ")
        topic_label = tkinter.Label(frame, text="   Quiz topic:", bg=frame_color)
        self.variableCombo_value = tkinter.StringVar()
        self._quiz_topics = tkinter.ttk.Combobox(frame, width=10, height=12, font=("Arial", 9),
                                                 values=quiz_topics, textvariable=self.variableCombo_value)
        if len(quiz_topics) > 0 and latest_quiz_topic in quiz_topics:
            self._quiz_topics.current(quiz_topics.index(latest_quiz_topic))
        self._create_quiz_bt = tkinter.Button(frame, text="  Create Quiz  ", height=1)
        self._save_bt = tkinter.Button(frame, text="  Save  ", height=1)

        self._clear_bt.pack(side=tkinter.LEFT, padx=12, pady=2)
        topic_label.pack(side=tkinter.LEFT, pady=2)
        self._quiz_topics.pack(side=tkinter.LEFT, padx=5, pady=2)
        self._create_quiz_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self._save_bt.pack(side=tkinter.LEFT, padx=5, pady=2)

    def _init_persistence_menu(self, frame, frame_color):
        saved_label = tkinter.Label(frame, text="                          Saved quizzes:", bg=frame_color)
        self._previous_quiz_bt = tkinter.Button(frame, text=u' \u25C4 ', height=1)
        self._next_quiz_bt = tkinter.Button(frame, text=u' \u25BA  ', height=1)
        self._persistence_status_label = tkinter.Label(frame, text="", anchor='w', bg='white')
        self._persistence_status_label.config(width=30)
        self._update_bt = tkinter.Button(frame, text="Update", height=1, state=tkinter.DISABLED)
        self._delete_bt = tkinter.Button(frame, text="Delete", height=1, state=tkinter.DISABLED)
        help_label = tkinter.Label(frame, text="Help", fg="blue", bg=frame_color, cursor="hand2")
        f = tkinter.font.Font(help_label, help_label.cget("font"))
        f.configure(underline=True)
        help_label.configure(font=f)

        saved_label.pack(side=tkinter.LEFT, padx=2, pady=2)
        self._previous_quiz_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self._next_quiz_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self._persistence_status_label.pack(side=tkinter.LEFT, padx=2, pady=2)
        self._delete_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self._update_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        help_label.pack(side=tkinter.LEFT, padx=25, pady=2)
        help_label.bind("<Button-1>", lambda e: webbrowser.get('windows-default').open(
            "file://" + os.path.realpath("./quz/help.html")))

    def _init_text_areas(self, root: tkinter.Tk):
        txt_frame = tkinter.Frame(root)
        self._input_frame = tkinter.scrolledtext.ScrolledText(txt_frame)
        self._input_frame.pack(side=tkinter.LEFT, pady=2, fill='both', expand=1)
        # self._input_frame.grid(row=0, column=0, sticky=tkinter.NE, pady=2)

        self._question_frame = tkinter.Frame(txt_frame, bg="white")
        self._question = tkinter.Label(self._question_frame, text=150 * " ", fg="blue", bg='white')
        self._comment = tkinter.Label(self._question_frame, text="a commnet here ", fg="blue", bg='white')
        self._is_check_A = tkinter.IntVar()
        self._is_check_B = tkinter.IntVar()
        self._check_A = tkinter.Checkbutton(self._question_frame, text="answer a", bg='white',
                                            variable=self._is_check_A)
        self._check_B = tkinter.Checkbutton(self._question_frame, text="answer B---\nthis is long", bg='white',
                                            variable=self._is_check_B)
        self._quiz_answer_bts.append((self._is_check_A, self._check_A))
        self._quiz_answer_bts.append((self._is_check_B, self._check_B))
        self._submit_bt = tkinter.Button(self._question_frame, text="  Submit  ")
        self._next_question_bt = tkinter.Button(self._question_frame, text=u' \u25BA  ', height=1)
        self._previous_question_bt = tkinter.Button(self._question_frame, text=u' \u25C4 ', height=1)
        self._submit_bt.place(x=20, y=330, width=100, height=25)
        self._previous_question_bt.place(x=160, y=330, width=40, height=25)
        self._next_question_bt.place(x=210, y=330, width=40, height=25)

        self._question.grid(row=0, column=0, columnspan=14, sticky=tkinter.W, pady=2)
        self._check_A.grid(row=1, column=0, sticky=tkinter.W, pady=2)
        self._check_B.grid(row=2, column=0, sticky=tkinter.W, pady=2)
        self._comment.grid(row=3, column=0, sticky=tkinter.W, pady=2)
        # self._submit_bt.grid(row=7, column=0, pady=2)

        spacer_label = tkinter.Label(self._question_frame, text=150 * ' ', fg="blue", bg='white')
        spacer_label.grid(row=15, column=0, columnspan=14, sticky=tkinter.W, pady=2)

        self._question_frame.pack(side=tkinter.LEFT, pady=2, fill='both', expand=1)
        # self._question_frame.grid(row=0, column=1, sticky=tkinter.NESW, pady=2)
        txt_frame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    def _init_bottom(self, root, instructions: str):
        frame = tkinter.Frame(root)
        frame.pack(expand=False)
        self._status_label = tkinter.Label(root, bg="#eeffee", fg='black')
        self._status_label['text'] = instructions

        self._status_label.pack(side=tkinter.LEFT, fill='both', expand='yes')

    def start(self):
        self.root.mainloop()

    def stop(self):
        self.root.destroy()

    def delete_quiz_question(self):
        [y.destroy() for (_, y) in self._quiz_answer_bts]
        self._question.destroy()
        self._comment.destroy()

    def create_quiz_question(self, question: str, anwsers: dict, comment: str):
        self._question = tkinter.Label(self._question_frame, text="Select the correct statement(s)", fg="blue",
                                       bg='white')
        self._question.grid(row=0, column=0, sticky=tkinter.W, pady=2)
        [y.delete() for (_, y) in self._quiz_answer_bts]
        self._is_check_B = tkinter.IntVar()
        self._check_A = tkinter.Checkbutton(self._question_frame, text="answer a", bg='white',
                                            variable=self._is_check_A)
        self._check_B = tkinter.Checkbutton(self._question_frame, text="answer B---\nthis is long", bg='white',
                                            variable=self._is_check_B)


if __name__ == '__main__':
    v = View('quiz', ['java', 'sql'], 'This is a manual layout test. To run the application, run cli.py')
    print('start')
    v.start()
    print('done')
