import sys
import pi.update_and_checkin
import logging


def config_log():
    if len(sys.argv) == 1:
        log_level = logging.INFO
        log_format = '%(message)s'
    else:
        log_level = logging.DEBUG
        log_format = '%(asctime)s - [%(levelname)s] - %(name)s - %(filename)s.%(funcName)s(%(lineno)d) - %(message)s'
    print(1111111111, log_format)
    log_file_name2 = __file__ + '.log'
    logging.basicConfig(filename=log_file_name2, filemode='w', level=log_level, format=log_format)
    return log_file_name2


if __name__ == '__main__':
    log_file_name = config_log()
    pi.update_and_checkin.main('br1', log_file_name)
