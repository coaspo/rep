import logging
import tkinter
import traceback
from datetime import datetime
from tkinter import simpledialog
from wpy.website import WebSite


class ContentsPage:
    UPDATE_LINE_MARKER = '<br><br>'

    @staticmethod
    def update(web_site: WebSite, contents_file_path: str):
        (version, lines) = ContentsPage._get_version(contents_file_path)
        print('------', version)
        [print(x) for x in lines]
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
                    if line.startswith(ContentsPage.UPDATE_LINE_MARKER):
                        f.write(ContentsPage.UPDATE_LINE_MARKER)
                        ContentsPage._append_content_links(web_site, f)
                        ts = datetime.now().isoformat()
                        num = ts[2:10] + '/' + ts[11:13] + ts[14:16] + ts[17:19]
                        version_line = '\n<p style="font-size:8px;">' + num + '; ' + version + '</p>\n</body></html>'
                        f.write(version_line)
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

    @staticmethod
    def _append_content_links(web_site: WebSite, f):
        f.write('\n<table id="table">\n' +
                '<tr> <th onclick = "sortTable(0)"> Topic ↕️</th> <th onclick = "sortTable(1)"> subdir ↕️</th>' +
                '<th onclick = "sortTable(2)"> File ↕️</th> <th onclick = "sortTable(3)">dates ↕️</th>' +
                '<th onclick="sortTable(4)"> kB ↕️</th>/tr>\n')
        lines = ''
        for topic_name in web_site.topic_names:
            web_pages = web_site.web_page_dict[topic_name]
            lines += ContentsPage._get_file_list_table_rows(web_pages)
        f.write(lines)
        f.write('</table>\nall files: ')
        f.write(str(web_site.total_kb_size))
        f.write(' kB')

    @staticmethod
    def _get_version(contents_file_path):
        with open(contents_file_path) as f:
            lines = f.read().splitlines()

        version = 'UNK?'
        for line in lines:
            if line.startswith('<p style='):
                version = line.split('; ')[1].strip()
                version = version[:len(version) - 4]
                break

        root = tkinter.Tk()
        root.withdraw()
        version = simpledialog.askstring(title="Git check-in;  " + __file__,
                                         prompt=("\nUpdate 'Search contents' related files and check into git.   "
                                                 "\n\nVersion name:"), initialvalue=version)
        return version, lines

    @staticmethod
    def _get_file_list_table_rows(web_pages):
        web_pages.sort(key=lambda x: x.file_path, reverse=True)

        previous_topic = ''
        previous_sub_dir = ''
        lines: str = ''
        for page in web_pages:
            line = '<tr>'
            topic = page.topic
            topic = topic[0].upper() + topic[1:]
            sub_dir = page.sub_dir
            if topic != previous_topic:
                previous_topic = topic
                line += '<td><b>' + topic + '</b></td><td>'
                line += '.</td>' if sub_dir == '' else sub_dir + '</td>'
            else:
                line += '<td class="i"><b>' + topic + '</b></td>'
                if sub_dir == '':
                    line += '<td>.</td>'
                elif sub_dir == previous_sub_dir:
                    line += '<td class="i">' + sub_dir + '</td>'
                else:
                    line += '<td>' + sub_dir + '</td>'
            previous_sub_dir = sub_dir
            lines += line + f"<td>{page.link}</td><td style='font-size:12px;'>{page.date_range}</td>" + \
                            f"<td>{page.kb_size}</td></tr>\n"
        return lines
