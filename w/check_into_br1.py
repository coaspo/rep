#!/usr/bin/env python3
#!/bin/bash
from datetime import datetime
from os import mkdir
from os import path
from os import listdir
import os

from shutil import copy
from subprocess import Popen, PIPE
from sys import exit

SCRIPT_NAME = path.basename(__file__)
LOG_FILE = SCRIPT_NAME + '.log'

def log(arg):
  with open(LOG_FILE, 'a') as f:
    f.write('\n'+str(arg))



def save_searcn_file_paths():
  file_paths = [] 
  log(file_paths) 
  for f1 in os.listdir("."):
    log(f1)
    if path.isdir(f1):
      for f2 in os.listdir(f1):
        log(f2)
        p = './'+f1+'/'+f2
        if path.isfile(p) and not p.endswith('.log') and "test" in p:
          file_paths.append(p[1:])
  log('file_paths= '+str(file_paths))
  with open('search_file_paths.txt', 'w') as f:
    f.writelines(p+'\n' for p in file_paths)
  log('Updated searcn_file_paths.txt')


def run(*args: str):
    print('cmd:', args)
    log(str(args))

    p = Popen(args, shell=False, stdout=PIPE, stderr=PIPE)
    o, e = p.communicate()
    output = o.decode("utf-8").replace('\r', '')
    errs = e.decode("utf-8").replace('\r', '')

    if len(output) > 0:
        log('output:\n' + output)
        print(output)
        if 'FAILURES' in output:
            print('May have intermittent tkinter venv failure. - try rerunning')
            exit(1)
    if len(errs) > 0:
        log('errs:\n' + errs)
        print(errs)
        if 'Everything up-to-date' in errs:
            exit(0)
        label = 15 * 'ERR---' if 'br1 -> br1' not in str(errs) else ''
        log(label)
        print(label)
        if 'ERR---' in label:
            exit(2)


if __name__ == '__main__':
    with open(LOG_FILE, 'w') as f:
      f.write(str(datetime.now()))
    save_searcn_file_paths()
    run('git', 'add', '*')
    run('git', 'status')
    msg = 'save' # input(" Git commit msg: ")
    run('git', 'commit', '-m', msg)
    run('git', 'push', 'origin', 'br1')
    run('git', 'diff')

    archive_dir = './logs-check-ins'
    if not path.isdir(archive_dir):
        mkdir(archive_dir)
    log_archive_file = archive_dir + '/' + SCRIPT_NAME + '-' + str(datetime.now()).replace(':', '-') + '.log'
    copy(LOG_FILE, log_archive_file)
    print('done')
