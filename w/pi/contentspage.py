import logging
import tkinter
import traceback
from datetime import datetime
from tkinter import simpledialog


class ContentsPage:
    @staticmethod
    def update(file_paths):
        (version, lines) = ContentsPage._get_version()
        if version is None:
            print('stopped; version not given')
            exit()
        try:
            with open('contents.html', 'w') as f:
                for line in lines:
                    if line.startswith('<br><br>'):
                        f.write(line + '\n')
                        ContentsPage._append_version_and_content_links(version, file_paths, f)
                        break
                    f.write(line + '\n')
        except Exception:
            logging.exception('')
            print(traceback.format_exc())
            with open('contents.html', 'w') as f:
                for line in lines:
                    f.write(line + '\n')
            raise

        logging.info('Updated contents.html')
        return version

    @staticmethod
    def _append_version_and_content_links(version, file_paths, f):
        ts = datetime.now().isoformat()
        num = ts[:10] + '/' + ts[21:]
        lines = ContentsPage._get_contents_file_list(file_paths)
        lines += '\n<br><p style="font-size:12px;">' + num + ';  ' + version
        f.write(lines)

    @staticmethod
    def _get_version():
        with open('contents.html') as f:
            lines = f.read().splitlines()

        version = 'update'
        for line in lines:
            if line.startswith('<p style="font-size:12px;">'):
                # for example: line = '2020-05-10; links',  version= 'links'
                version = line.split(';')[1].strip()
                break

        root = tkinter.Tk()
        root.withdraw()
        version = simpledialog.askstring(title="Git check-in;  " + __file__,
                                         prompt=("\nUpdate 'Search contents' related files and check into git.   "
                                                 "\nThis may take a while."
                                                 "\n\nVersion name:"), initialvalue=version)
        return version, lines

    @staticmethod
    def _get_contents_file_list(file_paths):
        file_paths.sort(key=lambda x: x[1], reverse=True)  # sort by last modified TS
        lines = '<table>'
        lines += ContentsPage._add_table_rows(file_paths, 'science')
        lines += ContentsPage._add_table_rows(file_paths, 'arts')
        lines += ContentsPage._add_table_rows(file_paths, 'recipes')
        lines += ContentsPage._add_table_rows(file_paths, 'tech')
        lines += '</table>'
        return lines

    @staticmethod
    def _add_table_rows(file_paths, topic):
        i = 0
        lines = ''
        label = topic + '/'
        for p in file_paths:
            if label in p[0]:
                i += 1
                dt = datetime.utcfromtimestamp(p[1]).strftime('%Y-%m-%d')
                link = ContentsPage._create_link(p[0])
                if i == 1:
                    lines += f"<tr><td>{topic.title()}:</td> <td>{link}</td> <td style=\"font-size:12px;\">{dt}</td" \
                             f"><tr>\n "
                else:
                    lines += f"<tr><td></td> <td>{link}</td> <td style=\"font-size:12px;\">{dt}</td><tr>\n"
        return lines

    @staticmethod
    def _create_link(file_path):
        i_start = file_path.rindex('/') + 1
        i_end = file_path.rindex('.html')
        file_name = file_path[i_start:i_end].replace('_', ' ')
        link = '<a href=\'./' + file_path + '\'>' + file_name + '</a>'
        return link
