import ltrans.controller
import tkinter.font
import tkinter.scrolledtext
import tkinter.ttk

class View:

    def __init__(self, language_names: list, instructions: str):
        root = tkinter.Tk()
        root.title("Word translator")
        self.root = root
        self._language_names = language_names
        self._init_menu(root)
        self._init_text_areas(root)
        self._init_bottom(root, instructions)

    @property
    def language_names(self):
        return self._language_names

    def _init_menu(self, root):
        print('$$$$', root)
        light_yellow = '#ffffcc'
        frame: tkinter.Frame = tkinter.Frame(root, height=500)
        frame.configure(background=light_yellow)
        frame.pack(fill='both', expand='yes')
        self.clear_bt = tkinter.Button(frame, text="  Clear  ")
        from_to_label = tkinter.Label(frame, text="From / to :", bg=light_yellow)

        self.src_language = tkinter.ttk.Combobox(frame, width=10, height=1, font=("Arial", 9),
                                                 values=self.language_names, state='readonly')
        self.src_language.current(0)
        self.destination_language = tkinter.ttk.Combobox(frame, width=10, height=1, font=("Arial", 9),
                                                         values=self.language_names, state='readonly')
        self.destination_language.current(1)
        self.swap_languages_bt = tkinter.Button(frame, text="  ⇆  ", height=1, width=2)
        self.is_each_word = tkinter.IntVar()
        self.translate_one_word_at_a_time_check_button = tkinter.Checkbutton(frame, text="One word at a time", bg=light_yellow,
                                                           variable=self.is_each_word)
        self.is_add_src = tkinter.IntVar()
        self.add_source_check_button = tkinter.Checkbutton(frame, text="Add source", bg=light_yellow,
                                                           variable=self.is_add_src)
        self.is_add_transliteration = tkinter.IntVar()
        self.add_transliteration_check_button = tkinter.Checkbutton(frame, text="Transliterate", bg=light_yellow,
                                                                    variable=self.is_add_transliteration,
                                                                    state=tkinter.DISABLED)
        self.trans_bt = tkinter.Button(frame, text="  Translate  ")
        self.save_bt = tkinter.Button(frame, text="  Save  ", height=1, state=tkinter.DISABLED)
        saved_label = tkinter.Label(frame, text="     Saved translations:", bg=light_yellow)
        self.next_bt = tkinter.Button(frame, text=u' \u25BA  ', height=1, state=tkinter.DISABLED)
        self.previous_bt = tkinter.Button(frame, text=u' \u25C4 ', height=1, state=tkinter.DISABLED)
        self.delete_bt = tkinter.Button(frame, text=" Delete ", height=1, state=tkinter.DISABLED)
        self.persistence_status_label = tkinter.Label(frame, width=80)

        # pack widgets
        self.clear_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        from_to_label.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.src_language.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.swap_languages_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.destination_language.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.translate_one_word_at_a_time_check_button.pack(side=tkinter.LEFT, pady=2)
        self.add_source_check_button.pack(side=tkinter.LEFT, pady=2)
        self.add_transliteration_check_button.pack(side=tkinter.LEFT, pady=2)
        self.trans_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.save_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        saved_label.pack(side=tkinter.LEFT, padx=2, pady=2)
        self.next_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.previous_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.delete_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.persistence_status_label.pack(side=tkinter.LEFT, padx=5, pady=2)

        frame.pack(fill='both', expand=False)

    def _init_persistence_controls(self, root):
        frame = tkinter.Frame(root)
        frame.pack(fill='both', expand='yes')
        self.save_bt = tkinter.Button(frame, text="Save", height=1, width=2)
        self.next_bt = tkinter.Button(frame, text="Display next", height=1, width=2)
        self.previous_bt = tkinter.Button(frame, text="Display previous", height=1, width=2)
        self.delete_bt = tkinter.Button(frame, text="Delete", height=1, width=2)

        self.save_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.next_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.previous_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.delete_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        frame.pack()

    def _init_text_areas(self, root):
        self.txt_frame = tkinter.Frame(root)
        self.input_frame = tkinter.scrolledtext.ScrolledText(self.txt_frame)
        self.input_frame.pack(side=tkinter.LEFT, pady=2, fill='both', expand='yes')

        self.output_frame = tkinter.scrolledtext.ScrolledText(self.txt_frame)
        self.output_frame.pack(side=tkinter.LEFT, pady=2, fill='both', expand='yes')
        self.txt_frame.pack(fill='both', expand='yes')

    def _init_bottom(self, root, instructions: str):
        frame = tkinter.Frame(root)
        frame.pack(fill='both', expand='yes')
        self.status_or_description_entry = tkinter.Entry(root, bg="#eeffee", fg='black')
        self.status_or_description_entry.insert(0, instructions)
        self.help_bt = tkinter.Button(root, text=' Help  ', height=1)

        self.status_or_description_entry.pack(side=tkinter.LEFT, fill='both', expand='yes')
        self.help_bt.pack(padx=5, pady=2)

    def bind_controls(self, controller: ltrans.controller.Controller):
        self.clear_bt.bind("<Button-1>", controller.clear_input)
        self.destination_language.bind("<KeyRelease>", controller.set_dest_language)
        self.trans_bt.bind("<Button-1>", controller.translate_text)
        self.swap_languages_bt.bind("<Button-1>", controller.swap_languages)

        self.save_bt.bind("<Button-1>", controller.save_translation)
        self.next_bt.bind("<Button-1>", controller.next_translation)
        self.previous_bt.bind("<Button-1>", controller.previous_translation)
        self.delete_bt.bind("<Button-1>", controller.delete_translation)

        self.root.protocol("WM_DELETE_WINDOW", controller.on_closing)
        print('Controller bound to view')

    def start(self):
        self.root.mainloop()

    def stop(self):
        self.root.destroy()


if __name__ == '__main__':
    v = View(['English', 'Spanish'], 'This is a manual layout test')
    print('start')
    v.start()
    print('done')
