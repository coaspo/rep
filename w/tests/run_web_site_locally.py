#!/usr/bin/env python3
import webbrowser
import os
import subprocess
from multiprocessing import Process
import time

def f():
    # start local server:
    os.system('python3 -m http.server 8080')


def start_local_server():
    os.chdir('..')
    os.chdir('..')
    print('cwd=', os.getcwd())
    # stop any local server:
    os.system('fuser -k 8080/tcp')
    print('process using 8080 stopped')

    p = Process(target=f)
    p.start()
    time.sleep(2)
    print('local server started')



if __name__ == '__main__':
    start_local_server()
    webbrowser.open('http://localhost:8080/w/')
    print('opened web site in local server')

