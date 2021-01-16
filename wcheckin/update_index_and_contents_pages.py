import traceback
import wpy.controller

if __name__ == '__main__':
    try:
        wpy.controller.update_index_and_contents_pages()
    except Exception as e:
        print(traceback.format_exc())
