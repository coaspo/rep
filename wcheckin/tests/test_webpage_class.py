import os

from wpy.webpage import WebPage


def test_webpage():
    if os.getcwd().endswith('/tests'):
        os.chdir('..')
    page = WebPage('../w/tests/search-files/links.html')
    actual = page.search_indexes
    expected = [('internet archive', 'https://archive.org'),
                ('free books', 'https://www.freebookcentre.net/'),
                ('coursera- free course', 'https://www.coursera.org/'),
                ('edx - mit, harvard', 'https://www.edx.org/')]
    assert expected == actual, 'contents_indexes() failed; expected:\n' + str(expected) + '\nactual:\n' + str(actual)

    page = WebPage('../w/tests/search-files/links.html')
    actual = page.file_path
    expected = '../w/tests/search-files/links.html'
    assert expected == actual, 'invalid file_path; expected:\n' + expected + '\nactual:\n' + actual

    actual = page.link
    expected = "<a href='./../w/tests/search-files/links.html'>links</a>"
    assert expected == actual, 'invalid search_indexes; expected:\n' + expected + '\nactual:\n' + actual

    actual = page.modification_date
    expected = '2021-01-07'
    assert expected == actual, 'invalid modification_date; expected:\n' + expected + '\nactual:\n' + actual

    actual = page.content_line_count
    expected = 7
    assert expected == actual, 'invalid num_of_lines; expected:\n' + str(expected) + '\nactual:\n' + str(actual)

    actual = page.topic
    expected = 'tests'
    assert expected == actual, 'invalid search_indexes; expected:\n' + expected + '\nactual:\n' + str(actual)

    actual = page.sub_topic
    expected = 'search-files'
    assert expected == actual, 'invalid search_indexes; expected:\n' + expected + '\nactual:\n' + str(actual)

    page = WebPage('../w/tests/search-files/category/word_list.html')
    actual = page.link
    expected = "<a href='./../w/tests/search-files/category/word_list.html'>word list</a>"
    assert expected == actual, 'invalid search_indexes; expected:\n' + expected + '\nactual:\n' + actual

    actual = page.sub_topic
    expected = 'search-files'
    assert expected == actual, 'invalid search_indexes; expected:\n' + expected + '\nactual:\n' + str(actual)

    actual = page.description
    expected = "This is a test"
    assert expected == actual, 'invalid search_indexes; expected:\n' + expected + '\nactual:\n' + actual
    print (page)
