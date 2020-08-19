#!/usr/bin/env python3
from datetime import datetime
from os import mkdir
from os import path
from tkinter import messagebox
import os
import traceback

from pi.checkin import CheckIn
from pi.contentspage import ContentsPage
from pi.indexpage import IndexPage
from pi.website import WebSite
import logging


def create_link(file_path):
    i_start = file_path.index('/') + 1
    i_end = file_path.rindex('.html')
    file_name = file_path[i_start:i_end].replace('_', ' ')
    link = '<a href=\'./' + file_path + '\'>' + file_name + '</a>'
    return link


def archive_log(logging_filename):
    archive_dir = './logs-check-ins'
    if not path.isdir(archive_dir):
        mkdir(archive_dir)
    log_archive_file = archive_dir + '/' + logging_filename + '-' + \
                       str(datetime.now()).replace(':', '-') + '.log'
    os.copy(logging_filename, log_archive_file)


def main(git_branch, logging_filename):
    target_dirs = ('./tech', './science', './recipes', './arts')
    logging.info(str(datetime.now()))
    try:
        website = WebSite(target_dirs)
        website.save_search_file_paths('search_file_paths.txt')
        website.save_search_labels('search_labels.txt')
        version = ContentsPage.update(website.file_paths)
        IndexPage.update_links(website.file_paths)
        CheckIn.run_git_commands(version, git_branch)

        logging.info('done')
        archive_log(logging_filename)
    except Exception as e:
        logging.error(traceback.format_exc())
        print(traceback.format_exc())
        if not logging.getLogger().isEnabledFor(logging.DEBUG):
            messagebox.showinfo(__file__, os.path.basename(__file__) + ' FAILED; \n\n' + \
                            str(e) + '\n\nSee trace i...')


if __name__ == '__main__':
    import doctest
    # This runs just a couple of tests;
    #  to run more tests, use w/check_in_tests.py
    doctest.testmod()
