import unicodedata
import re
import os
import logging
import logging.handlers
import datetime
import json

LOG = logging.getLogger(__name__)
non_ltrs_regex = ''.join(['|\\' + x for x in r'[\^$.|?*+()'])  # regex special char's
non_ltrs_regex = non_ltrs_regex + ''.join(['|\\' + x for x in ',!@#$%&-_=:;"?<>/{}]]']) # other non-ltr char's
non_ltrs_regex = '\'|[0-9]+' + non_ltrs_regex
is_logget_set = False

class Config(dict):
    def __init__(self, config_file_path = None, **kw):
        if config_file_path is not None and kw != {}:
            raise Exception('ambiguous constructor arg - use file path or dict arg\'s')

        if config_file_path == '__file__':
            config_file_path = os.path.abspath(os.path.dirname(__file__))
        if config_file_path is not None:
            with open(config_file_path) as json_file:
                config_dict = json.load(json_file)
            super(Config, self).__init__(config_dict)
        elif kw != {}:
            super(Config, self).__init__(**kw)
        else:
            raise Exception('missing constructor arg - use file path or dict arg\'s')


def set_logger(config):
    if config == None or config.get('LOG_DIR') == None:
        raise Exception('config missing config parameter "log_dir"')
    if is_logget_set:
        return
    log_dir = config['LOG_DIR']
    log_level_config = config.get('LOG_LEVEL')
    log_levels = {'CRITICAL': 50, 'ERROR': 40, 'WARNING': 30 , 'INFO': 20, 'DEBUG': 10, 'NOTSET':0 }
    LOG_LEVEL = log_levels.get(log_level_config)
    is_log_dir_created = False
    if LOG_LEVEL is None:
       raise Exception(f'Invalid log flag: {log_level_config} in config_trans.json, use one of: '+ str(log_levels.keys()))
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
        is_log_dir_created = True
    year_month = str(datetime.datetime.today())[:7]
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", LOG_LEVEL))
    logFormatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)s - %(funcName)s() - %(message)s")
    global log_file_path
    log_file_path = log_dir + "/translator-" + year_month + ".log"
    handler = logging.FileHandler(log_file_path, 'a', 'utf-8')
    handler.setFormatter(logFormatter)
    root.addHandler(handler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    root.addHandler(consoleHandler)
    if is_log_dir_created:
        LOG.info(f'created log_dir: {log_dir}')
    is_logger_set = True

