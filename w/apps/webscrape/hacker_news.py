#!/usr/bin/env python3
"""#>>> create_web_page(['l3', '<li>', '<a href="l2">l2</a>'], [10, 100, 50], [5, 10, 3], 2) '<html><head><meta
charset='UTF-8'></head><title>Hacker news sort</title>\\n<body>Top <a
href="https://news.ycombinator.com/">https://news.ycombinator.com/</a> links\\n2 top points:\\n<li>, 100 points \\n<a
href="l2">l2</a>, 50 points \\n\\n2 top comments:\\nl3, 5 comments \\n\\n2 top points*comments:\\n\\n2 top point
non-🦜/\U0001fab5/📰:\\n\\n🦜 twitter/facebook   \U0001fab5 BLOG   📰 news</pre></body></html>' """
import calendar
import datetime
import glob
import time
# import webbrowser
import bs4
import requests
import util

HACKER_NEWS_URL = 'https://news.ycombinator.com/'
DEBUG = 1
MONTH_ABRS = ['jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
MIN_POINTS = 200


def get_web_page(url: str):
    time.sleep(1)
    page = requests.get(url)
    html = page.text
    return html


def parse_web_page(html: str):
    soup = bs4.BeautifulSoup(html, 'lxml')
    table = soup.find_all('table')[0]
    links = table.findAll('a', {"class": "titlelink"})
    is_last_page = len(links) < 30
    descs = table.findAll('td', {"class": "subtext"})

    print(f'  BeautifulSoup extracted {len(links)} links, {len(descs)} desc, in {len(html)} HTML chars')
    if len(links) == 0:
        print(' ERR did not find any links; html=\n', html)
    if len(links) != len(descs):
        raise ValueError('ERR len links/descs: ' + str(len(links)) + '!=' + str(len(descs)))
    points = []
    comments = []
    extract_points_and_comments(comments, descs, links, points)
    print(f'  after filtering {len(links)} links, {len(descs)} desc')
    return links, points, comments, is_last_page


def extract_points_and_comments(comments, descs, links, points):
    i = 0
    while i < len(links):
        point_spans = descs[i].find_all('span', {"class": "score"})

        if len(point_spans) == 0 or 'ycombinator.com' in links[i] \
                or 'http' not in str(links[i]):
            print('    removed; no points/https;', str(links[i])[1:50])
            del (descs[i])
            del (links[i])
            continue
        point = int(point_spans[0].text[:-7])
        if point < MIN_POINTS:
            print(f'   removed link {point} < {MIN_POINTS}(min)')
            del (descs[i])
            del (links[i])
            continue
        points.append(point)
        txt = str(descs[i])
        i_end = txt.find('comments') - 1
        i_start = txt.find('>', i_end - 20) + 1
        comment = int(txt[i_start:i_end])
        comments.append(comment)
        links[i] = str(links[i]).replace('class="titlelink" ', '')
        i += 1


def get_url_desc(link):
    host, domain = util.get_host_and_domain(link)
    desc = ''
    if host == 'facebook' or host == 'linkedin' or host == 'twitter':
        desc = '🦜'
    elif host == 'youtube':
        desc = '🎞️'
    elif '.edu' in link:
        desc = '🏫'
    desc += host
    if domain != 'io':
        desc += '.' + domain + ' ' + util.get_country(domain)

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
            '.dev' in link or '.codes' in link or '.engineer' in link or '.software' in link:
        desc += ' 💻'
    if '.pdf' in link:
        desc += ' PDF'
    if 'video' in link or 'youtube' in link:
        desc += '🎞️'
    return desc.strip()


def get_url_legend(html):
    legend = 'Legend:   '
    if '🦜' in html:
        legend += '🦜 twitter/facebook'
    if '🪵' in html:
        legend += '   🪵 BLOG'
    if '🎞️' in html:
        legend += '   🎞️ youtube'
    if '🏫' in html:
        legend += '   🏫 .edu'
    if '🧪️' in html:
        legend += '   🧪️ science'
    if '📰' in html:
        legend += '   📰 news'
    if '💻' in html:
        legend += '   💻 computer'
    return legend


def scrape_ycombinator_links(month, day_start, day_end):
    year = datetime.datetime.today().year
    links = []
    points = []
    comments = []
    for day in range(day_start, day_end + 1):
        publish_date = f'{year}-{month:02d}-{day:02d}'
        print('Scraping', publish_date)
        url_sfx = 'front?day=' + publish_date
        ith_page = 1
        while True:
            url = HACKER_NEWS_URL + url_sfx + '&p=' + str(ith_page)
            # example: url = 'https://news.ycombinator.com/front?day=2022-01-01&p=1'
            if DEBUG:
                print(f' ----page:{ith_page}, url:{url} ----')
            html = get_web_page(url)
            links_i, points_i, comments_i, is_last_page = parse_web_page(html)
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
    return links, points, comments


def annotate_links_i(links_i, comments_i, points_i, publish_date):
    for j in range(len(links_i)):
        link = str(links_i[j])
        title = '" ' + 'title="' + str(points_i[j]) + ' pts, ' \
                + str(comments_i[j]) + ' comments ' \
                + publish_date + '">'
        link = link.replace('">', title)
        desc = get_url_desc(link)
        if desc != '':
            link += ' <b>' + desc + '</b>'
        # if is_link_valid(link):
        links_i[j] = link


def append_lines(html, sort_order, links, sfx, max_link_cnt, collected_links):
    zipped = zip(sort_order, links)
    links_sorted = list(zipped)
    links_sorted.sort(reverse=True, key=lambda y: y[0])
    # if DEBUG:
    #     print('    ---append_lines; links_sorted 1:\n     ', links_sorted[0:1])
    i = 0
    is_non_etc = sfx == '\n'
    for x in links_sorted:
        link = x[1]
        if is_non_etc and ('🦜' in link or '🪵' in link or '📰' in link or '💻' in link):
            continue
        if link not in collected_links:
            html += link + ', ' + "{:,}".format(x[0]) + sfx
            collected_links.append(link)
            i += 1
            if i == max_link_cnt:
                break
    return html


def create_web_page(links, points, comments, prev_file_path, next_file_path, top_count):
    html = "<html><head><meta charset='UTF-8'></head><title>Hacker news sort</title>\n<body>Top" + \
           f"<a href=\"{HACKER_NEWS_URL}\">{HACKER_NEWS_URL}</a> links &#8198; &#8198; &#8198; &#8198;"
    if prev_file_path is not None:
        html += f"<a href=\"{prev_file_path}\">prev</a> &#8198; &#8198;" + \
                f"<a href=\"{next_file_path}\">next</a> &#8198; &#8198; &#8198; &#8198;" + \
                "<a href=\"./hacker_news/top_of_all.html\">top of all</a>"
    html += '<pre> \n' + str(top_count) + ' top points:\n'
    collected_links = []
    html = append_lines(html, points, links, ' points \n', top_count, collected_links)

    html += '\n' + str(top_count) + ' top comments:\n'
    html = append_lines(html, comments, links, ' comments \n', top_count, collected_links)

    html += '\n' + str(top_count) + ' top non-🦜/🪵/📰/💻 points:\n'
    html = append_lines(html, points, links, '\n', top_count, collected_links)

    html += '\n' + get_url_legend(html)
    html += '</pre></body></html>'
    return html.replace('\r', '')


def read_all_previous_sorts():
    links = []
    points = []
    comments = []
    html_files = glob.glob('./hacker_news/*.html')
    print(html_files)
    for file_i in html_files:
        if 'top_of_all.html' in file_i:
            continue
        print('read_all_previous_sorts', file_i)
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
    print('Created ', file_path)


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
        prev_day_end = 11

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
        next_day_end = 11,
    return prev_month, prev_day_start, prev_day_end, next_month, next_day_start, next_day_end


def date_parameters(month_abr, month_range):
    if month_abr not in MONTH_ABRS:
        raise ValueError(month_abr + ' is not in: ' + str(MONTH_ABRS))
    if month_range not in [1, 2, 3]:
        raise ValueError(month_range + ' is not 1,2,3')
    month = MONTH_ABRS.index(month_abr) + 1
    year = datetime.datetime.today().year
    if month_range == 1:
        day_start = 1
        day_end = 10
    elif month_range == 2:
        day_start = 11
        day_end = 20
    else:
        day_start = 21
        test_date = datetime.datetime(year, month, 1)
        day_end = calendar.monthrange(test_date.year, test_date.month)[1]
    file_path = f'./hacker_news/{str(month).zfill(2)}_{month_abr}_{day_start}-{day_end}.html'
    prev_month, prev_day_start, prev_day_end, next_month, next_day_start, next_day_end = \
        prev_next_dates(month, month_range)
    prev_file_path = f'./{str(prev_month).zfill(2)}_{MONTH_ABRS[prev_month - 1]}_{prev_day_start}-{prev_day_end}.html'
    next_file_path = f'./{str(next_month).zfill(2)}_{MONTH_ABRS[next_month - 1]}_{next_day_start}-{next_day_end}.html'
    print(' --file_path', file_path, prev_file_path, next_file_path)
    return file_path, month, day_start, day_end, prev_file_path, next_file_path


def get_user_input():
    while True:
        month = input('Enter 1-st 3 ltrs of month: ').lower()
        if month in MONTH_ABRS:
            break
        print('invalid input')
    while True:
        period = input('Enter month period (1,2,3): ')
        if period.isdigit() and 0 < int(period) < 4:
            break
        print('invalid period')
    return month, int(period)


def main():
    try:
        print('started')
        month, period = 'apr', 1   # get_user_input()
        file_path, month, day_start, day_end, prev_file_path, next_file_path = \
            date_parameters(month, period)
        links, points, comments = \
            scrape_ycombinator_links(month, day_start, day_end)
        html = create_web_page(links, points, comments, prev_file_path, next_file_path, top_count=20)
        write_file(html, file_path)

        links, points, comments = \
            read_all_previous_sorts()
        html = create_web_page(links, points, comments, None, None, top_count=40)
        write_file(html, './hacker_news/top_of_all.html')
        # webbrowser.open_new_tab(file_path)

        print('done')
    except Exception as exc:
        print(exc)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
