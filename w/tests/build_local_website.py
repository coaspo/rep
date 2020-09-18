import os
from datetime import datetime
from os import path
from shutil import copyfile
from subprocess import Popen, PIPE
from sys import exit


def run(*args: str):
    print('\nCMD:', args)
    p = Popen(args, shell=True, stdout=PIPE, stderr=PIPE)
    o, e = p.communicate()
    output = o.decode("utf-8").replace('\r', '')
    errs = e.decode("utf-8").replace('\r', '')
    print('output:', output)
    print('errs:', errs)


def make_paths_usable_by_local_server():
    copyfile('./tests/search_file_paths__t.txt', 'search_file_paths.txt')
    copyfile('./tests/search_labels__t.txt', 'search_labels.txt')
    print('made paths usable by local server')


if __name__ == '__main__':
    print('Started', __file__)
    run(r'. venv/bin/activate')
    run('pytest',  './tests')
    make_paths_usable_by_local_server()
    print('done')
    exit(0)
