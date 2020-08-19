import atexit
import logging
import shutil
import sys
from datetime import datetime
from os import mkdir
from os import path
from tkinter import messagebox

import pi.update_and_checkin

logging_file_name = __file__ + '.log'


def exit_handler():
    archive_log()
    with open(logging_file_name) as f:
        if not logging.getLogger().isEnabledFor(logging.DEBUG):
            messagebox.showinfo(logging_file_name, f.read())
        else:
            print(f.read())


def archive_log():
    archive_dir = './logs-check-ins'
    if not path.isdir(archive_dir):
        mkdir(archive_dir)
    log_archive_file = archive_dir + '/' + logging_file_name + '-' + \
                       str(datetime.now()).replace(':', '-') + '.log'
    shutil.copyfile(logging_file_name, log_archive_file)


def config_log():
    if len(sys.argv) == 1:
        log_level = logging.INFO
        log_format = '%(message)s'
    else:
        log_level = logging.DEBUG
        # log_format = '%(asctime)s - [%(levelname)s] - %(name)s - %(filename)s.%(funcName)s(%(lineno)d) - %(message)s'
        log_format = '[%(levelname)s] - %(name)s - %(filename)s.%(funcName)s(%(lineno)d) - %(message)s'
    logging.basicConfig(filename=logging_file_name, filemode='w', level=log_level, format=log_format)


if __name__ == '__main__':
    config_log()
    atexit.register(exit_handler)
    pi.update_and_checkin.main('br1')
