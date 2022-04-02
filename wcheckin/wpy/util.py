import logging
import os
from subprocess import Popen, PIPE
from tkinter import messagebox
from datetime import datetime


class Util:
    @staticmethod
    def run_tests():
        logging.info('_' * 80 + '\n----- 0. cwd: ' + os.getcwd())
        msg = Util._run('python3', 'tests/run_all_pytests.py')
        messagebox.showinfo('TESTS ' + os.getcwd() + ' run_all_pytests.py', msg)

    @staticmethod
    def check_into_repository(version, git_branch):
        msg = '__1. ' + Util._run('git', 'add', '*')
        msg += '\n=__2. ' + Util._run('git', 'status', '-s')
        msg += '\n__3. ' + Util._run('git', 'commit', '-m', "'" + version + "'")
        msg += '\n__4. ' + Util._run('git', 'push', 'origin', git_branch)
        yy_mm_dd = datetime.now().isoformat()[2:10]
        msg += '\n__5. ' + Util._run('git', 'tag', '--force', yy_mm_dd, 'HEAD')
        # msg += '\n__6. ' + Util._run('git', 'push', '--tags', '--force')
        # failed fist run but not second run; replace with:
        msg += '\n__6. ' + Util._run('git', 'push', '-f', '--tags')
        print("msg=", msg)
        messagebox.showinfo('CHECKIN: ' + os.getcwd(), msg)
        logging.info('check_into_repository DONE')

    @staticmethod
    def _run(*args: str) -> str:
        msg = ' '.join(args)
        logging.info(msg)
        print('cmd: ', msg)

        p = Popen(args, shell=False, stdout=PIPE, stderr=PIPE)
        o, e = p.communicate()
        output = o.decode("utf-8").replace('\r', '')
        possible_errs = e.decode("utf-8").replace('\r', '')

        if len(output) > 0:
            msg = msg + '\n' + output
            print('output:\n', msg)
            logging.info('output:\n%s', msg)
        elif len(possible_errs) > 0:
            msg = msg + '\n' + possible_errs
            print('possible_ERRs:\n', msg)
            logging.info('possible_ERRs:\n%s', msg)
            if not (' -> ' in msg or 'Everything up-to-date' in msg):
                print('ERR in possible_ERRs')
                messagebox.showinfo('git ERR', msg)
                exit(2)
        if len(msg) > 300:
            msg = msg[0:300] + '  ...\n'
        return msg

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
        print(quote, '=====', link)
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

    @staticmethod
    def add_mouse_listeners(link):
        """
        >>> Util.add_mouse_listeners('<a href="https://www.coursera.org/">Coursera- Free course</a>')
        '<a href="https://www.coursera.org/" onmouseenter="enterLink(event)" onmouseleave="leaveLink(event)">'\
        'Coursera- Free course</a>'
        """
        try:
            i = link.index('>')
            link = link[:i] + ' onmouseenter="enterLink(event)" ' + link[i:]
            return link
        except Exception as ex:
            print('for', link, 'got:\n', ex)
            logging.exception(ex)
            raise ex

    @staticmethod
    def _get_formattedText(sub_dir, sub_sub_dir, link, link_indent, page):
        sub_dir = sub_dir.replace('_', '').replace('-', ' ')
        sub_sub_dir = sub_sub_dir.replace('_', '').replace('-', ' ')
        txt = ''
        if len(sub_dir) > 0:
            txt = sub_dir + '<br>\n'
        if len(sub_sub_dir) > 0:
            txt += 4 * '&nbsp;' + sub_sub_dir + '<br>\n'
        if page is not None:
            sfx = ' ' * (75 - len(link.split('>')[1].split('<')[0]) - link_indent)
            link += sfx
            date = page.date_range
            pg_cnt = str(page.page_count)
            link += date.ljust(10, ' ') + '  ' + pg_cnt
        txt += link_indent * '&nbsp;' + link + '<br>\n'
        return txt

    @staticmethod
    def get_web_page_links(webpages, is_for_contents_page):
        page = webpages[0]
        link_indent = 0
        if len(page.sub_dir) > 0:
            link_indent = 4
        if len(page.sub_sub_dir) > 0:
            link_indent = 8
        pg = page if is_for_contents_page else None
        txt = Util._get_formattedText(page.sub_dir, page.sub_sub_dir, page.link, link_indent, pg)
        for i in range(1, len(webpages)):
            page = webpages[i]
            if is_for_contents_page and 'class="test"' in page.link:
                continue
            prev_page = webpages[i - 1]
            link_indent = 0
            if len(page.sub_dir) > 0:
                link_indent = 4
            if len(page.sub_sub_dir) > 0:
                link_indent = 8
            if page.sub_dir == prev_page.sub_dir:
                sub_dir = ''
            else:
                sub_dir = page.sub_dir
            if page.sub_sub_dir == prev_page.sub_sub_dir:
                sub_sub_dir = ''
            else:
                sub_sub_dir = page.sub_sub_dir
            pg = page if is_for_contents_page else None
            txt += Util._get_formattedText(sub_dir, sub_sub_dir, page.link, link_indent, pg)
        if is_for_contents_page:
            txt = '    ' + txt.replace('<br>', '').replace('&nbsp;', ' ').replace('\n', '\n    ')
        return txt
