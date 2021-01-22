import logging
import traceback
from wpy.website import WebSite


class ExcerptPage:

    @staticmethod
    def create_excerpts(web_site: WebSite, details_file_path: str):
        try:
            with open(details_file_path, 'w') as f:
                f.write('\n<table id="table">\n' +
                        '<th onclick = "sortTable(0)"> File / Excerpt ↕️ </th>' +
                        '<th onclick="sortTable(1)">Updated ↕️</th></tr>\n')
                for topic_name in web_site.topic_names:
                    web_pages = web_site.web_page_dict[topic_name]
                    lines = ExcerptPage._get_file_list_table_rows(web_pages)
                    f.write(lines)
        except Exception as ex:
            logging.exception(ex)
            print(traceback.format_exc())

    @staticmethod
    def _get_file_list_table_rows(web_pages):
        web_pages.sort(key=lambda x: x.file_path, reverse=True)
        lines: str = ''
        for page in web_pages:
            if page.file_path.endswith('.html') or page.file_path.endswith('.txt'):
                path = page.topic
                path = path[0].upper() + path[1:]
                path += '/' + page.sub_dir
                lines += f'<tr><td><b>{path}/{page.link}</b><br>{page.link}</td><td>{page.modification_date[2:]}</td>\n'
        return lines
