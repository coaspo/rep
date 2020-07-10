#!/usr/bin/env python3

from multiprocessing import Process
from tkinter import messagebox
import os
import subprocess
import time
import traceback
import webbrowser

def f():
    # start local server:
    os.system('python3 -m http.server 8080')


def start_local_server():
    os.chdir('..')
    os.chdir('..')
    global msg
    msg += '\n1. cwd= '+ os.getcwd()
    # stop any local server:
    os.system('fuser -k 8080/tcp')
    msg += '\n2. process using 8080 stopped'

    p = Process(target=f)
    p.start()
    time.sleep(2)
    msg += '\n3. local server started'


if __name__ == '__main__':
    msg = ''
    try: 
      start_local_server()
      webbrowser.open('http://localhost:8080/w/tests/test_search.html')
      msg += '\n4/4. run local tests'
      print(msg)
    except Exception as e:
      print(traceback.format_exc())
      messagebox.showinfo(__file__, os.path.basename(__file__) + ' FAILED; \n\n' + str(e))

