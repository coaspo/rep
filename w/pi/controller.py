#!/usr/bin/env python3
import logging
from datetime import datetime

from pi.checkin import CheckIn
from pi.contentspage import ContentsPage
from pi.indexpage import IndexPage
from pi.website import WebSite


def main(git_branch):
    target_dirs = ('./tech', './science', './recipes', './arts')
    logging.info(str(datetime.now()))
    website = WebSite(target_dirs)
    website.save_search_file_paths('search_file_paths.txt')
    website.save_search_labels('search_labels.txt')
    version = ContentsPage.update(website.web_pages)
    IndexPage.update_links(website.file_path_structures)
    CheckIn.run_git_commands(version, git_branch)
    logging.info('done')
