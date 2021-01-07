import logging
import os.path
import re
from datetime import datetime


class WebPage:
    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.__link = WebPage._create_link(file_path)
        update_ts = os.path.getmtime(file_path)
        self.__modification_date = str(datetime.utcfromtimestamp(update_ts))[:10]
        self.__search_indexes,  self.__content_line_count ,  self.__description = \
            WebPage._scan_file(file_path)
        self.__topic, self.__sub_topic = \
            WebPage._find_topics(file_path)
        logging.debug(file_path)

    @staticmethod
    def _create_link(file_path):
        i_start = file_path.rindex('/') + 1
        i_end = file_path.rindex('.html')
        file_name = file_path[i_start:i_end].replace('_', ' ')
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
    def _extract_url_label(link):
        """
        >>> WebPage._extract_url_label('<a href="https://www.coursera.org/">Coursera- Free course</a>')
        ('coursera- free course', 'https://www.coursera.org/')
        >>> WebPage._extract_url_label("<a href='https://www.coursera.org/'>Coursera- Free course</a>")
        ('coursera- free course', 'https://www.coursera.org/')
        """
        link = link.replace('href= ', 'href=')
        quote = '"' if link.find('href="') > -1 else "'"
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
            print('for',link,'got:\n', ex)
            logging.exception(ex)
            raise ex
            

    @staticmethod
    def _scan_file(file_path):
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()
        indexes = []
        num_of_lines = 0
        description = ''
        for line in lines:
            num_of_lines += 1
            if line.find('<body>') > -1:
                num_of_lines = 0
            # search for comment:
            if line.find('<!--') > -1:
                description = line.replace('<!--', '').replace('-->', '').replace('\n', '')
            # search for anchors:
            i = line.find('<a ')
            if i > -1:
                if line.find('</a>', i) < 1:
                    raise Exception('ERR missing </a> in: ' + line + 'ERR file_path = ' + file_path)
                ii = line.index('</a>', i) + 4
                link = line[i:ii]
                if 'name=' not in link:
                    label_url = WebPage._extract_url_label(link)
                    indexes.append(label_url)
            # search for italic keywords:
            i = line.find('<i>')
            if i > -1:
                labels = WebPage._extract_italicized_labels(line)
                indexes.append((labels,))
        return indexes, num_of_lines - 1, description

    @staticmethod
    def _find_topics(file_path):
        """
        >>> WebPage._find_topics('a/b/f.html')
        ('a', 'b')
        >>> WebPage._find_topics('a/f.html')
        ('a', '')
        """
        i_end = file_path.index('/')
        topic = file_path[:i_end]

        sub_path = file_path[i_end + 1:]
        sub_topic = ''
        if sub_path.find("/") > 0:
            i_end = sub_path.index('/')
            sub_topic = sub_path[:i_end]
        return topic, sub_topic

    @property
    def file_path(self) -> str:
        return self.__file_path

    @property
    def link(self) -> str:
        return self.__link

    @property
    def modification_date(self) -> str:
        return self.__modification_date

    @property
    def content_line_count(self) -> int:
        return self.__content_line_count

    @property
    def search_indexes(self) -> list:
        return self.__search_indexes

    @property
    def topic(self) -> str:
        return self.__topic

    @property
    def sub_topic(self) -> str:
        return self.__sub_topic

    @property
    def description(self) -> str:
        return self.__description

    def __str__(self) -> str:
        return f'WebPage: file_path = {self.file_path}, ' + \
               f' modification_date = {self.modification_date}, num_of_lines = {self.content_line_count}, ' + \
               f' search_indexes = {self.search_indexes} '


if __name__ == '__main__':
    import doctest
    # This runs only a couple of tests;
    doctest.testmod()
