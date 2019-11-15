import logging
import ltrans.util
import datetime
import re


def test_set_logger():
    config = {'LOG_DIR': '../../tmp', 'LOG_LEVEL': 'INFO'}
    ltrans.util.set_logger(config, )
    LOG = logging.getLogger(__name__)
    ts = str(datetime.datetime.now())[:14]
    LOG.info(f'This is a test {ts}')

    with open(ltrans.util.log_file_path) as f:
        file_txt = f.read()
    assert ts in file_txt
    assert 'test_set_logger() - This is a test' in file_txt

def test_config_wo_file_path__for_testing():
    config = ltrans.util.Config(a=123, b='abc')
    assert config['a'] == 123
    assert config['b'] == 'abc'


def test_config():
    config_txt = '''
{
"PRIMARY_DESTINATION_LANGUAGE": "Klingon",
"DICTIONARY_DIR": "my-dict-dir"
}'''
    test_file_path = '../../tmp/config.json'
    with open(test_file_path, 'w') as f:
        f.write(config_txt)

    config = ltrans.util.Config(test_file_path)
    assert config['PRIMARY_DESTINATION_LANGUAGE'] == 'Klingon'
    assert config['DICTIONARY_DIR'] == 'my-dict-dir'


def test_non_ltrs_regex():
    actual = re.sub(ltrans.util.non_ltrs_regex, '', 'ab cd')
    assert actual == 'ab cd'
    actual = re.sub(ltrans.util.non_ltrs_regex, '', 'ab' + r'[\^$.|?*+()' + ' cd')
    assert actual == 'ab cd'
    actual = re.sub(ltrans.util.non_ltrs_regex, '', 'ab ,!@#$%&-_=:;"?<>/{}]] cd')
    assert actual == 'ab  cd'
