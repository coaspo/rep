import sys
import pi.update_and_checkin
import logging
import atexit

logging_file_name = __file__ + '.log'
def exit_handler():
    with open(logging_file_name) as f:
        return f.read()




def config_log():
    if len(sys.argv) == 1:
        log_level = logging.INFO
        log_format = '%(message)s'
    else:
        log_level = logging.DEBUG
        log_format = '%(asctime)s - [%(levelname)s] - %(name)s - %(filename)s.%(funcName)s(%(lineno)d) - %(message)s'
    logging.basicConfig(filename=logging_file_name, filemode='w', level=log_level, format=log_format)


if __name__ == '__main__':
    atexit.register(exit_handler)
    config_log()
    pi.update_and_checkin.main('br1', logging_file_name)
