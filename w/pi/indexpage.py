import logging
import shutil
import traceback

from pi.contentspage import ContentsPage


class IndexPage:
    @staticmethod
    def update_links(file_paths):
        with open('index.html') as f:
            lines = f.read().splitlines()
        try:
            with open('index.html', 'w') as f:
                for line in lines:
                    if 'href' in line and './' in line:
                        if '</a>' not in line or '<a ' not in line:
                            raise Exception('Missing "<a " "</a>" or ".html" in: ' + line)
                        i = line.find('<a ')
                        ii = line.index('</a>', i) + 4
                        link = line[i:ii]
                        (label, url) = IndexPage._extract_url_label(link)

                        i = url.rfind('/') + 1
                        i2 = url.rfind('.html')
                        file_desc = url[i:i2].replace('_', ' ')
                        line = line.replace('>' + label + '<', '>' + file_desc + '<')
                    f.write(line + '\n')
        except Exception as e:
            logging.error(str(e))
            print(traceback.format_exc())
            with open('index.html', 'w') as f:
                for line in lines:
                    f.write(line + '\n')
            raise
        logging.info('Updated index.html')

    @staticmethod
    def update(web_pages: str):
        shutil.copyfile('index.html', 'index.tmp')
        try:
            with open('index.tmp', 'w') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith('<br><br>'):
                        f.write(line + '\n')
                        ContentsPage._append_version_and_content_links(version, file_paths, f)
                        break
                    f.write(line + '\n')
        except Exception:
            logging.exception('')
            print(traceback.format_exc())
            with open('contents.html', 'w') as f:
                for line in lines:
                    f.write(line + '\n')
            raise
        logging.info('Updated index.html')


    @staticmethod
    def _extract_url_label(link):
        link = link.replace('href= ', 'href=')
        quote = '"' if link.find('href="') > -1 else "'"
        i = link.index('href=' + quote) + 6
        i2 = link.index(quote, i)
        url = link[i:i2]
        i = link.index('>', i2) + 1
        i2 = link.index('</a>', i)
        label = link[i:i2].lower().strip()
        attrs = (label, url)
        return attrs


if __name__ == '__main__':
    import doctest

    # This runs just a couple of tests;
    doctest.testmod()
