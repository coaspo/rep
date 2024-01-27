#!/usr/bin/env python3
"""#>>> create_web_page(['l3', '<li>', '<a href="l2">l2</a>'], [10, 100, 50], [5, 10, 3], 2) '<html><head><meta
charset='UTF-8'></head><title>Hacker news sort</title>\\n<body>Top <a
href="https://news.ycombinator.com/">https://news.ycombinator.com/</a> links\\n2 top points:\\n<li>, 100 points \\n<a
href="l2">l2</a>, 50 points \\n\\n2 top comments:\\nl3, 5 comments \\n\\n2 top points*comments:\\n\\n2 top point
non-🦜/\U0001fab5/📰:\\n\\n🦜 twitter/facebook   \U0001fab5 BLOG   📰 news</pre></body></html>' """
import calendar
import datetime
import glob
import os
import random
import time
# import webbrowser
import bs4
import requests
import util
import re

HACKER_NEWS_URL = 'https://news.ycombinator.com/'
DEBUG = False
URL = 'not set'
if DEBUG:
    print('=== DEBUG IS TURNED ON ===')

MONTH_ABBRS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
MIN_POINTS = 200


def get_web_page(url: str):
    headers = {'Accept-Language' : "en-US", \
               'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",\
  #             'HTTP header Accept-Encoding' : "gzip, deflate", \
               'HTTP headers Accept' : "text/html"}
    headers = {'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
    try:
        page = requests.get(url, timeout=5, headers=headers)
    except:
        print('FAILED to read url,', url, '\n   waiting for 15 seconds before trying again ')
        time.sleep(15)
        page = requests.get(url, timeout=5, headers=headers)
    page = requests.get(url, timeout=5, headers=headers)
    html = page.text
    return html


def parse_web_page_text(text: str):
    lines = text.split('\n')
    is_previous_line_desc =  False
    descs = []
    points = []
    comments = []
    for line in lines:
      if is_previous_line_desc:
        points_i = 0
        comments_i = 0
        parts = line.split(' ')
        if parts[0].isnumeric():
          points_i = int(parts[0])
        points.append(points_i)
        if 'comments' in line:
          parts = line.split('|')
          parts = parts[2].strip().split('comments')
          comments_i = int(parts[0].strip())
        comments.append(comments_i)
      i = line.find('.')
      j = line.find('(')
      if i > -1 and  j > -1:
        desc = line[i+1:j].strip()  # line is numbered has link with description
        desc = re.sub('\[.*?\]', '', desc).strip()
        descs.append(desc)
        is_previous_line_desc = True
      else:
        is_previous_line_desc = False
    if len(descs) != len(points) != len(comments):
      raise ValueError('ERR descs/points/comments  ' \
                 +f'{len(descs)}/{len(points)}/{len(comments)} length not same')
    return descs, points, comments


def parse_web_page(html: str, prev_file_path):
    soup = bs4.BeautifulSoup(html, 'lxml')
    descs, points, comments =  parse_web_page_text(soup.get_text())
    links = extract_links(html ,descs)
    is_last_page = len(links) < 28
    print(f'  before filtering, {len(links)} links; prev_file_path:', prev_file_path)
    links_filtered, points_filtered, comments_filtered =[], [],[]
    if len(prev_file_path) == 0:
        previous_file_text = ''
    else:
        with open(prev_file_path) as f:
            previous_file_text = f.read()
    for i, link in enumerate(links):
      if 'http' not in links[i]:
        print('  Skipping (missing "http")', i, 'th link: "', links[i])
      elif len(previous_file_text) > 0 and links[i] in previous_file_text:
        print('  Skipping (is in previous file)', i, 'th link: "', links[i])
      else:
        links_filtered.append(links[i])
        points_filtered.append(points[i])
        comments_filtered.append(comments[i])
    num_of_links = len(links_filtered)
    num_of_removed_links = len(links) -num_of_links
    print(num_of_links, 'new links, ', num_of_removed_links, 'duplicate links removed')
    if DEBUG:
        [print('"',i,'"') for i in links_filtered]
    return links_filtered, points_filtered, comments_filtered, is_last_page

# <a href="https://github.com/apenwarr/blip">Blip: A tool for seeing your Internet latency</a>
def extract_links(html ,descs):
    links = []
    for desc in descs:
      i = html.find(desc)
      i_start = html.rfind('<', 0, i)
      i_end = html.find('</a>', i)+4
      link = html[i_start:i_end]
      links.append(link)
      # print(i, '--', html[i_start:i_end])
    if len(descs) != len(links):
      raise ValueError(f'ERR descs/links  {len(descs)}/{len(links)} length not same')
    return links


def get_url_desc(link):
    if 'https' not in link:
      link = link.replace('href="', 'href="https://news.ycombinator.com/')
    host, domain = util.get_host_and_domain(link)
    desc = ''
    desc += host
    if domain != 'io':
        desc += '.' + domain + ' ' + util.get_country(domain)

    if host == 'facebook' or host == 'linkedin' or host == 'twitter':
        desc = '🦜'
    elif '.edu' in link:
        desc = '🏫'
    if 'blog' in link:
        desc += ' 🪵'
    elif 'nature.com' in link or 'scien' in link or 'sci-news' in link or \
            'kolabtree' in link or 'scidev' in link or 'labbulletin' in link or \
            'popsci.com' in link or 'nasa' in link or 'nationalgeog' in link or \
            'aaas.org' in link or 'space.com' in link or 'pnas.org' in link or \
            'howstuffworks' in link or 'nautil.us' in link or 'pnas.org' in link or \
            'smithsonian' in link or 'wired' in link or 'phys.org' in link or \
            'sien' in link:
        desc += ' 🧪️'
    elif 'news' in link or 'cnn.com' in link or 'nytimes.com' in link or \
            'huffpost' in link or 'usatoday' in link or 'wsj.com' in link or \
            'politico' in link or 'reuters' in link or 'dailymail' in link or \
            'latimes' in link or 'reuters' in link or 'washingtonpost' in link or \
            'wsj.com' in link or 'theguardian' in link or 'usatoday' in link or \
            'npr.org' in link:
        desc += ' 📰'
    if 'java' in link or 'github' in link or 'linux' in link or 'computer' in link or '.net' in link or \
            '.dev' in link or '.codes' in link or '.engineer' in link or '.software' in link or \
            'apple.com' in link or 'microsoft' in link or 'google' in link:
        desc += ' 💻'
    if '.pdf' in link:
        desc += ' 📄'
    if 'video' in link or 'youtube' in link:
        desc += '🎞️'
    return desc.strip()


def get_url_legend(html):
    legend = 'Legend:   '
    if '🦜' in html:
        legend += '🦜 twitter/facebook'
    if '🪵' in html:
        legend += '   🪵 BLOG'
    if '🎞' in html:
        legend += '   🎞️ youtube'
    if '🏫' in html:
        legend += '   🏫 .edu'
    if '🧪️' in html:
        legend += '   🧪️ science'
    if '📰' in html:
        legend += '   📰 news'
    if '📄' in html:
        legend += '   📄 PDF'
    if '💻' in html:
        legend += '   💻 computer'
    return legend


def scrape_ycombinator_links(year, month, day_start, day_end, prev_file_path):
    links = []
    points = []
    comments = []
    day_start = int(day_start)
    for day in range(day_start, day_end + 1):
        publish_date = f'{year}-{month:02d}-{day:02d}'
        print('Scraping', publish_date)
        url_sfx = 'front?day=' + publish_date
        ith_page = 1
        while True:
            URL = HACKER_NEWS_URL + url_sfx + '&p=' + str(ith_page)
            # example: URL = 'https://news.ycombinator.com/front?day=2022-01-01&p=1'
            print(f' {URL}')
            if not day_start == day_end:
                sec =  random.choice([5, 10, 20, 15, 3, 8])
                time.sleep(sec)  # spoof webscrape detection
            html = get_web_page(URL)
            links_i, points_i, comments_i, is_last_page = parse_web_page(html, prev_file_path)
            if len(links_i) == 0:
                break
            elif ith_page > 4:
                print('  possible ERR, more than 4 pages scanned')
                break
            annotate_links_i(links_i, comments_i, points_i, publish_date)
            links += links_i
            points += points_i
            comments += comments_i
            ith_page += 1
            if is_last_page:
                break
    print('scraped', len(links), 'links')
    return links, points, comments


def annotate_links_i(links_i, comments_i, points_i, publish_date):
    for j in range(len(links_i)):
        link = str(links_i[j])
        title = '" ' + 'title="' + str(points_i[j]) + ' pts, ' \
                + str(comments_i[j]) + ' comments ' \
                + publish_date + '">'
        if DEBUG:
            print('+++', j, '==', link, title)
        link = link.replace('">', title)
        desc = get_url_desc(link)
        if desc != '':
            link += ' <b>' + desc + '</b>'
        # if is_link_valid(link):
        links_i[j] = link


def is_gossip_or_computer_related(link):
    return '🦜' in link or '🪵' in link or '📰' in link or '💻' in link \
           or 'apple.com' in link or 'gitlab' in link


def find_page_title(link):
    if '.pdf' in link:
        return ''
    i_start = link.find('https')
    i_end = link.find('">', i_start)
    url = link[i_start:i_end]
    if len(url) > 150:
        return ''
    try:
        html = get_web_page(url)
        i_start = html.find('<title>') + 7
        if i_start < 7:
            return ''
        i_end = html.find('</title>')
        title =  html[i_start:i_end].lower().strip()
        if 'not found' in title or '404' in title:
            return ''
        return title.title()
    except Exception as exc:
        return ''


def append_lines(html, sort_order, links, sfx, max_link_cnt, collected_links):
    zipped = zip(sort_order, links)
    links_sorted = list(zipped)
    links_sorted.sort(reverse=True, key=lambda y: y[0])
    if DEBUG:
        print('    ---append_lines; links_sorted 1:\n     ', links_sorted[0:1])
    i = 0
    filter_gossip = sfx == ''
    for x in links_sorted:
        link = x[1]
        if filter_gossip and is_gossip_or_computer_related(link):
            continue
        if link not in collected_links:
            labeled_link = link
            title = find_page_title(labeled_link)
            if title in labeled_link:
                title = ''
            else:
                labeled_link = labeled_link.replace(title, '...')
            html += labeled_link + ', ' + "{:,}".format(x[0]) + sfx + ' ' + title + '\n'
            collected_links.append(link)
            i += 1
            if i == max_link_cnt:
                break
    print(  "    appended top", i, "links")
    return html


current_date = datetime.datetime.now()
print(current_date.isoformat())
def create_web_page(links, points, comments, prev_file_path, next_file_path, top_count):
    current_date = datetime.datetime.now().isoformat()
    html = "<html><head><meta charset='UTF-8'></head><title>Hacker news sort</title>\n<body>Top " + \
           f"<a href=\"{HACKER_NEWS_URL}\">{HACKER_NEWS_URL}</a> links \"{current_date}\" &#8198; &#8198; &#8198; &#8198;"
    if prev_file_path is not None:
        html += f"<a href=\"{prev_file_path}\">prev</a> &#8198; &#8198;" + \
                f"<a href=\"{next_file_path}\">next</a> &#8198; &#8198; &#8198; &#8198;" + \
                "<a href=\"./top_of_all.html\">top of all</a>"
    html += '&#8198; &#8198; &#8198; created ' + str(datetime.date.today())
    print('  append top points')
    html += '<pre> \n' + str(top_count) + ' top points:\n'
    collected_links = []
    html = append_lines(html, points, links, ' points', top_count, collected_links)

    print('  append top comments')
    html += '\n' + str(top_count) + ' top comments:\n'
    html = append_lines(html, comments, links, ' comments', top_count, collected_links)

    print('  append non-🦜/🪵/📰/💻 points')
    html += '\n' + str(top_count) + ' top non-🦜/🪵/📰/💻 points:\n'
    html = append_lines(html, points, links, '', top_count, collected_links)

    html += '\n' + get_url_legend(html)
    html += '</pre></body></html>'
    return html.replace('\r', '')


def read_all_previous_sorts():
    links = []
    points = []
    comments = []
    html_files = glob.glob('./hacker_news/*.html')
    html_files.sort()
    for file_i in html_files:
        if 'top_of_all.html' in file_i or 'tmp' in file_i:
            continue
        print('  reading', file_i)
        with open(file_i) as f:
            lines = f.readlines()
        links_i = [x for x in lines if x.startswith('<a href="http')]
        for link in links_i:
            i2 = link.find('</a>') + 4
            link = link[:i2]
            desc = get_url_desc(link)
            if desc != '':
                link += ' <b>' + desc + '</b>'
            links.append(link)
            i1 = link.find('title="') + 7  # title="263 pts, 142 comments">
            i2 = link.find(' pts,', i1)
            point = int(link[i1:i2])
            points.append(point)
            i1 = i2 + 6
            i2 = link.find(' comments', i1)
            comment = int(link[i1:i2])
            comments.append(comment)
    if DEBUG:
        print(' ---read_all_previous_sorts; ', len(points), len(comments), len(links))
    return links, points, comments


def write_file(html, file_path):
    with open(file_path, 'w') as f:
        f.write(html)
    print('Created', file_path, len(html), ' characters\n')


def prev_next_dates(month, month_range):
    year = datetime.datetime.today().year
    if month_range == 1:
        prev_month = month - 1 if month > 1 else 12
        prev_day_start = 21
        test_date = datetime.datetime(year, prev_month, 1)
        prev_day_end = calendar.monthrange(test_date.year, test_date.month)[1]

        next_month = month
        next_day_start = 11
        next_day_end = 20

    elif month_range == 2:
        prev_month = month
        prev_day_start = 1
        prev_day_end = 10

        next_month = month
        next_day_start = 21
        test_date = datetime.datetime(year, next_month, 1)
        next_day_end = calendar.monthrange(test_date.year, test_date.month)[1]
    else:
        prev_month = month
        prev_day_start = 11
        prev_day_end = 20

        next_month = month + 1 if month < 12 else 1
        next_day_start = 1
        next_day_end = 10
    return prev_month, prev_day_start, prev_day_end, next_month, next_day_start, next_day_end


def date_parameters(month_abr, month_range):
    if month_abr not in MONTH_ABBRS:
        raise ValueError(month_abr + ' is not in: ' + str(MONTH_ABBRS))
    if month_range not in [1, 2, 3]:
        raise ValueError(month_range + ' is not 1,2,3')
    month = MONTH_ABBRS.index(month_abr) + 1
    today = datetime.datetime.today()
    if month_range == 1:
        day_start = 1
        day_end = 10
    elif month_range == 2:
        day_start = 11
        day_end = 20
    else:
        day_start = 21
        test_date = datetime.datetime(today.year, month, 1)
        day_end = calendar.monthrange(test_date.year, test_date.month)[1]
    file_path = f'./hacker_news/{str(month).zfill(2)}_{month_abr}_{str(day_start).zfill(2)}-{day_end}.html'
    prev_month, prev_day_start, prev_day_end, next_month, next_day_start, next_day_end = \
        prev_next_dates(month, month_range)
    prev_day_start = str(prev_day_start).zfill(2)
    next_day_start = str(next_day_start).zfill(2)
    prev_file_path = f'./hacker_news/{str(prev_month).zfill(2)}_{MONTH_ABBRS[prev_month - 1]}_{prev_day_start}-{prev_day_end}.html'
    next_file_path = f'./hacker_news/{str(next_month).zfill(2)}_{MONTH_ABBRS[next_month - 1]}_{next_day_start}-{next_day_end}.html'
    print(' --file_paths,  current:', file_path, '  prev:', prev_file_path, '  next:', next_file_path)
    year = today.year - 1 if month > today.month else today.year
    return file_path, year, month, day_start, day_end, prev_file_path, next_file_path


def get_user_input():
    while True:
        month = input('Enter 1-st 3 ltrs or name of month: ').lower()[0:3]
        if month in MONTH_ABBRS:
            break
        print('invalid input')
    while True:
        period = input('Enter mon{}th period (1,2,3): ')
        if period.isdigit() and 0 < int(period) < 4:
            break
        print('invalid period')
    return month, int(period)


def get_next_month_period():
    files = os.listdir("./hacker_news")
    files = [x for x in files if x[0:2].isdigit()]  # remove unnumbered files
    mod_time  =  [os.path.getmtime("./hacker_news/" + x) for x in files]
    files = [x for _,x in sorted(zip(mod_time,files))]
    last_month = files[-1][3:6]
    last_start_date = files[-1][7:9]
    print(files[-1], last_month, last_start_date)
    if last_start_date == '01':
        period = 2
        month = last_month
    elif last_start_date == '11':
        period = 3
        month = last_month
    else:
        period = 1
        index = MONTH_ABBRS.index(last_month) + 1
        if index == len(MONTH_ABBRS):
            index = 0
        month = MONTH_ABBRS[index]
    print('new month/period: ', month, str(period))
    return month, period


def main():
    try:
        print('Started hacker_news.py')

        file_path = './hacker_news/top_of_all.html'
        print ("  1/2 Updating", file_path)
        links, points, comments = \
            read_all_previous_sorts()
        html = create_web_page(links, points, comments, None, None, top_count=40)
        write_file(html, file_path)
        # webbrowser.open_new_tab(file_path)
        # month, period = 'apr', 1   #
        # month, period = get_user_input()

        month, period = get_next_month_period()
        file_path, year, month, day_start, day_end, prev_file_path, next_file_path = \
            date_parameters(month, period)
        print ("  2/2 Updating", file_path)
        links, points, comments = \
            scrape_ycombinator_links(year, month, day_start, day_end, prev_file_path)
        html = create_web_page(links, points, comments, prev_file_path, next_file_path, top_count=20)
        write_file(html, file_path)

        print('Done')
    except Exception as exc:
        print(exc)
        import traceback
        traceback.print_exc()
        print('URL=', URL)


if __name__ == "__main__":
    main()
