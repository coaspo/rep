import logging
import tkinter
import traceback
from datetime import datetime
from tkinter import simpledialog
from typing import List

from wpy.webpage import WebPage
from wpy.website import WebSite
from wpy.util import Util


class ContentsPage:
    UPDATE_LINE_MARKER = '<!--c-marker:-->'

    @staticmethod
    def update(web_site: WebSite, contents_file_path: str):
        (version, lines) = ContentsPage._get_version(contents_file_path)
        if version is None:
            print('stopped; version not given')
            exit()
        ContentsPage._update_contents(version, lines, web_site, contents_file_path)
        logging.info('Updated ' + contents_file_path)
        return version

    @staticmethod
    def _update_contents(version, lines, web_site, contents_file_path):
        try:
            with open(contents_file_path, 'w') as f:
                for line in lines:
                    if ContentsPage.UPDATE_LINE_MARKER in line:
                        f.write(line)
                        ts = datetime.now().isoformat()
                        num = ts[2:10] + '/' + ts[11:13] + ts[14:16] + ts[17:19]
                        version_line = '\n<pre>Version: ' + num + '; ' + version + '\n' + \
                                       (' ' * 77) + 'publish date / pages'
                        f.write(version_line)
                        ContentsPage._append_content_links(web_site, f)
                        break
                    f.write(line + '\n')
                f.write('\n</body></html>')
        except Exception as ex:
            logging.exception(ex)
            print(traceback.format_exc())
            with open(contents_file_path, 'w') as f:
                for line in lines:
                    f.write(line + '\n')
                f.close()
            raise ex

    @staticmethod
    def _append_content_links(web_site: WebSite, f):
        topics = web_site.topic_names
        topics.sort()
        lines = ''
        for topic in topics:
            lines += '\n<b>' + topic.upper() + '</b>\n'
            web_pages = web_site.web_page_dict[topic]
            lines += Util.get_web_page_links(web_pages, True)
        f.write(lines)
        f.write('\n all of above files: ')
        f.write("~{:,.0f}".format(web_site.total_page_count))
        f.write(' PGs;  ')
        f.write("~{:,.0f}".format(web_site.total_page_count*60))
        f.write(' lines;  ')
        f.write("~{:,.0f}".format(web_site.total_kb_size))
        f.write(' kB')

    @staticmethod
    def _get_version(contents_file_path):
        with open(contents_file_path) as f:
            lines = f.read().splitlines()

        version = 'UNK'
        for line in lines:
            if line.startswith('<pre>Version:'):
                version = line.split('; ')[1].strip()
                break
        root = tkinter.Tk()
        root.withdraw()
        version = simpledialog.askstring(title="Git check-in;  " + __file__,
                                         prompt=("\nUpdate 'Search contents' related files and check into git.   "
                                                 "\n\nVersion name:"), initialvalue=version)
        return version, lines

