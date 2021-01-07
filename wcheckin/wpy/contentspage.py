import logging
import tkinter
import traceback
from datetime import datetime
from tkinter import simpledialog


class ContentsPage:
    @staticmethod
    def update(web_pages):
        (version, lines) = ContentsPage._get_version()
        if version is None:
            print('stopped; version not given')
            exit()
        try:
            with open('../w/contents.html', 'w') as f:
                print ('start--------')
                for line in lines:
                    print ('line--------', line)
                    if line.startswith('<br><br>'):
                        f.write(line + '\n')
                        ContentsPage._append_version_and_content_links(version, web_pages, f)
                        break
                    f.write(line + '\n')
        except Exception as ex:
            logging.exception(ex)
            print(traceback.format_exc())
            with open('../w/contents.html', 'w') as f:
                for line in lines:
                    f.write(line + '\n')
            raise ex

        logging.info('Updated contents.html')
        return version

    @staticmethod
    def _append_version_and_content_links(version, web_pages, f):
        ts = datetime.now().isoformat()
        num = ts[:10] + '/' + ts[21:]
        lines = ContentsPage._get_file_list_table(web_pages)
        lines += '\n<br><p style="font-size:12px;">' + num + ';  ' + version
        f.write(lines)

    @staticmethod
    def _get_version():
        with open('../w/contents.html') as f:
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
    def _get_file_list_table(web_pages):
        web_pages.sort(key=lambda x: x.file_path, reverse=True)
        lines = '<table><tr><td></td> <td></td> <td></td> <td>last update</td><td>line count</td></tr>\n'

        previous_topic = ''
        previous_sub_topic = ''
        for web_page in web_pages:
            if web_page.topic != previous_topic:
                previous_topic = web_page.topic
                display_topic = web_page.topic.title()
            else:
                display_topic = ''

            if web_page.sub_topic != previous_sub_topic:
                previous_sub_topic = web_page.sub_topic
                display_sub_topic = web_page.sub_topic.title()
            else:
                display_sub_topic = ''

            lines += f"<tr><td><b>{display_topic} </b></td> <td>{display_sub_topic}</td> <td>{web_page.link}</td>" \
                     f"<td style=\"font-size:12px;\">{ web_page.modification_date[2:]}</td>" \
                     f"<td>{web_page.content_line_count}</td></tr>\n "

        lines += '</table>'
        return lines

    @staticmethod
    def _create_link(file_path):
        i_start = file_path.rindex('/') + 1
        i_end = file_path.rindex('.html')
        file_name = file_path[i_start:i_end].replace('_', ' ')
        link = '<a href=\'./' + file_path + '\'>' + file_name + '</a>'
        return link
