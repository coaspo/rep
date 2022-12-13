#!/usr/bin/env python3
import webbrowser

from hacker_news import *


def create_html_page(links, points, month, day):
    html = "<html><head><meta charset='UTF-8'></head><title>Hacker news sorted</title>\n<body>Point sorted  " + \
           f"links of <a href=\"{HACKER_NEWS_URL}\">{HACKER_NEWS_URL}</a>,  date[m/d]: {month}/{day}<pre>"
    collected_links = []
    html = append_lines(html, points, links, ' points', 10_000, collected_links)
    html += '\n' + get_url_legend(html)
    html += '</pre></body></html>'
    return html.replace('\r', '')


def main():
    try:
        print('Started', __name__)
        import hacker_news
        hacker_news.DEBUG = True
        hacker_news.MIN_POINTS = 0
        from datetime import datetime
        today = datetime.today()
        month = today.month - 1
        day = int(today.day)
        if hacker_news.DEBUG:
            print(f'month:{month:02d}  day: {day:02d}')
        links, points, comments = \
            scrape_ycombinator_links(month, day, day)
        html = create_html_page(links, points, month, day)
        file_path = './hacker_news/tmp_current_sorted.html'
        write_file(html, file_path)
        print('Created', file_path, '\n  wait ... opening it in browser')
        webbrowser.open_new_tab(file_path)
        print('Done')
    except Exception as exc:
        print(exc)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
