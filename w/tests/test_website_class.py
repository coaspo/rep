import os

from pi.website import WebSite
from shutil import copyfile

def make_paths_usable_by_local_server():
    copyfile('./tests/search_files_paths__t.txt', 'search_files_paths.txt')
    copyfile('./tests/search_labels__t.txt', 'search_labels.txt')

def test_save_search_file_paths():
    if os.getcwd().endswith('/tests'):
        os.chdir('..')
    print(99999999, os.getcwd())
    target_dirs = ('./tests/search-files',)
    website = WebSite(target_dirs)

    if os.path.exists("./tests/search_files_paths__t.txt"):
        os.remove("./tests/search_files_paths__t.txt")
    website.save_search_file_paths('./tests/search_files_paths__t.txt')
    with open('./tests/search_files_paths__t.txt') as f:
        actual = f.read()
    expected = """tests/search-files/links-2.html
tests/search-files/links.html
tests/search-files/problems-examples.html
tests/search-files/problems-solutions.html
tests/search-files/recipe.html
"""
    assert expected == actual, 'save_searcn_file_paths() failed; actual:\n' + actual + '\nexpected:\n' + expected


def test_save_search_labels():
    if os.getcwd().endswith('/tests'):
        os.chdir('..')
    target_dirs = ('./tests/search-files',)
    website = WebSite(target_dirs)
    website.save_search_labels('./tests/search_labels__t.txt')

    with open('./tests/search_labels__t.txt') as f:
        actual = f.read()
    expected = """wolfram$$0$$https://www.wolfram.com/
worldometers$$0$$https://www.worldometers.info/
week in virology$$0$$https://www.microbe.tv/twiv/archive/
internet archive$$1$$https://archive.org
free books$$1$$https://www.freebookcentre.net/
coursera- free course$$1$$https://www.coursera.org/
edx - mit, harvard$$1$$https://www.edx.org/
serve done$$4"""  # anchor label, file index, url
    assert expected == actual, 'save_search_labels() failed: actual:\n' + actual + '\nexpected:\n' + expected

    make_paths_usable_by_local_server()
