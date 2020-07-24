#!/usr/bin/env python3
from datetime import datetime
from os import listdir
from os import mkdir
from os import path
from shutil import copy
from subprocess import Popen, PIPE
from sys import exit
from tkinter import messagebox
from tkinter import simpledialog
import os
import re
import tkinter as tk
import traceback

LOG_FILE = path.basename(__file__) + '.log'
msg = ''

def log(*args):
  global LOG_FILE
  with open(LOG_FILE, 'a') as f:
    f.write('\n')
    for arg in args:
       f.write(' '+str(arg))


def update_version_and_contents(file_paths):
  with open('help.html') as f:
    lines = f.read().splitlines()
    
  version= 'update'
  for line in lines:
    if line.startswith('<p style="font-size:12px;">'):
      # for example: line = '2020-05-10; links',  version= 'links' 
      version = line.split(';')[1].strip()
      break
        
  root = tk.Tk()
  root.withdraw()
  version = simpledialog.askstring(title="Git check-in;  "+ __file__, prompt=
                               ("\nUdate 'Search contents' related files and check into git.   "
                               "\nThis may take a while."
                               "\n\nVersion name:"), 
                               initialvalue=version)
  if version is None:
    exit()
  with open('help.html', 'w') as f:
    for line in lines:
      print('---', line)
      if line.startswith('<br><br>'):
        f.write(line+'\n')
        append_version_and_content_links(version, file_paths, f)
        break
      f.write(line+'\n')
  global msg
  msg += '\nversion: ' + version
  return version

def append_version_and_content_links(version, file_paths, f):
  dt = datetime.now().isoformat()[:10]
  print(dt)
  print(version)
  lines = get_contents_file_list(file_paths)
  lines += '\n<br><p style="font-size:12px;">'+ dt + ';  ' + version
  f.write(lines)

def get_contents_file_list(file_paths):
  file_paths.sort(key = lambda x: x[1], reverse = True)  # sort by ;ast modified TS
  lines = '<table>'
  lines += add_table_rows(file_paths, 'science')
  lines += add_table_rows(file_paths, 'arts')
  lines += add_table_rows(file_paths, 'recipes')
  lines += add_table_rows(file_paths, 'tech')
  lines += '</table>'
  return lines;


def add_table_rows(file_paths, topic):
  i = 0
  lines = ''
  label = topic + '/'
  for p in file_paths:
    if label in p[0]:
      i += 1
      dt = datetime.utcfromtimestamp(p[1]).strftime('%Y-%m-%d')
      link = create_link(p[0])
      if i == 1:
        lines += f"<tr><td>{topic}</td> <td>{link}</td> <td>{dt}</td><tr>\n"
      else:
        lines += f"<tr><td></td> <td>{link}</td> <td>{dt}</td><tr>\n"
      dt_previous = dt
  return lines

def create_link(file_path):
  i_start = file_path.index('/')+1
  i_end = file_path.rindex('.html')
  file_name = file_path[i_start:i_end].replace('-', ' ')
  link = '<a href="./' + file_path + '">' + file_name + '</a>'
  return link
 
def save_searcn_file_paths(save_file):
  file_paths = []  
  for f1 in os.listdir("."):
    if path.isdir(f1):
      for f2 in os.listdir(f1):
        p = f1+'/'+f2
        log(p)
        if path.isfile(p) and not p.endswith('.log') and "test" not in p and \
                    "js/" not in p and "pycache" not in p and ".tmp" not in p:
          file_paths.append((p, os.path.getmtime(p)))
  file_paths.sort(key=lambda x: x[0])
  log('file_paths= ', file_paths)
  with open(save_file, 'w') as f:
    f.writelines('/'+ x[0] +'\n' for x in file_paths)
  log('Updated '+ save_file)
  global msg
  msg += '\nSaved search file paths in: ' + save_file
  return file_paths


def save_search_labels(file_paths, save_file):
  with open(save_file, 'w') as f:
    f.write('')
  is_first = True
  for i, x in enumerate(file_paths):
    if 'problem' in x[0]:
      continue
    log(x[0])
    indexes = contents_indexes(x[0])
    if len(indexes) > 0:
      with open(save_file, 'a') as f:
        for atrs in indexes:
          if not is_first:
            f.write('\n')
          else:
            is_first = False
          f.write(atrs[0]) # anchor label or table header
          f.write('$$')
          f.write(str(i))  # file index number
          if len(atrs) > 1:
            f.write('$$')
            f.write(atrs[1]) # url
  log('save_file= ', save_file)
  global msg
  msg += '\nSaved search labels to: ' + save_file


def contents_indexes(file_path):
  with open(file_path) as f:
    lines = f.readlines()
  indexes = []
  for line in lines:
    # search for anchors:
    i = line.find('<a ')
    if i > -1:
      if '</a>' not in line:
        print('ERR mising </a> in: ' + line + 'ERR file_path = ' + file_path)
      ii = line.index('</a>',i) + 4
      link = line[i:ii]
      label_url = extract_url_label(link)
      indexes.append(label_url)
    # search for italic keywords:
    i = line.find('<i>')
    if i > -1:
      labels = extract_italicized_labels(line)
      indexes.append((labels,))
  return indexes

def extract_italicized_labels(line):
  """
  >>> extract_italicized_labels('aa <i>AAA</i> bbb <i>BBB</i> xxx<i>222</i>yyy<i>333</i>zzz')
  'aaa bbb 222 333'
  """
  s = re.sub("^(.*?)<i>", "", line)
  s = re.sub("</i>.*?<i>", " ", s)
  s = re.sub("</i>.*", "", s).strip().lower()
  return s
  
def extract_url_label(link):
  """
  >>> extract_url_label('<a href="https://www.coursera.org/">Coursera- Free course</a>')
  ('coursera- free course', 'https://www.coursera.org/')
  >>> extract_url_label("<a href='https://www.coursera.org/'>Coursera- Free course</a>")
  ('coursera- free course', 'https://www.coursera.org/')
  """
  link=link.replace('href= ','href=')
  quote =  '"' if link.find('href="')>-1  else "'"
  i = link.index('href=' + quote) + 6
  i2 = link.index(quote, i) 
  url = link[i:i2]
  i = link.index('>', i2) + 1
  i2 = link.index('</a>', i) 
  label = link[i:i2].lower().strip()
  attrs = (label, url) 
  return attrs
  
def run(*args: str):
    global msg
    msg += '\n'+str(args)
    print('cmd:', args)
    log('cmd:', args)

    p = Popen(args, shell=False, stdout=PIPE, stderr=PIPE)
    o, e = p.communicate()
    output = o.decode("utf-8").replace('\r', '')
    errs = e.decode("utf-8").replace('\r', '')

    if len(output) > 0:
        log('output: ', output)
        print(output)
        if 'FAILURES' in output:
            messagebox.showinfo("FAILURES", msg +
                 '\nMay have intermittent tkinter venv failure.\nTry rerunning')
            exit(1)
    if len(errs) > 0:
        log('errs: ', errs)
        print(errs)
        if 'Everything up-to-date' in errs:
            messagebox.showinfo("Git done", msg +'\nCode checked in')
            exit(0)
        label = 15 * 'ERR---' if 'br1 -> br1' not in str(errs) else ''
        log(label)
        print(label)
        if 'ERR---' in label:
            messagebox.showinfo("ERR", msg +'\n'+lavel)
            exit(2)

if __name__ == '__main__x':
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    msg = ''
    try:
      file_paths = save_searcn_file_paths('search_file_paths.txt')
      version = update_version_and_contents(file_paths)
      with open(LOG_FILE, 'w') as f:
        f.write(str(datetime.now()))
      save_search_labels(file_paths, 'search_labels.txt')
      run('git', 'add', '*')
      run('git', 'status')
      run('git', 'commit', '-m', "'" + version + "'")
      run('git', 'push', 'origin', 'br1')
      run('git', 'diff')

      archive_dir = './logs-check-ins'
      if not path.isdir(archive_dir):
          mkdir(archive_dir)
      log_archive_file = archive_dir + '/' + path.basename(__file__) + '-' + \
                         str(datetime.now()).replace(':', '-') + '.log'
      copy(LOG_FILE, log_archive_file)
      log('done')
      messagebox.showinfo(__file__, msg +'\ndone')
    except Exception as e:
      print(traceback.format_exc())
      messagebox.showinfo(__file__, os.path.basename(__file__) + ' FAILED; \n\n' + \
           str(e)  + '\n\nSee trace in: ' + LOG_FILE)
      log(traceback.format_exc())
