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
            with open('contents.html', 'w') as f:
                for line in lines:
                    if line.startswith('<br><br>'):
                        f.write(line + '\n')
                        ContentsPage._append_version_and_content_links(version, web_pages, f)
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
    def _append_version_and_content_links(version, web_pages, f):
        ts = datetime.now().isoformat()
        num = ts[:10] + '/' + ts[21:]
        lines = ContentsPage._get_file_list_table(web_pages)
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
    def _get_file_list_table(web_pages):
        web_pages.sort(key=lambda x: x.modification_date, reverse=True)
        lines = '<table>'
        topics = set()
        for web_page in web_pages:
            path = web_page.file_path
            i_end = path.index('/')
            topic = path[:i_end]
            topics.add(topic)

        previous_topic = ''
        previous_sub_topic = ''
        for web_page in web_pages:
            dt = web_page.modification_date
            link = web_page.link
            num_of_lines = web_page.num_of_lines

            path = web_page.file_path  # path may be  topic/sub-topic/x.html or topic/x.html
            i_end = path.index('/')
            topic = path[:i_end]
            if topic != previous_topic:
                previous_topic = topic
                display_topic = topic.title()
            else:
                display_topic = ''

            path = path[i_end + 1:]
            sub_topic = ''
            if path.find("/") > 0:
                i_end = path.index('/')
                sub_topic = path[:i_end]

            if sub_topic != previous_sub_topic:
                previous_sub_topic = sub_topic
                display_sub_topic = sub_topic.title()
            else:
                display_sub_topic = ''

            lines += f"<tr><td><b>{display_topic} </b></td> <td>{display_sub_topic}</td> <td>{link}</td>" \
                     f"> <td style=\"font-size:12px;\">{dt}</td><td>{num_of_lines}</td><tr>\n "

        lines += '</table>'
        return lines

    @staticmethod
    def _create_link(file_path):
        i_start = file_path.rindex('/') + 1
        i_end = file_path.rindex('.html')
        file_name = file_path[i_start:i_end].replace('_', ' ')
        link = '<a href=\'./' + file_path + '\'>' + file_name + '</a>'
        return link
