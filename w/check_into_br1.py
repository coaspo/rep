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

SCRIPT_NAME = path.basename(__file__)
LOG_FILE = SCRIPT_NAME + '.log'
msg = ''

def log(*args):
  with open(LOG_FILE, 'a') as f:
    f.write('\n')
    for arg in args:
       f.write(' '+str(arg))


def update_version_info():
  with open('help.html') as f:
    lines = f.read().splitlines()
    
  ver = 'update'
  for line in lines:
    if line.startswith('20'):
        ver = line.split(';')[1].strip()
        
  root = tk.Tk()
  root.withdraw()
  ver = simpledialog.askstring(title="Git check-in;  "+ __file__,
                               prompt=(' '*100)+"\nVersion name:",
                               initialvalue=ver)
  
  with open('help.html', 'w') as f:
    for line in lines:
      if line.startswith('20'):
        dt = datetime.now().isoformat()[:10]
        line = dt + ';  ' + ver
      f.write(line+'\n')
  global msg
  msg += '\nversion: ' + ver
  return ver

def save_searcn_file_paths(save_file):
  file_paths = [] 
  for f1 in os.listdir("."):
    if path.isdir(f1):
      for f2 in os.listdir(f1):
        p = './'+f1+'/'+f2
        log(p)
        if path.isfile(p) and not p.endswith('.log') and "test" not in p and "/js/" not in p:
          file_paths.append(p[1:])
  log('file_paths= ', file_paths)
  with open(save_file, 'w') as f:
    f.writelines(p+'\n' for p in file_paths)
  log('Updated '+ save_file)
  global msg
  msg += '\nUpdated ' + save_file


def save_links(save_file):
  with open(save_file, 'w') as f:
    f.write('')
  for f1 in os.listdir("."):
    if path.isdir(f1):
      for f2 in os.listdir(f1):
        p = './'+f1+'/'+f2
        if path.isfile(p) and not (p.endswith('.log') or "test" in p 
           or "/js/" in p or 'pycache' in p or 'problem' in p):
          log(p)
          links = collect_links(p)
          if len(links) > 0:
            with open(save_file, 'a') as f:
              f.write(links)
              f.write('$$')
              f.write(p[2:])
              f.write('\n')
  log('save_file= ', save_file)
  global msg
  msg += '\nSaved link descs to: ' + save_file


def collect_links(file_path):
  with open(file_path) as f:
    lines = f.readlines()
  links = []
  for line in lines:
    i = line.find('<a ')
    if i > -1:
      ii = line.index('</a>',i) + 4
      links.append(line[i:ii])
  return '##'.join(links)


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
            messagebox.showinfo("FAILURES", msg +'\nMay have intermittent tkinter venv failure.\nTry rerunning')
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


if __name__ == '__main__':
    msg = ''
    ver = update_version_info()
    with open(LOG_FILE, 'w') as f:
      f.write(str(datetime.now()))
    save_searcn_file_paths('search_file_paths.txt')
    save_links('search_links.txt')
    run('git', 'add', '*')
    run('git', 'status')
    run('git', 'commit', '-m', "'" + ver + "'")
    run('git', 'push', 'origin', 'br1')
    run('git', 'diff')

    archive_dir = './logs-check-ins'
    if not path.isdir(archive_dir):
        mkdir(archive_dir)
    log_archive_file = archive_dir + '/' + SCRIPT_NAME + '-' + str(datetime.now()).replace(':', '-') + '.log'
    copy(LOG_FILE, log_archive_file)
    log('done')
    messagebox.showinfo(__file__, msg +'\ndone')
