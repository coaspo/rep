from quz.persistence import file_prefixes
from quz.util import set_logger
from tests.t_util import recreate_tmp_dir
import json

TMP_DIR = recreate_tmp_dir(__file__)

CONFIG = {'LOG_DIR': TMP_DIR, 'LOG_LEVEL': 'CRITICAL'}
set_logger(CONFIG)


def test_no_latest_work_file():
    with open(TMP_DIR + r'\quiz-.1.json', 'w') as f:
        f.write('dummy content')
    with open(TMP_DIR + r'\quiz-desc.2.json', 'w') as f:
        f.write('dummy content')
    with open(TMP_DIR + r'\java-.3.json', 'w') as f:
        f.write('dummy content')
    latest_category, categories = file_prefixes(TMP_DIR)
    assert latest_category == 'java'
    assert categories == ['java', 'quiz']


def test_with_latest_work_file():
    with open(TMP_DIR + r'\scrum-agile.1.json', 'w') as f:
        f.write('dummy content')
    latest_work = {'LATEST_FILE_PREFIX': 'quiz'}
    with open(TMP_DIR + r'\latest_work.json', 'w') as f:
        json.dump(latest_work, f)
    latest_category, categories = file_prefixes(TMP_DIR)
    assert latest_category == 'quiz'
    assert categories == ['java', 'quiz', 'scrum']
