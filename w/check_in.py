import pi.update_and_checkin
import logging

logging.basicConfig(filename=__file__ + '.log2', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.info('Started sdff')

if __name__ == '__main__':
    pi.update_and_checkin.main('br1')
