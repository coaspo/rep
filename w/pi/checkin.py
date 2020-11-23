import logging
from subprocess import Popen, PIPE
from tkinter import messagebox


class CheckIn:
    @staticmethod
    def run_git_commands(version, git_branch):
        CheckIn._run('python3', 'tests/run_all_pytests.py')
        CheckIn._run('git', 'add', '*')
        CheckIn._run('git', 'status')
        CheckIn._run('git', 'commit', '-m', "'" + version + "'")
        CheckIn._run('git', 'push', 'origin', git_branch)
        # CheckIn._run('git', 'diff')

    @staticmethod
    def _run(*args: str):
        msg = ' '.join(args)
        logging.info(msg)
        print('cmd: ', msg)

        p = Popen(args, shell=False, stdout=PIPE, stderr=PIPE)
        o, e = p.communicate()
        output = o.decode("utf-8").replace('\r', '')
        errs = e.decode("utf-8").replace('\r', '')

        if len(output) > 0:
            print(output)
            if 'FAILURES' in output:
                logging.error(output)
                if not logging.getLogger().isEnabledFor(logging.DEBUG):
                    messagebox.showinfo("FAILURES", output +
                                        '\nMay have intermittent tkinter venv failure.\nTry rerunning')
                exit(1)
        if len(errs) > 0:
            logging.error(errs)
            print(errs)
            if 'Everything up-to-date' in errs:
                if not logging.getLogger().isEnabledFor(logging.DEBUG):
                    messagebox.showinfo("Git done", errs + '\nCode checked in')
                exit(0)
            label = 15 * 'ERR---' if 'br1 -> br1' not in str(errs) else ''
            print(label)
            if 'ERR---' in label:
                logging.error(label)
                if not logging.getLogger().isEnabledFor(logging.DEBUG):
                    messagebox.showinfo("ERR", label)
                exit(2)
