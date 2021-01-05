#!/usr/bin/env python3
import logging
import os
from datetime import datetime

from wpy.checkin import CheckIn
from wpy.contentspage import ContentsPage
from wpy.indexpage import IndexPage
from wpy.website import WebSite


def main(git_branch):
    target_dirs = ('../w/tech', '../w/science', '../w/recipes', '../w/arts')
    logging.info(str(datetime.now()))
    website = WebSite(target_dirs)
    website.save_search_file_paths('../w/search_file_paths.txt')
    website.save_search_labels('../w/search_labels.txt')
    version = ContentsPage.update(website.web_pages)
    IndexPage.update_links(website.file_path_structures)
    CheckIn.run_tests()
    CheckIn.run_git_commands(version, git_branch)
    print('111111111',os.getcwd()) 
    os.chdir('../w')
    print('22222222',os.getcwd()) 
    CheckIn.run_git_commands(version, git_branch)
    os.chdir('../wpublish')
    logging.info('done')
