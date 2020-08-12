#!/usr/bin/env python3
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import os
import sys
import traceback
import pi.update_and_checkin




def check():
  pass

def test_save_search_file_paths(target_dirs):
  pi.update_and_checkin.msg = ''
  file_paths = pi.update_and_checkin.get_search_file_paths(target_dirs)
  pi.update_and_checkin.save_search_file_paths('tests/search_files_paths__t.txt', file_paths)
  actual = pi.update_and_checkin.msg
  expected = '\nSaved search file paths in: tests/search_files_paths__t.txt'
  assert actual == expected, 'save_search_file_paths() failed; actual:\n' + actual + '\nexpected:\n' + expected
  
  with open ('tests/search_files_paths__t.txt') as f:
    actual = f.read()
  expected = """/tests/search-files/links-2.html
/tests/search-files/links.html
/tests/search-files/problems-examples.html
/tests/search-files/problems-solutions.html
/tests/search-files/recipe.html
"""
  assert expected == actual, 'save_searcn_file_paths() failed; actual:\n' + actual + '\nexpected:\n' + expected

def test_save_search_labels(file_paths):
  pi.update_and_checkin.msg = ''
  #make_file_paths_relative()
  pi.update_and_checkin.save_search_labels('tests/search_labels__t.txt', file_paths)
  expected = '\nSaved search labels to: tests/search_labels__t.txt'
  actual = pi.update_and_checkin.msg
  assert pi.update_and_checkin.msg == expected, 'test_save_search_labels() failed; actual:\n' + actual + '\nexpected:\n' + expected
  
  with open ('tests/search_labels__t.txt') as f:
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
  with open ('tests/search_files_paths__t.txt') as f:
    lines = f.readlines()
  with open ('tests/search_files_paths__t.txt', 'w') as f:
    [f.write(''+x) for x in lines]


def test_get_contents_file_list(file_paths):
  expected = """tests/search-files/links-2.html
tests/search-files/links.html
tests/search-files/problems-examples.html
tests/search-files/problems-solutions.html
tests/search-files/recipe.html"""   # sorted
  actual = [x[0] for x in file_paths]
  actual = '\n'.join(actual)
  assert expected == actual, 'make_file_paths_sever_testable() failed: actual:\n' + actual + '\nexpected:\n' + expected

  paths = pi.update_and_checkin.get_contents_file_list(file_paths)
   #assert expected == actual, 'test_get_contents() failed, expected:\n' + expected + '\nactual:\n' + actual


def main():
  sys.path.insert(1, '../')
  import pi.update_and_checkin

  try:
    #os.remove('update_and_checkin.pi.log')
    target_dirs = ('./tests/search',)
    test_save_search_file_paths(target_dirs)
    test_contents_indexes()
    file_paths = pi.update_and_checkin.get_search_file_paths(target_dirs)
    test_save_search_labels(file_paths)
    test_get_contents_file_list(file_paths)
    make_file_paths_sever_testable()
  except Exception as e:
    print(traceback.format_exc())
    messagebox.showinfo(__file__, 'Test(s) FAILED; \n\n' + str(e))
  else:
    messagebox.showinfo(__file__, 'Tests suceesfull')

