import atexit
import logging
import shutil
import sys
from datetime import datetime
from os import mkdir
from os import path
from tkinter import messagebox


logging_file_name: str = ''


def _exit_handler():
    _archive_log()
    global logging_file_name
    with open(logging_file_name) as f:
        if not logging.getLogger().isEnabledFor(logging.DEBUG):
            messagebox.showinfo(logging_file_name, f.read())
        else:
            print(f.read())


def _archive_log():
    archive_dir = './logs-publish-and-check-ins'
    if not path.isdir(archive_dir):
        mkdir(archive_dir)
    global logging_file_name
    archived_name = logging_file_name.replace('.log', str(datetime.now()).replace(':', '-') + '.log')
    log_archive_file = archive_dir + '/' + archived_name
    shutil.copyfile(logging_file_name, log_archive_file)


def config_log(file_name):
    global logging_file_name
    logging_file_name = file_name
    if len(sys.argv) == 1:
        log_level = logging.INFO
        log_format = '%(message)s'
    else:
        log_level = logging.DEBUG
        # log_format = '%(asctime)s - [%(levelname)s] - %(name)s - %(filename)s.%(funcName)s(%(lineno)d) - %(message)s'
        log_format = '[%(levelname)s] - %(name)s - %(filename)s.%(funcName)s(%(lineno)d) - %(message)s'
    logging.basicConfig(filename=logging_file_name, filemode='w', level=log_level, format=log_format)
    atexit.register(_exit_handler)
