import logging
import traceback


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
                    if line.startswith('<!--*'):
                        f.write('\n' + line)
                        i_end = line.index('-->')
                        topic = line[6:i_end]
                        webpages = website.web_page_dict[topic]
                        is_first = True
                        for page in webpages:
                            f.write('\n<tr><td>')
                            if page.sub_topic == '':
                                f.write(page.link)
                            else:
                                if is_first:
                                    f.write(page.sub_topic + '</td><td>' + page.link)
                                else:
                                    f.write('</td><td>' + page.link)
                            f.write('</td></tr>')
                        while line != '<!--*/END-->':
                            j += 1
                            line = lines[j]
                        f.write('\n<!--*/END-->')
                    else:
                        f.write('\n' + line)
                    j += 1
        except Exception as e:
            logging.error(str(e))
            print('ERR line: ', line, '\n', traceback.format_exc())
            with open(file_path, 'w') as f:
                for line in lines:
                    f.write(line + '\n')
            raise e
        logging.info('Updated index.html')

    @staticmethod
    def _extract_url_label(link):
        try:
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
        except Exception:
            logging.exception('')
            print('ERR link: ', link, '\n', traceback.format_exc())
            raise


if __name__ == '__main__':
    import doctest

    # This runs just a couple of tests;
    doctest.testmod()
