import os

from pi.webpage import WebPage


def test_webpage():
    if os.getcwd().endswith('/py'):
        os.chdir('..')
    if os.getcwd().endswith('/tests'):
        os.chdir('..')
    page = WebPage('tests/search-files/links.html')
    actual = page.search_indexes
    expected = [('internet archive', 'https://archive.org'),
                ('free books', 'https://www.freebookcentre.net/'),
                ('coursera- free course', 'https://www.coursera.org/'),
                ('edx - mit, harvard', 'https://www.edx.org/')]
    assert expected == actual, 'contents_indexes() failed; expected:\n' + str(expected) + '\nactual:\n' + str(actual)

    page = WebPage('tests/search-files/recipe.html')
    actual = page.file_path
    expected = 'tests/search-files/recipe.html'
    assert expected == actual, 'invalid file_path; expected:\n' + expected + '\nactual:\n' + actual

    actual = page.modification_date
    expected = '2020-11-13'
    assert expected == actual, 'invalid modification_date; expected:\n' + expected + '\nactual:\n' + actual

    actual = page.content_line_count
    expected = 5
    assert expected == actual, 'invalid num_of_lines; expected:\n' + str(expected) + '\nactual:\n' + str(actual)

    actual = page.search_indexes
    expected = [('pizza',), ('serve done',)]
    assert expected == actual, 'invalid search_indexes; expected:\n' + str(expected) + '\nactual:\n' + str(actual)

    actual = page.link
    expected = "<a href='./tests/search-files/recipe.html'>recipe</a>"
    assert expected == actual, 'invalid search_indexes; expected:\n' + expected + '\nactual:\n' + actual

    actual = page.description
    print('------actual=', actual)
    expected = "This is a description"
    assert expected == actual, 'invalid search_indexes; expected:\n' + expected + '\nactual:\n' + actual

