import tkinter.scrolledtext
import tkinter.ttk


class View:

    def __init__(self, language_names):
        root = tkinter.Tk()
        root.title("Model")
        root.configure(background='white')
        self.root = root
        self._init_text_areas(root)
        self._language_names = language_names
        self._init_controls(root)

    @property
    def language_names(self):
        return self._language_names

    def _init_text_areas(self, root):
        self.txt_frame = tkinter.Frame(root)
        self.input_frame = tkinter.scrolledtext.ScrolledText(self.txt_frame)
        self.input_frame.grid(row=0, column=0, padx=2, pady=2)
        self.output_frame = tkinter.scrolledtext.ScrolledText(self.txt_frame)
        self.output_frame.grid(row=0, column=1, padx=2, pady=2)
        self.txt_frame.pack()

    def _init_controls(self, root):
        self.src_language = tkinter.ttk.Combobox(root, width=20, height=1, font=("Arial", 9),
                                                 values=self.language_names, state='readonly')
        self.destination_language = tkinter.ttk.Combobox(root, width=20, height=1, font=("Arial", 9),
                                                         values=self.language_names, state='readonly')
        self.trans_bt = tkinter.Button(root, text="  Translate  ", state=tkinter.DISABLED)
        self.is_add_src = tkinter.IntVar()
        add_source_check_button = tkinter.Checkbutton(root, text="Source", bg="white", variable=self.is_add_src)
        self.is_add_pronunciation = tkinter.IntVar()
        add_pronunciation_check_button = tkinter.Checkbutton(root, text="Pronunciation", bg="white",
                                                               variable=self.is_add_pronunciation)
        self.clear_bt = tkinter.Button(root, text="  Clear  ")
        self.status_label = tkinter.Label(root, bg="white",
                                          text="Enter text on left panel & exit panel to translate it")

        self.src_language.pack(side=tkinter.LEFT, padx=5, pady=2)
        arrow_label = tkinter.Label(root, bg="white", font=("Arial", 12), text="→")
        arrow_label.pack(side=tkinter.LEFT, padx=2, pady=2)
        self.destination_language.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.trans_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        add_label = tkinter.Label(root, bg="white", text="   Add:")
        add_label.pack(side=tkinter.LEFT, padx=5, pady=2)
        add_source_check_button.pack(side=tkinter.LEFT, pady=2)
        add_pronunciation_check_button.pack(side=tkinter.LEFT, pady=2)
        self.clear_bt.pack(side=tkinter.LEFT, padx=5, pady=2)
        self.status_label.pack(side=tkinter.LEFT, padx=5, pady=2)

    def bind_controls(self, controller, model):
        self.clear_bt.bind("<Button-1>", controller.clear_input)
        self.input_frame.bind("<Leave>", controller.find_src_language)
        self.destination_language.bind("<KeyRelease>", controller.set_dest_language)
        self.trans_bt.bind("<Button-1>", controller.translate_text)
        self.root.protocol("WM_DELETE_WINDOW", controller.on_closing)
        self.txt_frame.bind("<Key>", controller.txt_frame_key_press)
        print('Connroller bound to view')

    def start(self):
        self.root.mainloop()

    def stop(self):
        self.root.destroy()
        print('s        ssss   sss')

if __name__ == '__main__':
    v = View(['French', 'Spanish'])
    v.start()
    v.stop()
    print('done')

