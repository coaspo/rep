from datetime import datetime
from shutil import copy
from subprocess import Popen, PIPE
import os
import sys

FILE_NAME = os.path.basename(__file__)
LOG_PATH = FILE_NAME + '.log'


def run(*args: str):
    print('cmd:', args)
    with open(LOG_PATH, 'a') as f1:
        f1.write('\n' + str(args))

    p = Popen(args, shell=True, stdout=PIPE, stderr=PIPE)
    o, e = p.communicate()
    output = o.decode("utf-8").replace('\r', '')
    errs = e.decode("utf-8").replace('\r', '')

    with open(LOG_PATH, 'a') as f2:
        if len(output) > 0:
            f2.write('\n' + output)
            print(output)
            if 'FAILURES' in output:
                print('May have intermittent tkinter venv failure. - try rerunning')
                sys.exit(1)
        if len(errs) > 0:
            f2.write('\n' + 15 * 'ERR---' + '\n' + errs)
            print(15 * 'ERR---', '\n', errs)
            sys.exit(2)


if __name__ == '__main__':
    with open(LOG_PATH, 'w') as f:
        f.write(str(datetime.now()))
    run(r'..\python-venv\Scripts\activate.bat')
    run('pytest', 'tests/')
    run('git', 'add', '*')
    run('git', 'status')
    msg = input("Git commit msg: ")
    run('git', 'commit', '-m', '"' + msg + '"')
    run('git', 'push', 'origin', 'br1')
    run(r'..\python-venv\Scripts\deactivate.bat')

    archive_dir = './logs-check-ins'
    if not os.path.isdir(archive_dir):
        os.mkdir(archive_dir)
    archive_path = archive_dir + '/' + FILE_NAME + '-' + str(datetime.now()).replace(':', '-') + '.log'
    copy(LOG_PATH, archive_path)
