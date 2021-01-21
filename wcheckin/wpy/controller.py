#!/usr/bin/env python3
import logging
import os
from datetime import datetime

from wpy.util import Util
from wpy.contentspage import ContentsPage
from wpy.indexpage import IndexPage
from wpy.website import WebSite


def main(git_branch):
    Util.run_tests()
    version = update_index_and_contents_pages()
    check_in(version, git_branch)


def update_index_and_contents_pages():
    target_dirs = ('../w/tech', '../w/recipes', '../w/art', '../w/science')
    logging.info(str(datetime.now()))
    website = WebSite(target_dirs)
    website.save_search_file_paths('../w/search_file_paths.txt')
    website.save_search_labels('../w/search_labels.txt')
    IndexPage.update_links(website, '../w/index.html')
    version = ContentsPage.update(website, '../w/contents.html')
    return version


def check_in(version, git_branch):
    Util.check_into_repository(version, git_branch)
    os.chdir('../w')
    print('Current dir:', os.getcwd())
    Util.check_into_repository(version, git_branch)
    os.chdir('../wcheckin')
    logging.info('done')
