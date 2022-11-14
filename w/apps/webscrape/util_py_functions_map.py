#!/usr/bin/env python3
import webbrowser

from hacker_news import *


def main():
    try:
        print('started')
        files = []
        for file in glob.iglob('./*.py', recursive=True):
            files.append(file[2:-3])
            print(file[2:-3])
        file = input("Enter one of the following files names: " + str(files))
        print('done')
    except Exception as exc:
        print(exc)
        import traceback
        traceback.print_exc()



if __name__ == "__main__":
    main()
