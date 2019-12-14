import logging
import os
import tkinter.font
import tkinter.scrolledtext
import tkinter.ttk
import webbrowser

log = logging.getLogger(__name__)


class View:
    def __init__(self, language_names: list, instructions: str):
        root = tkinter.Tk()
        root.title("Word translator")
        self._root = root
        self._language_names = language_names
        self._init_menu(root)
        self._init_text_areas(root)
        self._init_bottom(root, instructions)
        if log.isEnabledFor(logging.DEBUG):
            log.debug("Finished")

    @property
    def language_names(self):
        return self._language_names

    @property
    def clear_bt(self):
        return self._clear_bt

    @property
    def destination_language(self):
        return self._destination_language

    @property
    def trans_bt(self):
        return self._trans_bt

    @property
    def swap_languages_bt(self):
        return self._swap_languages_bt

    @property
    def add_source_check_bt(self):
        return self._add_source_check_bt

    @property
    def add_transliteration_check_bt(self):
        return self._add_transliteration_check_bt

    @property
    def is_add_src(self):
        return self._is_add_src

    @property
    def add_transliteration_check_bt(self):
        return self._add_transliteration_check_bt

    @property
    def is_add_transliteration(self):
        return self._is_add_transliteration

    @property
    def save_bt(self):
        return self._save_bt

    @property
    def next_bt(self):
        return self._next_bt

    @property
    def previous_bt(self):
        return self._previous_bt

    @property
    def delete_bt(self):
        return self._delete_bt

    @property
    def root(self):
        return self._root

    def _init_menu(self, root: tkinter.Tk):
        light_yellow = '#ffffcc'
        frame: tkinter.Frame = tkinter.Frame(root, height=500)
        frame.configure(background=light_yellow)
        frame.pack(fill='both', expand='yes')
        self._clear_bt = tkinter.Button(frame, text="  Clear  ")
        from_to_label = tkinter.Label(frame, text="From / to :", bg=light_yellow)

        self.src_language = tkinter.ttk.Combobox(frame, width=10, height=12, font=("Arial", 9),
                                                 values=self.language_names, state='readonly')
        self.src_language.current(0)
        self._destination_language = tkinter.ttk.Combobox(frame, width=12, height=10, font=("Arial", 9),
                                                          values=self.language_names, state='readonly')
        self._destination_language.current(1)
        self._swap_languages_bt = tkinter.Button(frame, text="  ⇆  ", height=1, width=2)
        self._is_add_src = tkinter.IntVar()
        self._add_source_check_bt = tkinter.Checkbutton(frame, text="Add source", bg=light_yellow,
                                                        variable=self._is_add_src)
        self._is_add_transliteration = tkinter.IntVar()
        self._add_transliteration_check_bt = tkinter.Checkbutton(frame, text="Transliterate", bg=light_yellow,
                                                                 variable=self._is_add_transliteration,
                                                                 state=tkinter.DISABLED)
        self._trans_bt = tkinter.Button(frame, text="  Translate  ")
        self._save_bt = tkinter.Button(frame, text="  Save  ", height=1)
        saved_label = tkinter.Label(frame, text="     Saved translations:", bg=light_yellow)
        self._next_bt = tkinter.Button(frame, text=u' \u25BA  ', height=1)
        self._previous_bt = tkinter.Button(frame, text=u' \u25C4 ', height=1)
        self._delete_bt = tkinter.Button(frame, text=" Delete ", height=1)
        help_label = tkinter.Label(frame, text="Help", fg="blue", bg=light_yellow, cursor="hand2")

        self._clear_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        from_to_label.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.src_language.pack(side=tkinter.LEFT, padx=5, pady=2)
        self._swap_languages_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self._destination_language.pack(side=tkinter.LEFT, padx=5, pady=2)

        self._add_source_check_bt.pack(side=tkinter.LEFT, pady=2)
        self._add_transliteration_check_bt.pack(side=tkinter.LEFT, pady=2)
        self._trans_bt.pack(side=tkinter.LEFT, padx=5, pady=2)

        self._save_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        saved_label.pack(side=tkinter.LEFT, padx=2, pady=2)
        self._next_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self._previous_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self._delete_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        help_label.pack(side=tkinter.LEFT, padx=25, pady=2)
        help_label.bind("<Button-1>", lambda e: webbrowser.get('windows-default').open(
            "file://" + os.path.realpath("./ltrans/help.html")))

        frame.pack(fill='both', expand=False)

    def _init_persistence_controls(self, root: tkinter.Tk):
        frame = tkinter.Frame(root)
        frame.pack(fill='both', expand='yes')
        self._save_bt = tkinter.Button(frame, text="Save", height=1, width=2)
        self._next_bt = tkinter.Button(frame, text="Display next", height=1, width=2)
        self._previous_bt = tkinter.Button(frame, text="Display previous", height=1, width=2)
        self._delete_bt = tkinter.Button(frame, text="Delete", height=1, width=2)

        self._save_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self._next_bt.pack(side=tkinter.LEFT, padx=5, pady=2)

        self._previous_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self._delete_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        frame.pack()

    def _init_text_areas(self, root: tkinter.Tk):
        self.txt_frame = tkinter.Frame(root)
        self.input_frame = tkinter.scrolledtext.ScrolledText(self.txt_frame)
        self.input_frame.pack(side=tkinter.LEFT, pady=2, fill='both', expand='yes')

        self.output_frame = tkinter.scrolledtext.ScrolledText(self.txt_frame)
        self.output_frame.pack(side=tkinter.LEFT, pady=2, fill='both', expand='yes')
        self.txt_frame.pack(fill='both', expand='yes')

    def _init_bottom(self, root, instructions: str):
        frame = tkinter.Frame(root)
        frame.pack(fill='both', expand='yes')
        self.status_label = tkinter.Label(root, bg="#eeffee", fg='black')
        self.status_label['text'] = instructions

        self.status_label.pack(side=tkinter.LEFT, fill='both', expand='yes')

    def start(self):
        self.root.mainloop()

    def stop(self):
        self.root.destroy()


def _create_two_column_table(input_text: str, translated_text: str):
    html = list('<table><tr><td>')
    html.append(input_text)
    html.append('</td><td>')
    html.append(translated_text)
    html.append('</td></tr></table>')
    return ''.join(html)


if __name__ == '__main__':
    v = View(['English', 'Spanish'], 'This is a manual layout test. To run the application, run cli.py')
    print('start')
    v.start()
    print('done')
