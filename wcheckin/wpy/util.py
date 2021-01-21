import logging
from subprocess import Popen, PIPE
from tkinter import messagebox


class Util:
    @staticmethod
    def run_tests():
        Util._run('python3', 'tests/run_all_pytests.py')

    @staticmethod
    def check_into_repository(version, git_branch):
        Util._run('git', 'add', '*')
        Util._run('git', 'status')
        Util._run('git', 'commit', '-m', "'" + version + "'")
        Util._run('git', 'push', 'origin', git_branch)
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
            if 'FAILURES' in output or 'ERROR' in output:
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

    @staticmethod
    def extract_url_label(link):
        """
        >>> Util.extract_url_label('<a href="https://www.coursera.org/">Coursera- Free course</a>')
        ('coursera- free course', 'https://www.coursera.org/')
        >>> Util.extract_url_label("<a href='https://www.coursera.org/'>Coursera- Free course</a>")
        ('coursera- free course', 'https://www.coursera.org/')
        """
        link = link.replace('href= ', 'href=')
        quote = '"' if link.find('href="') > -1 else "'"
        try:
            i = link.index('href=' + quote) + 6
            i2 = link.index(quote, i)
            url = link[i:i2]
            i = link.index('>', i2) + 1
            i2 = link.index('</a>', i)
            label = link[i:i2].lower().strip()
            attrs = (label, url)
            return attrs
        except Exception as ex:
            print('for', link, 'got:\n', ex)
            logging.exception(ex)
            raise ex
