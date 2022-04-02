import logging
import traceback
from wpy.util import Util


class IndexPage:

    @staticmethod
    def update_links(website, file_path):
        with open(file_path) as f:
            lines = f.read().splitlines()
        line = 'NA'
        try:
            with open(file_path, 'w') as f:
                f.write(lines[0])
                j = 1
                while j < len(lines):
                    line = lines[j]
                    i_start = line.find('<!--*/')
                    if i_start < 0:
                        f.write('\n' + line)
                    else:
                        f.write('\n' + line + '\n')
                        i_end = line.index('-->')
                        topic = line[i_start + 6:i_end]
                        print('IndexPage.update_links() topic=', topic)
                        webpages = website.web_page_dict[topic]
                        txt = Util.get_web_page_links(webpages, False)
                        f.write(txt)
                        while line.find('<!--*/END-->') < 0:  # remove previous lines
                            j += 1
                            line = lines[j]
                        f.write('\n<!--*/END-->')
                    j += 1

        except Exception as e:
            logging.error(str(e))
            print('ERR line: ', line, '\n', traceback.format_exc())
            with open(file_path, 'w') as f:
                for line in lines:
                    f.write(line + '\n')
            raise e
        logging.info('Updated index.html')



if __name__ == '__main__':
    import doctest

    # This runs just a couple of tests;
    doctest.testmod()
