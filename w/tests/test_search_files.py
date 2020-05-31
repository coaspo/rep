#!/usr/bin/env python3
from run_web_site_locally import start_local_server
import webbrowser


if __name__ == '__main__':
    start_local_server()
    webbrowser.open('http://localhost:8080/w/tests/test_search_files.html')
    print('opened html file to do local tests')
