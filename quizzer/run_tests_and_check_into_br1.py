import os
import sys
from datetime import datetime
from subprocess import Popen, PIPE

LOG_FILE = os.path.basename(__file__) + '.log'


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
                sys.exit(1)
        if len(errs) > 0:
            f2.write('\n' + 15 * 'ERR---' + '\n' + errs)
            print(15 * 'ERR---', '\n', errs)
            sys.exit(2)


if __name__ == '__main__':
    with open(LOG_FILE, 'w') as f:
        f.write(str(datetime.now()))
    run(r'..\python-venv\Scripts\activate.bat')
    run('pytest', 'tests/')
    run('git', 'add', '*')
    run('git', 'status')
    msg = input("Git commit msg: ")
    run('git', 'commit', '-m', '"' + msg + '"')
    run('git', 'push', 'origin', 'brw')
    run(r'..\python-venv\Scripts\deactivate.bat')
