import logging
import tkinter
import traceback
from datetime import datetime
from tkinter import simpledialog


class ContentsPage:
    VERSION_LINE_MARKER = '<br><br><p style="font-size:8px;">'

    @staticmethod
    def update(web_site, contents_file_path):
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
                    if line.startswith(ContentsPage.VERSION_LINE_MARKER):
                        ts = datetime.now().isoformat()
                        num = ts[2:10] + '/' + ts[11:13] + ts[14:16] + ts[17:19]
                        version_line = '\n' + ContentsPage.VERSION_LINE_MARKER + num + ';  ' + version + '</p>'
                        f.write(version_line)
                        ContentsPage._append_content_links(web_site, f)
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
    def _append_content_links(web_site, f):
        f.write('\n<table id="table">\n<tr> <th></th> <th></th> <th onclick = "sortTable(2)"> File ↕️</th> ' +
                '<th onclick = "sortTable(3)">update ↕️</th> <th onclick = "sortTable(4)"> kB ↕️</th> </tr>\n')
        lines = ''
        for topic_name in web_site.topic_names:
            lines += ContentsPage._get_file_list_table(web_site.web_page_dict[topic_name])
        f.write(lines)
        f.write('\n</table>')

    @staticmethod
    def _get_version(contents_file_path):
        with open(contents_file_path) as f:
            lines = f.read().splitlines()

        version = 'UNK?'
        for line in lines:
            if line.startswith(ContentsPage.VERSION_LINE_MARKER):
                version = line.split('; ')[1].strip()
                version = version[:len(version)-4]
                break

        root = tkinter.Tk()
        root.withdraw()
        version = simpledialog.askstring(title="Git check-in;  " + __file__,
                                         prompt=("\nUpdate 'Search contents' related files and check into git.   "
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
            if topic != previous_topic:
                previous_topic = topic
                line += '<td><b>' + topic + '</b></td><td>'
                line += '.</td><td>' if sub_dir == '' else sub_dir + '</td><td>'
            else:
                line += '<td></td><td>'
                if sub_dir =='':
                   line += '.</td><td>' if sub_dir == previous_sub_dir else sub_dir + '</td><td>'
                else:
                   line += '</td><td>' if sub_dir == previous_sub_dir else sub_dir + '</td><td>'
            previous_sub_dir = sub_dir
            lines += line + f"{page.link}</td><td style='font-size:12px;'>{page.modification_date[2:]}" + \
                     f"</td><td>{page.kb_size}</td></tr>\n"
        return lines

    @staticmethod
    def _create_link(file_path):
        i_start = file_path.rindex('/') + 1
        if file_path.endswith('.html'):
            i_end = file_path.rindex('.html')
        else:
            i_end = len(file_path)
        file_name = file_path[i_start:i_end].replace('_', ' ')
        link = '<a href=\'./' + file_path + '\'>' + file_name + '</a>'
        return link
