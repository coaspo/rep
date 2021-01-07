import logging
import os
import traceback
from tkinter import messagebox

import pi.controller
from pi.log import config_log

if __name__ == '__main__':
    try:
        log_file_name = os.path.basename(__file__) + '.log'
        config_log(log_file_name)
        pi.controller.main('br1')
    except Exception as e:
        logging.error(traceback.format_exc())
        print(traceback.format_exc())
        if not logging.getLogger().isEnabledFor(logging.DEBUG):
            messagebox.showinfo(__file__, os.path.basename(__file__) + ' FAILED; \n\n' +
                                str(e) + '\n\nSee trace i...')
