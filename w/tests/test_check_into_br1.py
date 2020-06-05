#!/usr/bin/env python3
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox


def test_collect_links():
  links = check_into_br1.collect_links('../tests/search-files/links.html')
  expected = '<a href="https://archive.org">Internet archive</a>##'\
             '<a href="https://www.freebookcentre.net/">Free books</a>##'\
             '<a href="https://www.coursera.org/">Coursera- Free course</a>##'\
             '<a href="https://www.edx.org/">edX - MIT, Harvard</a>'
  assert expected == links, 'collect_links() failed; expected, actual\n' + expected + '\n' +links


def test_save_links():
  check_into_br1.msg = ''
  check_into_br1.save_links('a.tmp')
  assert check_into_br1.msg == '\nSaved link descs to: a.tmp', 'save_links() failed\n' + check_into_br1.msg
  with open ('a.tmp') as f:
    lines = f.readlines()
  assert 2 == len(lines), 'save_links() failed; count expected/actual: 2/' + len(links)


if __name__ == '__main__':
  import sys
  sys.path.insert(1, '../')
  import check_into_br1

  test_collect_links()
  test_save_links()
