import os
from tkinter import simpledialog

import mock

from wpy.contentspage import ContentsPage
from wpy.website import WebSite


def test_contents_page():
<<<<<<< HEAD
    if os.getcwd().endswith('/py'):
        os.chdir('..')
=======
>>>>>>> br1
    if os.getcwd().endswith('/tests'):
        os.chdir('..')
    target_dirs = ('../w/tests/search-files',)
    website = WebSite(target_dirs)
    simpledialog.askstring = mock.Mock(return_value="ver-1")
    ContentsPage.update(website.web_pages)

<<<<<<< HEAD
    with open('contents.html') as f:
=======
    with open('../w/contents.html') as f:
>>>>>>> br1
        source = f.read()
        assert "ver-1" in source, 'did not find "ver-1" in contents.html:\n' + source
