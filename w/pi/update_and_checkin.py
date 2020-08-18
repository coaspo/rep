#!/usr/bin/env python3
from datetime import datetime
from os import mkdir
from os import path
from shutil import copy
from tkinter import messagebox
import os
import traceback

from pi.checkin import CheckIn
from pi.contentspage import ContentsPage
from pi.indexpage import IndexPage
from pi.website import WebSite




# def log(*args):
#     global LOG_FILE
#     if LOG_FILE is None:
#         LOG_FILE = path.basename(__file__) + '.log'
#         with open(LOG_FILE, 'w') as f:
#             f.write(str(datetime.now()))
#
#     with open(LOG_FILE, 'a') as f:
#         f.write('\n')
#         for arg in args:
#             f.write(' ' + str(arg))


def create_link(file_path):
    i_start = file_path.index('/') + 1
    i_end = file_path.rindex('.html')
    file_name = file_path[i_start:i_end].replace('_', ' ')
    link = '<a href=\'./' + file_path + '\'>' + file_name + '</a>'
    return link


def archive_log():
    archive_dir = './logs-check-ins'
    if not path.isdir(archive_dir):
        mkdir(archive_dir)
    log_archive_file = archive_dir + '/' + path.basename(__file__) + '-' + \
                       str(datetime.now()).replace(':', '-') + '.log'
    # copy(LOG_FILE, log_archive_file)


def main(git_branch):
    msg = ''
    target_dirs = ('./tech', './science', './recipes', './arts')
    try:
        website = WebSite(target_dirs)
        website.save_search_file_paths('search_file_paths.txt')
        website.save_search_labels('search_labels.txt')
        version = ContentsPage.update(website.file_paths)
        IndexPage.update_links(website.file_paths)
        CheckIn.runGitCommands(version, git_branch)

        # log('done')
        archive_log()
        messagebox.showinfo(__file__, msg + '\ndone')
    except Exception as e:
        print(traceback.format_exc())
        messagebox.showinfo(__file__, os.path.basename(__file__) + ' FAILED; \n\n' + \
                            str(e) + '\n\nSee trace i...')
        ##log(traceback.format_exc())




if __name__ == '__main__':
    import doctest

    # This runs just a couple of tests;
    #  to run more tests, use w/check_in_tests.py
    doctest.testmod()
