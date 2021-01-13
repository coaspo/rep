#!/usr/bin/env python3
import logging
import os
from datetime import datetime

from wpy.checkin import CheckIn
from wpy.contentspage import ContentsPage
from wpy.indexpage import IndexPage
from wpy.website import WebSite


def main(git_branch):
    #CheckIn.run_tests()
    target_dirs = ('../w/tech', '../w/recipes', '../w/arts', '../w/science')
    logging.info(str(datetime.now()))
    website = WebSite(target_dirs)
    website.save_search_file_paths('../w/search_file_paths.txt')
    website.save_search_labels('../w/search_labels.txt')
    version = ContentsPage.update(website, '../w/contents.html')
    IndexPage.update_links(website)
    print('Current dir:', os.getcwd())
    CheckIn.run_git_commands(version, git_branch)
    os.chdir('../w')
    print('Current dir:', os.getcwd())
    CheckIn.run_git_commands(version, git_branch)
    os.chdir('../wcheckin')
    logging.info('done')
