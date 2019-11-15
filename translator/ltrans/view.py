import tkinter.scrolledtext
import tkinter.ttk
import tkinter.font

class View:

    def __init__(self, language_names, instructions):
        root = tkinter.Tk()
        root.title("Word translator")
        root.configure(background='white')
        self.root = root
        self._language_names = language_names
        self._init_controls(root)
        self._init_text_areas(root)
        self.status_label = tkinter.Label(root, bg="#ccffcc", fg='black',
                                          text=instructions)
        self.status_label.pack(side=tkinter.LEFT, fill='both', expand='yes')

    @property
    def language_names(self):
        return self._language_names

    def _init_controls(self, root):
        frame = tkinter.Frame(root, height=500)
        frame.pack(fill='both', expand='yes')
        self.clear_bt = tkinter.Button(frame, text="  Clear  ")
        fromTo_label = tkinter.Label(frame, text="From / to :")

        self.src_language = tkinter.ttk.Combobox(frame, width=20, height=1, font=("Arial", 9),
                                                 values=self.language_names, state='readonly')
        self.destination_language = tkinter.ttk.Combobox(frame, width=20, height=1, font=("Arial", 9),
                                                         values=self.language_names, state='readonly')
        self.swap_languages_bt = tkinter.Button(frame, text="  ⇆  ", height = 1, width = 2)
        self.is_add_src = tkinter.IntVar()
        self.add_source_check_button = tkinter.Checkbutton(frame, text="Add source", bg="white", variable=self.is_add_src)
        self.is_add_transliteration = tkinter.IntVar()
        self.add_transliteration_check_button = tkinter.Checkbutton(frame, text="Transliterate", bg="white",
                                              variable=self.is_add_transliteration, state=tkinter.DISABLED)
        self.trans_bt = tkinter.Button(frame, text="  Translate  ", state=tkinter.DISABLED)

        self.save_bt = tkinter.Button(frame, text="  Save  ", height = 1)
        saved_label = tkinter.Label(frame, text="     Saved translations:")
        self.next_bt = tkinter.Button(frame, text=" Next ", height = 1)
        self.previous_bt = tkinter.Button(frame, text=" Previous ", height = 1)
        self.delete_bt = tkinter.Button(frame, text=" Delete ", height = 1)

        self.clear_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        fromTo_label.pack(side=tkinter.LEFT, padx=5, pady=2)

        self.src_language.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.swap_languages_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.destination_language.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.add_source_check_button.pack(side=tkinter.LEFT, pady=2)
        self.add_transliteration_check_button.pack(side=tkinter.LEFT, pady=2)
        self.trans_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.save_bt.pack(side=tkinter.LEFT, padx=5, pady=2)

        saved_label.pack(side=tkinter.LEFT, padx=2, pady=2)
        self.next_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.previous_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.delete_bt.pack(side=tkinter.LEFT, padx=5, pady=2)

        frame.pack( fill='both', expand=False)

    def _init_text_areas(self, root):
        self.txt_frame = tkinter.Frame(root)
        self.input_frame = tkinter.scrolledtext.ScrolledText(self.txt_frame)
        self.input_frame.pack(side=tkinter.LEFT, pady=2, fill='both', expand='yes')

        self.output_frame = tkinter.scrolledtext.ScrolledText(self.txt_frame)
        self.output_frame.pack(side=tkinter.LEFT, pady=2, fill='both', expand='yes')
        self.txt_frame.pack(fill='both', expand='yes')


    def _init_persistence_controls(self, root):
        frame = tkinter.Frame(root)
        frame.pack(fill='both', expand='yes')
        self.save_bt = tkinter.Button(frame, text="Save", height = 1, width = 2)
        self.next_bt = tkinter.Button(frame, text="Display next", height = 1, width = 2)
        self.previous_bt = tkinter.Button(frame, text="Display previous", height = 1, width = 2)
        self.delete_bt = tkinter.Button(frame, text="Delete", height = 1, width = 2)

        self.save_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.next_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.previous_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.delete_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        frame.pack()

    def bind_controls(self, controller, model):
        self.clear_bt.bind("<Button-1>", controller.clear_input)
        self.input_frame.bind("<Leave>", controller.find_src_language)
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

