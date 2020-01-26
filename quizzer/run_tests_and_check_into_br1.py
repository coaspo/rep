from datetime import datetime
from os import mkdir
from os import path
from shutil import copy
from subprocess import Popen, PIPE
from sys import exit

SCRIPT_NAME = path.basename(__file__)
LOG_FILE = SCRIPT_NAME + '.log'


def run(*args: str):
    print('cmd:', args)
    with open(LOG_FILE, 'a') as f1:
        f1.write('\n' + str(args))

    p = Popen(args, shell=True, stdout=PIPE, stderr=PIPE)
    o, e = p.communicate()
    output = o.decode("utf-8").replace('\r', '')
    errs = e.decode("utf-8").replace('\r', '')

    with open(LOG_FILE, 'a') as f2:
        if len(output) > 0:
            f2.write('\n' + output)
            print(output)
            if 'FAILURES' in output:
                print('May have intermittent tkinter venv failure. - try rerunning')
                exit(1)
        if len(errs) > 0:
            f2.write('\n' + 15 * 'ERR---' + '\n' + errs)
            print(15 * 'ERR---', '\n', errs)
            exit(2)


if __name__ == '__main__':
    with open(LOG_FILE, 'w') as f:
        f.write(str(datetime.now()))
    run(r'..\python-venv\Scripts\activate.bat')
    run('pytest', 'tests/')
    run('git', 'add', '*')
    run('git', 'status')
    msg = '"' + input("Git commit msg: ") + '"'
    run('git', 'commit', '-m', msg)
    run('git', 'push', 'origin', 'br1')
    run('git', 'diff')
    run(r'..\python-venv\Scripts\deactivate.bat')

    archive_dir = './logs-check-ins'
    if not path.isdir(archive_dir):
        mkdir(archive_dir)
    log_archive_file = archive_dir + '/' + SCRIPT_NAME + '-' + str(datetime.now()).replace(':', '-') + '.log'
    copy(LOG_FILE, log_archive_file)
