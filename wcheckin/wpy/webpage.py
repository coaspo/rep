import logging
import os.path
import re
from datetime import datetime
from wpy.util import Util


class WebPage:
    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.__link = WebPage._create_link(file_path)
        self.__topic, self.__sub_dir = WebPage._find_topic(file_path)
        update_ts = os.path.getmtime(file_path)

        self.__modification_date = str(datetime.utcfromtimestamp(update_ts))[:10]
        lines = WebPage._read_file(file_path)
        if lines is None:
            self.__search_indexes = []
            self.__excerpt = self.__date_range = ''
        else:
            self.__search_indexes = WebPage._find_indexes(lines)
            (self.__excerpt, dummy) = WebPage._find_excerpt(lines)
            self.__date_range = WebPage._find_date_range(lines)
        self.__kb_size = round(os.path.getsize(file_path) / 1000, 1)

        logging.debug(file_path)


    @staticmethod
    def _read_file(file_path):
        if file_path.endswith('.html') or file_path.endswith('.txt'):
            try:
                with open(file_path, encoding="utf-8") as f:
                    lines = f.readlines()
                    return lines
            except Exception:
                print('ERR file_path=', file_path)
                raise
        else:
            return None


    @staticmethod
    def _create_link(file_path):
        i_start = file_path.rindex('/') + 1
        if file_path.endswith('.html'):
            i_end = file_path.rindex('.html')
        else:
            i_end = len(file_path)
        file_name = file_path[i_start:i_end].replace('_', ' ')
        file_name = file_name[0].upper() + file_name[1:]
        link = '<a href=\'./' + file_path + '\'>' + file_name + '</a>'
        return link

    @staticmethod
    def _extract_italicized_labels(line):
        """
        >>> WebPage._extract_italicized_labels('aa <i>AAA</i> bbb <i>BBB</i> xxx<i>222</i>yyy<i>333</i>zzz')
        'aaa bbb 222 333'
        """
        s = re.sub("^(.*?)<i>", "", line)
        s = re.sub("</i>.*?<i>", " ", s)
        s = re.sub("</i>.*", "", s).strip().lower()
        return s

    @staticmethod
    def _find_indexes(lines):
        indexes = []
        for line in lines:
            # search for anchors:
            i = line.find('<a ')
            if i > -1:
                if line.find('</a>', i) < 1:
                    raise Exception('ERR missing </a> in: ' + line + 'ERR lines = ' + lines)
                ii = line.index('</a>', i) + 4
                link = line[i:ii]
                if 'name=' not in link:
                    label_url = Util.extract_url_label(link)
                    indexes.append(label_url)
            # search for italic keywords:
            i = line.find('<i>')
            if i > -1:
                labels = WebPage._extract_italicized_labels(line)
                indexes.append((labels,))
        return indexes

    @staticmethod
    def _find_date_range(lines) -> str:
        dates = []
        for line in lines:
            i = line.find('🗓')
            if i > -1:
                date = line[i + 1:].split("<")
                date = date[0].strip()
                fields = date.split(" - ")
                fields = fields[0].split("-")
                fields = [int(x) for x in fields]
                fields = [str(x) if x > 9 else '0' + str(x) for x in fields]
                date = '-'.join(fields)
                dates.append(date)
        if len(dates) == 0:
            date_range = ''
        elif len(dates) == 1:
            date_range = dates[0]
        else:
            date_range = max(dates) + ' - ' + min(dates)
        return date_range

    @staticmethod
    def _find_excerpt(lines: list) -> (str, int):
        n = 5
        text = ''.join(lines)
        if '<table>' not in text:
            return '', 222  #lines[0: min(len(lines), n)], 222
        text = ''
        if text.find('<table>') > -1:
            num_of_rows = text.count('<tr>')
            num_of_lines = 0
        return ('', 111)


    @staticmethod
    def _find_topic(file_path):
        """
        >>> WebPage._find_topic('a/b/f.html')
        ('a', 'b')
        >>> WebPage._find_topic('a/f.html')
        ('a', '')
        """
        i_start = file_path.index('/w/') + 3
        i_end = file_path.index('/', i_start)
        topic = file_path[i_start:i_end]

        sub_path = file_path[i_end + 1:]
        sub_dir = ''
        if sub_path.find("/") > 0:
            i_end = sub_path.index('/')
            sub_dir = sub_path[:i_end]
        return topic, sub_dir

    @property
    def file_path(self) -> str:
        return self.__file_path

    @property
    def link(self) -> str:
        return self.__link

    @property
    def date_range(self) -> str:
        return self.__date_range

    @property
    def kb_size(self) -> float:
        return self.__kb_size

    @property
    def search_indexes(self) -> list:
        return self.__search_indexes

    @property
    def topic(self) -> str:
        return self.__topic

    @property
    def sub_dir(self) -> str:
        return self.__sub_dir

    @property
    def excerpt(self) -> str:
        return self.__excerpt

    def __str__(self) -> str:
        return f'WebPage: file_path = {self.file_path}, link = {self.link}, ' + \
               f' date_range = {self.date_range}, kb_size = {self.kb_size}, ' + \
               f' search_indexes = {self.search_indexes} topic = {self.topic} ' + \
               f' sub_dir = {self.sub_dir}  excerpt = {self.excerpt}'


if __name__ == '__main__':
    import doctest

    # This runs only a couple of tests;
    doctest.testmod()
