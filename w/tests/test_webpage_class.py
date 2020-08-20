from pi.webpage import WebPage


def test_search_indexes():
    page = WebPage('./tests/search-files/links.html')
    actual = page.search_indexes
    expected = [('internet archive', 'https://archive.org'),
                ('free books', 'https://www.freebookcentre.net/'),
                ('coursera- free course', 'https://www.coursera.org/'),
                ('edx - mit, harvard', 'https://www.edx.org/')]
    assert expected == actual, 'contents_indexes() failed; expected:\n' + str(expected) + '\nactual:\n' + str(actual)

    page = WebPage('./tests/search-files/recipe.html')
    actual = page.search_indexes
    expected = [('serve done',), ]
    assert expected == actual, 'contents_indexes() failed; expected:\n' + str(expected) + '\nactual:\n' + str(actual)
