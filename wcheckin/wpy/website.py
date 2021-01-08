import logging
import os

from wpy.webpage import WebPage


class WebSite:
    def __init__(self, target_dirs):
        self.__file_path_structure = WebSite._get_search_file_path_structures(target_dirs)
        self.__web_pages = WebSite._get_web_pages(target_dirs)

    @staticmethod
    def _get_search_file_path_structures(target_dirs):
        file_path_structures = []
        for target_dir in target_dirs:
            for subdir, dirs, files in os.walk(target_dir):
                for afile in files:
                    if afile.endswith('.html'):
                        p = subdir + '/' + afile
                        file_path_structures.append([p, os.path.getmtime(p)])
        file_path_structures.sort(key=lambda x: x[0])
        logging.info('WebSite; ' + str(len(file_path_structures)) + ' file paths')
        return file_path_structures

    @staticmethod
    def _get_search_file_paths(target_dirs):
        file_paths = []
        print(')))  ))))', os.getcwd())
        print(')))  )))) }}', target_dirs)
        for target_dir in target_dirs:
          for subdir, dirs, files in os.walk(target_dir):
            print('=====  ==subdir= ', subdir, '+++++++dirs= ', dirs)
            for file in files:
                print('=======file =', file)
                p = os.path.join(subdir, file)
                print('=======p=', p)
                file_paths.append(p)
        file_paths.sort(key=lambda x: x)
        logging.info('WebSite; ' + str(len(file_paths)) + ' file paths')
        return file_paths

    @staticmethod
    def _get_web_pages(target_dirs):
        file_paths = WebSite._get_search_file_paths(target_dirs)
        web_pages = []
        for file_path in file_paths:
            if file_path.endswith('.html'):
                web_pages.append(WebPage(file_path))
        return web_pages

    def save_search_file_paths(self, save_file):
        with open(save_file, 'w') as f:
            f.writelines(x[0][5:] + '\n' for x in self.file_path_structures)

    @property
    def file_path_structures(self) -> list:
        return self.__file_path_structure

    @property
    def web_pages(self) -> list:
        return self.__web_pages

    def save_search_labels(self, save_file):
        with open(save_file, 'w') as f:
            f.write('')
        is_first = True
        for i, x in enumerate(self.file_path_structures):
            if 'problem' in x[0]:
                continue
            web_page = WebPage(x[0])
            indexes = web_page.search_indexes
            if len(indexes) > 0:
                with open(save_file, 'a') as f:
                    for attrs in indexes:
                        if not is_first:
                            f.write('\n')
                        else:
                            is_first = False
                        f.write(attrs[0])  # anchor label or table header
                        f.write('$$')
                        f.write(str(i))  # file index number
                        if len(attrs) > 1:
                            f.write('$$')
                            f.write(attrs[1])  # url
        logging.info('Created ' + save_file)

    def __str__(self) -> str:
        return f'WebSite: file_paths = {self.__file_path_structure} '
