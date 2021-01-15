import os
from tkinter import simpledialog

import mock

from wpy.indexpage import IndexPage
from wpy.website import WebSite


def test_update_links():
    if os.getcwd().endswith('/tests'):
        os.chdir('..')
    target_dirs = ('tests/w/topic1', 'tests/w/topic2')
    website = WebSite(target_dirs)
    IndexPage.update_links(website, './tests/index.html')

    with open('./tests/index.html') as f:
        source = f.read()
        #assert "ver-1" in source, 'did not find "ver-1" in contents.html:\n' + source
