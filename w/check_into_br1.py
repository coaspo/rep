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

SCRIPT_NAME = path.basename(__file__)
LOG_FILE = SCRIPT_NAME + '.log'

def log(*args):
  with open(LOG_FILE, 'a') as f:
    f.write('\n')
    for arg in args:
       f.write(' '+str(arg))


def update_version_info():
  with open('help.html') as f:
    lines = f.read().splitlines()
  ver = 'update'
  with open('help.html', 'w') as f:
    for line in lines:
      if line.startswith('* '):
        ver = line.split(';')[1].strip()
        root = tk.Tk()
        root.withdraw()
        ver = simpledialog.askstring(title="Git check-in",prompt="Version name:",initialvalue=msg)
        dt = datetime.now().isoformat()[:10]
        line = '* ' + dt + ';  ' + ver
      f.write(line+'\n')
  return ver

def save_searcn_file_paths():
  file_paths = [] 
  for f1 in os.listdir("."):
    if path.isdir(f1):
      for f2 in os.listdir(f1):
        p = './'+f1+'/'+f2
        log(p)
        if path.isfile(p) and not p.endswith('.log') and "test" in p:
          file_paths.append(p[1:])
  log('file_paths= ', file_paths)
  with open('search_file_paths.txt', 'w') as f:
    f.writelines(p+'\n' for p in file_paths)
  log('Updated searcn_file_paths.txt')


def run(*args: str):
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
            print('May have intermittent tkinter venv failure. - try rerunning')
            exit(1)
    if len(errs) > 0:
        log('errs: ', errs)
        print(errs)
        if 'Everything up-to-date' in errs:
            exit(0)
        label = 15 * 'ERR---' if 'br1 -> br1' not in str(errs) else ''
        log(label)
        print(label)
        if 'ERR---' in label:
            exit(2)


if __name__ == '__main__':
    ver = update_version_info()
    with open(LOG_FILE, 'w') as f:
      f.write(str(datetime.now()))
    save_searcn_file_paths()
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
    print('done')
