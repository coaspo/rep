import os
from tkinter import simpledialog

import mock

from pi.contentspage import ContentsPage
from pi.website import WebSite


def test_contents_page():
    if os.getcwd().endswith('/tests'):
        os.chdir('..')
    target_dirs = ('./tests/search-files',)
    website = WebSite(target_dirs)
    simpledialog.askstring = mock.Mock(return_value="ver-1")
    ContentsPage.update(website.web_pages)

    with open('contents.html') as f:
        source = f.read()
        assert "ver-1" in source, 'did not find "ver-1" in contents.html:\n' + source
