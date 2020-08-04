#!/usr/bin/env python3
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import os
import sys
import traceback
import pychin.update_and_checkin




def check():
  pass

def test_save_searcn_file_paths():
  pychin.update_and_checkin.msg = ''
  file_paths = pychin.update_and_checkin.save_search_file_paths('search_files_paths__t.txt')
  actual = pychin.update_and_checkin.msg
  expected = '\nSaved search file paths in: search_files_paths__t.txt'
  assert actual == expected, 'save_searcn_file_paths() failed; actual:\n' + actual + '\nexpected:\n' + expected
  
  with open ('search_files_paths__t.txt') as f:
    actual = f.read()
  expected = """/search-files/links-2.html
/search-files/links.html
/search-files/problems-examples.html
/search-files/problems-solutions.html
/search-files/recipe.html
"""
  assert expected == actual, 'save_searcn_file_paths() failed; actual:\n' + actual + '\nexpected:\n' + expected

def test_contents_indexes():
  actual = pychin.update_and_checkin.contents_indexes('../tests/search-files/links.html')
  expected = [('internet archive', 'https://archive.org'),
         ('free books', 'https://www.freebookcentre.net/'), 
         ('coursera- free course', 'https://www.coursera.org/'), 
         ('edx - mit, harvard', 'https://www.edx.org/')]
  assert expected == actual, 'contents_indexes() failed; expected:\n' + str(expected) + '\nactual:\n' +str(actual)
  
  actual = pychin.update_and_checkin.contents_indexes('../tests/search-files/recipe.html')
  expected = [('serve done',),]
  assert expected == actual, 'contents_indexes() failed; expected:\n' + str(expected) + '\nactual:\n' +str(actual)


def test_save_search_labels(file_paths):
  pychin.update_and_checkin.msg = ''
  #make_file_paths_relative()
  pychin.update_and_checkin.save_search_labels(file_paths, 'search_labels__t.txt')
  expected = '\nSaved search labels to: search_labels__t.txt'
  actual = pychin.update_and_checkin.msg
  assert pychin.update_and_checkin.msg == expected, 'test_save_search_labels() failed; actual:\n' + actual + '\nexpected:\n' + expected
  
  with open ('search_labels__t.txt') as f:
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


def make_file_paths_sever_testable():
  with open ('search_files_paths__t.txt') as f:
    lines = f.readlines()
  with open ('search_files_paths__t.txt', 'w') as f:
    [f.write('/tests'+x) for x in lines]


def test_get_contents_file_list(file_paths):
  expected = """search-files/links-2.html
search-files/links.html
search-files/problems-examples.html
search-files/problems-solutions.html
search-files/recipe.html"""   # sorted
  actual = [x[0] for x in file_paths]
  actual = '\n'.join(actual)
  assert expected == actual, 'make_file_paths_sever_testable() failed: actual:\n' + actual + '\nexpected:\n' + expected

  paths = pychin.update_and_checkin.get_contents_file_list(file_paths)
   #assert expected == actual, 'test_get_contents() failed, expected:\n' + expected + '\nactual:\n' + actual


def main():
  sys.path.insert(1, '../')
  import pychin.update_and_checkin

  try:
    #os.remove('update_and_checkin.py.log')
    test_save_searcn_file_paths()
    file_paths = """/search-files/links-2.html
/search-files/links.html
/search-files/problems-examples.html
/search-files/problems-solutions.html
/search-files/recipe.html
"""
    test_contents_indexes()
    test_save_search_labels(file_paths)
    test_get_contents_file_list(file_paths)
    make_file_paths_sever_testable()
  except Exception as e:
    print(traceback.format_exc())
    messagebox.showinfo(__file__, 'Test(s) FAILED; \n\n' + str(e))
  else:
    messagebox.showinfo(__file__, 'Tests suceesfull')

if __name__ == '__main__':
  main()
