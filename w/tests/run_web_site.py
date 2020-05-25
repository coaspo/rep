import webbrowser
import os
import subprocess
from multiprocessing import Process
import time

def f():
    os.system('python3 -m http.server 8080')

os.chdir('..')
os.chdir('..')
print('cwd=', os.getcwd())

os.system('fuser -k 8080/tcp')
print('process using 8080 stopped')

p = Process(target=f)
p.start()
time.sleep(2)
print('local server ready')

if __name__ == '__main__':
    webbrowser.open('http://localhost:8080/w/')
    print('starter site in local server')

