#!/usr/bin/env python3
from datetime import datetime
from os import mkdir
from os import path
from os import listdir
import os
from datetime import datetime
from shutil import copy
from subprocess import Popen, PIPE
from sys import exit
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import traceback

LOG_FILE = path.basename(__file__) + '.log'
msg = ''

def log(*args):
  global LOG_FILE
  with open(LOG_FILE, 'a') as f:
    f.write('\n')
    for arg in args:
       f.write(' '+str(arg))


def update_version_info():
  with open('help.html') as f:
    lines = f.read().splitlines()
    
  ver= 'update]'
  for line in lines:
    if line.startswith('20'):
        ver = line.split(';')[1].strip()
        
  root = tk.Tk()
  root.withdraw()
  ver = simpledialog.askstring(title="Git check-in;  "+ __file__, prompt=
                               ("\nUdate 'Search contents' related files and check into git.   "
                               "\nThis will take a while."
                               "\n\nVersion name:"), 
                               initialvalue=ver)
  if ver is None:
    ver = 'update'
  print(ver)
  with open('help.html', 'w') as f:
    for line in lines:
      if line.startswith('20'):
        dt = datetime.now().isoformat()[:10]
        line = dt + ';  ' + ver
      f.write(line+'\n')
  global msg
  msg += '\nversion: ' + ver
  return ver
  
file_paths = [] 

def save_searcn_file_paths(save_file):
  global file_paths 
  for f1 in os.listdir("."):
    if path.isdir(f1):
      for f2 in os.listdir(f1):
        p = f1+'/'+f2
        log(p)
        if path.isfile(p) and not p.endswith('.log') and "test" not in p and \
                    "js/" not in p and "pycache" not in p and ".tmp" not in p:
          file_paths.append(p)
  file_paths.sort()
  log('file_paths= ', file_paths)
  with open(save_file, 'w') as f:
    f.writelines('/'+ p+'\n' for p in file_paths)
  log('Updated '+ save_file)
  global msg
  msg += '\nSaved search file paths in: ' + save_file


def save_search_labels(save_file):
  with open(save_file, 'w') as f:
    f.write('')
  global file_paths
  is_first = True
  for i, p in enumerate(file_paths):
    if 'problem' in p:
      continue
    log(p)
    links = collect_links(p)
    if len(links) > 0:
      with open(save_file, 'a') as f:
        for atrs in links:
          if not is_first:
            f.write('\n')
          else:
            is_first = False
          print(atrs[0])
          f.write(atrs[0]) # anchor label
          f.write('$$')
          f.write(str(i))  # file index number
          f.write('$$')
          f.write(atrs[1]) # url
  log('save_file= ', save_file)
  global msg
  msg += '\nSaved search labels to: ' + save_file


def collect_links(file_path):
  with open(file_path) as f:
    lines = f.readlines()
  labels_urls = []
  for line in lines:
    i = line.find('<a ')
    print(line)
    if i > -1:
      ii = line.index('</a>',i) + 4
      link = line[i:ii]
      label_url = extract_url_label(link)
      labels_urls.append(label_url)
  return labels_urls

def extract_url_label(link):
  
  
  """
  >>> extract_url_label('<a href="https://www.coursera.org/">Coursera- Free course</a>')
  ('Coursera- Free course', 'https://www.coursera.org/')
  >>> extract_url_label("<a href='https://www.coursera.org/'>Coursera- Free course</a>")
  ('Coursera- Free course', 'https://www.coursera.org/')
  """
  link=link.replace('href= ','href=')
  quote =  '"' if link.find('href="')>-1  else "'"
  i = link.index('href=' + quote) + 6
  i2 = link.index(quote, i) 
  url = link[i:i2]
  i = link.index('>', i2) + 1
  i2 = link.index('</a>', i) 
  label = link[i:i2].lower()
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

if __name__ == '__main__22':
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    msg = ''
    try:
      ver = update_version_info()
      with open(LOG_FILE, 'w') as f:
        f.write(str(datetime.now()))
      save_searcn_file_paths('search_file_paths.txt')
      save_search_labels('search_labels.txt')
      run('git', 'add', '*')
      run('git', 'status')
      run('git', 'commit', '-m', "'" + ver + "'")
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
      messagebox.showinfo(__file__, os.path.basename(__file__) + ' FAILED; \n\n' + str(e))
