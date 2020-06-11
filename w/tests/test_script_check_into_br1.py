#!/usr/bin/env python3
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import os
import sys
import traceback


def test_save_searcn_file_paths():
  check_into_br1.msg = ''
  check_into_br1.save_searcn_file_paths('files_paths__t.txt')
  assert check_into_br1.msg == '\nSaved search file paths in: files_paths__t.txt', 'save_searcn_file_paths() failed\n' + check_into_br1.msg
  with open ('files_paths__t.txt') as f:
    txt = f.read()
  expected = """search-files/links-2.html
search-files/links.html
search-files/problems-examples.html
search-files/problems-solutions.html
search-files/recipe.html
"""
  assert expected == txt, 'save_searcn_file_paths() failed; expected:\n' + expected + '\nactual:\n' + txt


def test_collect_labels_urls():
  labels_urls = check_into_br1.collect_labels_urls('../tests/search-files/links.html')
  expected = [('Internet archive', 'https://archive.org'),
         ('Free books', 'https://www.freebookcentre.net/'), 
         ('Coursera- Free course', 'https://www.coursera.org/'), 
         ('edX - MIT, Harvard', 'https://www.edx.org/')]
  assert expected == labels_urls, 'collect_labels_urls() failed; expected:\n' + expected + '\nactual:\n' +links


def test_save_search_labels():
  check_into_br1.msg = ''
  #make_file_paths_relative()
  check_into_br1.save_search_labels('search_labels__t.txt')
  assert check_into_br1.msg == '\nSaved search labels to: search_labels__t.txt', 'save_links() failed\n' + check_into_br1.msg
  with open ('search_labels__t.txt') as f:
    txt = f.read()
  expected = """Wolfram$$https://www.wolfram.com/$$0
worldometers$$https://www.worldometers.info/$$0
Week in virology$$https://www.microbe.tv/twiv/archive/$$0
Internet archive$$https://archive.org$$1
Free books$$https://www.freebookcentre.net/$$1
Coursera- Free course$$https://www.coursera.org/$$1
edX - MIT, Harvard$$https://www.edx.org/$$1"""

  assert expected == txt, 'save_search_labels() failed; count expected:\n' + expected + '\nactual:\n' + txt


def make_file_paths_sever_testable():
  with open ('files_paths__t.txt') as f:
    lines = f.readlines()
  with open ('files_paths__t.txt', 'w') as f:
    f.write(''.join(lines))


if __name__ == '__main__':
  sys.path.insert(1, '../')
  import check_into_br1

  try:
    os.remove('check_into_br1.py.log')
    test_save_searcn_file_paths()
    test_collect_labels_urls()
    test_save_search_labels()
    make_file_paths_sever_testable()
  except Exception as e:
    messagebox.showinfo(__file__, 'Test(s) FAILED; \n\n' + str(e))
  else:
    messagebox.showinfo(__file__, 'Tests suceesfull')

