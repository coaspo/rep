import logging
import tkinter
import traceback
from datetime import datetime
from tkinter import simpledialog


class ContentsPage:
    @staticmethod
    def update(web_site, contents_file_path):
        (version, lines) = ContentsPage._get_version(contents_file_path)
        if version is None:
            print('stopped; version not given')
            exit()
        try:
            with open(contents_file_path, 'w') as f:
                for line in lines:
                    if line.startswith('<br><br>'):
                        f.write(line)
                        f.write(
                            '\n<table><tr><td></td> <td></td> <td></td> <td>last update</td><td>line count</td></tr>\n')
                        ContentsPage._append_version_and_content_links(version, web_site, f)
                        f.write('</table>')
                        f.close()
                        break
                    f.write(line + '\n')
        except Exception as ex:
            logging.exception(ex)
            print(traceback.format_exc())
            with open(contents_file_path, 'w') as f:
                for line in lines:
                    f.write(line + '\n')
                f.close()
            raise ex

        logging.info('Updated ' + contents_file_path)
        return version

    @staticmethod
    def _append_version_and_content_links(version, web_site, f):
        lines = ''
        for topic_name in web_site.topic_names:
            lines += ContentsPage._get_file_list_table(web_site.web_page_dict[topic_name])
        ts = datetime.now().isoformat()
        num = ts[2:10] + '/' + ts[11:13] + ts[14:16] + ts[17:19]

        lines += '\n<br><p style="font-size:12px;">' + num + ';  ' + version
        f.write(lines)

    @staticmethod
    def _get_version(contents_file_path):
        with open(contents_file_path) as f:
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

        previous_topic = ''
        previous_sub_dir = ''
        lines: str = ''
        for page in web_pages:
            line = '<tr>'
            topic = page.topic
            sub_dir = page.sub_dir
            link = page.link
            if topic != previous_topic:
                previous_topic = topic
                line += '<td><b>' + topic + '</b></td>'
                if sub_dir == '':
                    line += '<td colspan="2">'
                else:
                    line += '<td>' + sub_dir + '</td><td>'
            else:
                if sub_dir == '':
                    line += '<td></td><td colspan="2">'
                else:
                    if sub_dir == previous_sub_dir:
                        line += '<td></td><td></td></td><td>'
                    else:
                        line += '<td></td><td>' + sub_dir + '</td><td>'
            previous_sub_dir = sub_dir
            lines += line + f"{page.link}</td><td style=\"font-size:12px;\">{page.modification_date[2:]}" + \
                     f"</td><td>{page.content_line_count}</td></tr>\n"
        return lines

    @staticmethod
    def _create_link(file_path):
        i_start = file_path.rindex('/') + 1
        i_end = file_path.rindex('.html')
        file_name = file_path[i_start:i_end].replace('_', ' ')
        link = '<a href=\'./' + file_path + '\'>' + file_name + '</a>'
        return link
