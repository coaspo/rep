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
                        prev_sub_dir = ''
                        for page in webpages:
                            sub_dir = page.sub_dir.capitalize()
                            if len(sub_dir) > 0:
                                sub_dir += ':'
                            if sub_dir == '':
                                f.write('\n<tr><td colspan="2">')
                            else:
                                if sub_dir != prev_sub_dir:
                                    f.write('\n<tr><td>' + sub_dir + '</td><td>')
                                else:
                                    f.write('\n<tr><td></td><td>')
                            prev_sub_dir = sub_dir
                            i = page.link.index('>') + 1
                            link = page.link[:i] + page.link[i:i+1].upper() + page.link[i+1:]
                            f.write(link)
                            f.write('</td></tr>')
                        while line != '<!--*/END-->':  # remove previous lines
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
