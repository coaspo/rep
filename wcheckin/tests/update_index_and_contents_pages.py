import os
import traceback
import wpy.controller

if __name__ == '__main__':
    if os.getcwd().endswith('/tests'):
        os.chdir('..')
    try:
        wpy.controller.update_index_and_contents_pages()
    except Exception as e:
        print(traceback.format_exc())
