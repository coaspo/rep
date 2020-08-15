from subprocess import Popen, PIPE
from tkinter import messagebox


class CheckIn():
    @staticmethod
    def runGitCommands(version, git_branch):
        CheckIn._run('git', 'add', '*')
        CheckIn._run('git', 'status')
        CheckIn._run('git', 'commit', '-m', "'" + version + "'")
        CheckIn._run('git', 'push', 'origin', git_branch)
        # CheckIn._run('git', 'diff')


    @staticmethod
    def _run(*args: str):
        # global msg
        # msg += '\n' + str(args)
        print('cmd:', args)
        # log('cmd:', args)

        p = Popen(args, shell=False, stdout=PIPE, stderr=PIPE)
        o, e = p.communicate()
        output = o.decode("utf-8").replace('\r', '')
        errs = e.decode("utf-8").replace('\r', '')

        if len(output) > 0:
            # log('output: ', output)
            print(output)
            if 'FAILURES' in output:
                messagebox.showinfo("FAILURES", msg +
                                    '\nMay have intermittent tkinter venv failure.\nTry rerunning')
                exit(1)
        if len(errs) > 0:
            log('errs: ', errs)
            print(errs)
            if 'Everything up-to-date' in errs:
                messagebox.showinfo("Git done", msg + '\nCode checked in')
                exit(0)
            label = 15 * 'ERR---' if 'br1 -> br1' not in str(errs) else ''
            log(label)
            print(label)
            if 'ERR---' in label:
                messagebox.showinfo("ERR", msg + '\n' + label)
                exit(2)
