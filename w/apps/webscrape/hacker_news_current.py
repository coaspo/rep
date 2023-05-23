#!/usr/bin/env python3
import webbrowser

from hacker_news import *


def create_html_page(links, points, todays_date):
    html = "<html><head><meta charset='UTF-8'></head><title>Hacker news sorted</title>\n<body>Point sorted  " + \
           f"links of <a href=\"{HACKER_NEWS_URL}\">{HACKER_NEWS_URL}</a>,   {todays_date}<pre>"
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
        year = today.year
        month = today.month
        year = today.year
        day = int(today.day)
        todays_date = f'{year}-{month:02d}-{day:02d}'
        print("Today's date:", todays_date)
        links, points, comments = \
            scrape_ycombinator_links(year, month, day, day, '')
        html = create_html_page(links, points, todays_date)
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
