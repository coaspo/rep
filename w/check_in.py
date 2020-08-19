import pi.update_and_checkin
from pi.log import config_log

if __name__ == '__main__':
    config_log(__file__ + '.log')
    pi.update_and_checkin.main('br1')
