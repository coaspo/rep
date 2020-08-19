import os
import logging

from pi.webpage import WebPage


class WebSite:
    def __init__(self, target_dirs):
        self.__file_paths = WebSite._get_search_file_paths(target_dirs)

    @staticmethod
    def _get_search_file_paths(target_dirs):
        file_paths = []
        for subdir, dirs, files in os.walk("."):
            is_target_dir = False
            for target_dir in target_dirs:
                if subdir.startswith(target_dir):
                    is_target_dir = True
                    break
            if is_target_dir:
                for file in files:
                    p = os.path.join(subdir, file)[2:]
                    file_paths.append([p, os.path.getmtime(p)])
        file_paths.sort(key=lambda x: x[0])
        logging.info('WebSite; ' + str(len(file_paths)) + ' file paths')
        return file_paths

    def save_search_file_paths(self, save_file):
        with open(save_file, 'w') as f:
            f.writelines('/' + x[0] + '\n' for x in self.file_paths)

    @property
    def file_paths(self) -> list:
        return self.__file_paths

    def save_search_labels(self, save_file):
        with open(save_file, 'w') as f:
            f.write('')
        is_first = True
        for i, x in enumerate(self.file_paths):
            if 'problem' in x[0]:
                continue
            web_page = WebPage(x[0])
            indexes = web_page.search_indexes
            if len(indexes) > 0:
                with open(save_file, 'a') as f:
                    for atrs in indexes:
                        if not is_first:
                            f.write('\n')
                        else:
                            is_first = False
                        f.write(atrs[0])  # anchor label or table header
                        f.write('$$')
                        f.write(str(i))  # file index number
                        if len(atrs) > 1:
                            f.write('$$')
                            f.write(atrs[1])  # url
        logging.info('Created ' + save_file)

    def __str__(self) -> str:
        return f'WebSite: file_paths = {self.__file_paths} '
