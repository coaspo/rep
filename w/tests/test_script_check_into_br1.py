#!/usr/bin/env python3
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import os
import sys
import traceback


def test_save_searcn_file_paths():
  check_into_br1.msg = ''
  check_into_br1.save_searcn_file_paths('search_files_paths__t.txt')
  assert check_into_br1.msg == '\nSaved search file paths in: search_files_paths__t.txt', 'save_searcn_file_paths() failed\n' + check_into_br1.msg
  with open ('search_files_paths__t.txt') as f:
    txt = f.read()
  expected = """/search-files/links-2.html
/search-files/links.html
/search-files/problems-examples.html
/search-files/problems-solutions.html
/search-files/recipe.html
"""
  assert expected == txt, 'save_searcn_file_paths() failed; expected:\n' + expected + '\nactual:\n' + txt


def test_collect_links():
  labels_urls = check_into_br1.collect_links('../tests/search-files/links.html')
  expected = [('internet archive', 'https://archive.org'),
         ('free books', 'https://www.freebookcentre.net/'), 
         ('coursera- free course', 'https://www.coursera.org/'), 
         ('edx - mit, harvard', 'https://www.edx.org/')]
  assert expected == labels_urls, 'collect_links() failed; expected:\n' + str(expected) + '\nactual:\n' +str(labels_urls)


def test_save_search_labels():
  check_into_br1.msg = ''
  #make_file_paths_relative()
  check_into_br1.save_search_labels('search_labels__t.txt')
  assert check_into_br1.msg == '\nSaved search labels to: search_labels__t.txt', 'save_links() failed\n' + check_into_br1.msg
  with open ('search_labels__t.txt') as f:
    txt = f.read()
  expected = """wolfram$$0$$https://www.wolfram.com/
worldometers$$0$$https://www.worldometers.info/
week in virology$$0$$https://www.microbe.tv/twiv/archive/
internet archive$$1$$https://archive.org
free books$$1$$https://www.freebookcentre.net/
coursera- free course$$1$$https://www.coursera.org/
edx - mit, harvard$$1$$https://www.edx.org/"""  # anchor label, file index, url
  assert expected == txt, 'save_search_labels() failed:\n' + expected + '\nactual:\n' + txt


def make_file_paths_sever_testable():
  with open ('search_files_paths__t.txt') as f:
    lines = f.readlines()
  with open ('search_files_paths__t.txt', 'w') as f:
    [f.write('/tests'+x) for x in lines]



if __name__ == '__main__':
  sys.path.insert(1, '../')
  import check_into_br1

  try:
    os.remove('check_into_br1.py.log')
    test_save_searcn_file_paths()
    test_collect_links()
    test_save_search_labels()
    make_file_paths_sever_testable()
  except Exception as e:
    print(traceback.format_exc())
    messagebox.showinfo(__file__, 'Test(s) FAILED; \n\n' + str(e))
  else:
    messagebox.showinfo(__file__, 'Tests suceesfull')

