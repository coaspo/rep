import shutil
import sys
from datetime import datetime
from os import mkdir

import pi.update_and_checkin
import logging
import atexit

logging_file_name = __file__ + '.log'

def exit_handler():
    archive_log()
    with open(logging_file_name) as f:
        print(f.read())


def archive_log():
    archive_dir = './logs-check-ins'
    if not sys.path.isdir(archive_dir):
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
        log_format = '%(asctime)s - [%(levelname)s] - %(name)s - %(filename)s.%(funcName)s(%(lineno)d) - %(message)s'
    logging.basicConfig(filename=logging_file_name, filemode='w', level=log_level, format=log_format)


if __name__ == '__main__':
    atexit.register(exit_handler)
    config_log()
    pi.update_and_checkin.main('br1', logging_file_name)
