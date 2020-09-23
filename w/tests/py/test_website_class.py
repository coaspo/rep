import os

from pi.website import WebSite
from shutil import copyfile

def make_paths_usable_by_local_server():
    copyfile('./tests/search_file_paths__t.txt', 'search_file_paths.txt')
    copyfile('./tests/search_labels__t.txt', 'search_labels.txt')

def test_website():
    if os.getcwd().endswith('/py'):
        os.chdir('..')
    if os.getcwd().endswith('/tests'):
        os.chdir('..')
    target_dirs = ('./tests/search-files',)
    website = WebSite(target_dirs)

    if os.path.exists("./tests/search_file_paths__t.txt"):
        os.remove("./tests/search_file_paths__t.txt")
    website.save_search_file_paths('./tests/search_file_paths__t.txt')
    with open('./tests/search_file_paths__t.txt') as f:
        actual = f.read()
    expected = """tests/search-files/category/words.html
tests/search-files/links-2.html
tests/search-files/links.html
tests/search-files/problems-examples.html
tests/search-files/problems-solutions.html
tests/search-files/recipe.html
"""
    assert expected == actual, 'save_searcn_file_paths() failed; actual:\n' + actual + '\nexpected:\n' + expected


    if os.path.exists("./tests/search_labels__t.txt"):
        os.remove("./tests/search_labels__t.txt")
    website.save_search_labels('./tests/search_labels__t.txt')

    with open('./tests/search_labels__t.txt') as f:
        actual = f.read()
    expected = """wolfram$$1$$https://www.wolfram.com/
worldometers$$1$$https://www.worldometers.info/
week in virology$$1$$https://www.microbe.tv/twiv/archive/
internet archive$$2$$https://archive.org
free books$$2$$https://www.freebookcentre.net/
coursera- free course$$2$$https://www.coursera.org/
edx - mit, harvard$$2$$https://www.edx.org/
pizza$$5
serve done$$5"""  # anchor label, file index, url
    assert expected == actual, 'save_search_labels() failed: actual:\n' + actual + '\nexpected:\n' + expected

    actual = len(website.web_pages)
    expected = 6
    assert expected == actual, 'save_search_labels() failed: actual:\n' + str(actual) + '\nexpected:\n' + str(expected)
    make_paths_usable_by_local_server()
