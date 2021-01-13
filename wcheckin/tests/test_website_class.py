import os

from wpy.website import WebSite
from shutil import copyfile

def make_paths_usable_by_local_server():
    copyfile('tests/search_file_paths__t.txt', 'search_file_paths.txt')
    copyfile('tests/search_labels__t.txt', 'search_labels.txt')

def test_website():
    if os.getcwd().endswith('/tests'):
        os.chdir('..')
    target_dirs = ('./tests/w/topic1','./tests/w/topic2')
    website = WebSite(target_dirs)

    if os.path.exists("./tests/search_file_paths__t.txt"):
        os.remove("./tests/search_file_paths__t.txt")
    website.save_search_file_paths('./tests/search_file_paths__t.txt')
    with open('./tests/search_file_paths__t.txt') as f:
        actual = f.read()
    expected = """tests/search-files/category/word_list.html
tests/search-files/links-2.html
tests/search-files/links.html
tests/search-files/problems-examples.html
tests/search-files/problems-solutions.html
tests/search-files/recipe.html
tests/test_search.html
"""
    assert expected == actual, 'save_searcn_file_paths() failed;\n actual:\n' + actual + '\nexpected:\n' + expected


    if os.path.exists("./tests/search_labels__t.txt"):
        os.remove("./tests/search_labels__t.txt")
    website.save_search_labels('../w/tests/search_labels__t.txt')

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
serve done$$5
http://localhost:8080/w/tests/test_search.html$$6$$http://localhost:8080/w/tests/test_search.html
http://localhost:8080/w/index.html$$6$$http://localhost:8080/w/index.html
https://li.netlify.app/w/index.html$$6$$https://li.netlify.app/w/index.html
https://li.netlify.app/w/tests/test_search.html$$6$$https://li.netlify.app/w/tests/test_search.html"""  # anchor label, file index, url
    assert expected == actual, 'search_labels__t.txt failed:\n actual:\n' + actual + '\nexpected:\n' + expected

    actual = str(len(website.web_page_dict))
    expected = "1"
    assert expected == actual, 'len(website.web_pages) failed:\n actual:\n' + actual + '\nexpected:\n' + expected

    actual = str(website.topic_names)
    expected = "['tests']"
    assert expected == actual, 'website.topic_names failed:\n actual:\n' + actual + '\nexpected:\n' + expected

    actual = str(len(website.web_page_dict['tests']))  # num of web pages
    expected = "7"
    assert expected == actual, "len(website.web_pages['tests']) failed:\n actual:\n" + actual + "\nexpected:\n" + expected

    actual = str(website.web_page_dict['tests'][0])
    expected = "WebPage: file_path = ../w/tests/search-files/category/word_list.html, link = <a href='./../w/tests/search-files/category/word_list.html'>word list</a>,  modification_date = 2021-01-11, num_of_lines = 2,  search_indexes = [] topic = tests  sub_topic = search-files  description = This is a test"
    assert expected == str(actual), "website.topics['tests'][0] failed:\n actual:\n" + actual + "\nexpected:\n" + expected
