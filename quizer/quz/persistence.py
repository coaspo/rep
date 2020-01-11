import abc
import calendar
import datetime
import glob
import json
import logging
import os.path
import traceback
from abc import ABC

log = logging.getLogger(__name__)


class AbstractPersistence(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def save(self, quiz: dict) -> str:
        pass

    @abc.abstractmethod
    def get(self) -> tuple:
        pass

    @abc.abstractmethod
    def get_next(self) -> tuple:
        pass

    @abc.abstractmethod
    def get_previous(self) -> tuple:
        pass

    @abc.abstractmethod
    def delete(self) -> tuple:
        pass

    @abc.abstractmethod
    def update(self, quiz: dict) -> tuple:
        pass


class FileStorage:
    def __init__(self, config: dict):
        self._config = config
        self._save_dir = self._latest_file_number = self._file_paths_index = self._files_paths = None
        self._initialize()

    def _initialize(self):
        self._save_dir, err_msg = self._get_save_dir()
        if err_msg is None:
            self._latest_file_number, self._files_paths = FileStorage._get_file_paths(self._save_dir)
            self._file_paths_index = len(self._files_paths) - 1
        else:
            raise Exception('FileStorage failed - ' + err_msg)

    def _get_save_dir(self) -> tuple:
        if self._config is None or self._config.get('SAVED_QUIZES_DIR') is None:
            return None, 'config missing parameter "SAVED_QUIZES_DIR"'
        save_dir = self._config['SAVED_QUIZES_DIR']
        if save_dir.startswith("./"):
            save_dir = os.path.dirname(__file__) + save_dir[1:]
        save_dir = os.path.abspath(save_dir)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'dict_file_path={save_dir}')

        if not os.path.exists(save_dir):
            try:
                os.mkdir(save_dir, 0o777)
                log.info(f'Created dir ' + save_dir)
            except Exception as e:
                trace = str(e) + '\n\t' + traceback.format_exc()
                log.error(trace)
                return None, str(e)
        return save_dir, None

    @staticmethod
    def _get_file_paths(save_dir: str) -> tuple:
        file_paths = glob.glob(save_dir + '/*.json')
        if len(file_paths) == 0:
            return 0, []

        file_paths.sort()
        quiz_nums = []
        proper_formatted_file_paths = []
        for file_path in file_paths:
            x = file_path.split('.')
            if len(x) > 0 and x[1].isnumeric():
                quiz_nums.append(int(x[1]))
            proper_formatted_file_paths.append(file_path)

        if len(quiz_nums) == 0:
            latest_file_number = 0
        else:
            latest_file_number = max(quiz_nums)
        return latest_file_number, proper_formatted_file_paths

    def save(self, quiz: dict) -> str:
        print('++++++++++++\n', dict)
        quiz_number = self._latest_file_number + 1
        file_index = self._file_paths_index + 1
        file_path = self._save_dir + '/quiz.' + str(quiz_number) + '.json'
        if file_index > len(self._files_paths):
            raise SystemError(
                f'Index Error:  _file_path_index= {file_index}' +
                f'(len(_files_paths)={len(self._files_paths)})')
        with open(file_path, "w", encoding='utf8') as f:
            json.dump(quiz, f, ensure_ascii=False, sort_keys=False, indent=0)

        self._files_paths.append(file_path)
        self._latest_file_number = quiz_number
        self._file_paths_index = file_index
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'file_path={file_path}')
        return file_path

    def update(self, quiz: dict) -> tuple:
        with open(self._files_paths[self._file_paths_index], "w", encoding='utf8') as f:
            json.dump(quiz, f, ensure_ascii=False, sort_keys=False, indent=0)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'file_path={self._files_paths[self._file_paths_index]}')
        return self._file_info(), 'Updated: ' + self._file_name()

    def increment_file_index(self):
        self._validate_file_paths()
        if self._file_paths_index != len(self._files_paths) - 1:
            self._file_paths_index += 1

    def decrement_file_index(self):
        self._validate_file_paths()
        if self._file_paths_index != 0:
            self._file_paths_index -= 1

    def _validate_file_paths(self):
        if len(self._files_paths) == 0:
            raise FileExistsError(f'There are no quiz files in: {self._save_dir}')

    def read(self) -> tuple:
        file_path = self._files_paths[self._file_paths_index]
        try:
            with open(file_path, "r", encoding='utf8') as f:
                quiz_dict = json.load(f)
        except OSError:
            self.initialize()
            file_path = self._files_paths[self._file_paths_index]
            with open(file_path, "r", encoding='utf8') as f:
                quiz = json.load(f)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'file_path={file_path}\nquiz_dict=\n{quiz_dict}')
        return self._file_info(), self._file_name(), quiz_dict

    def delete(self) -> str:
        self._validate_file_paths()
        file_path = self._files_paths[self._file_paths_index]
        os.remove(file_path)
        del self._files_paths[self._file_paths_index]
        self._file_paths_index -= 1
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'file_path={file_path}')
        return file_path

    def _file_name(self):
        file_num = str(self._file_paths_index + 1)
        file_path = self._files_paths[self._file_paths_index]
        file_name = os.path.basename(file_path)
        file_name = file_name[:len(file_name) - 5]
        info = file_num + '.  ' + file_name
        return info

    def _file_info(self):
        file_path = self._files_paths[self._file_paths_index]
        seconds_since_created = os.path.getmtime(file_path)
        create_ts = datetime.datetime.utcfromtimestamp(seconds_since_created).isoformat()[:22]
        # remove T in, for example, create_ts = 2019-12-11T19:20:48.85
        create_ts = create_ts[2:10] + ' ' + create_ts[11:16]
        day_index = datetime.datetime.utcfromtimestamp(seconds_since_created).weekday()
        count = str(self._file_paths_index + 1) + '/' + str(len(self._files_paths))
        info = count + '  ' + file_path + '  ' + create_ts + ' ' + calendar.day_name[day_index][0:3]
        return info


class Persistence(AbstractPersistence):
    file_storage_err_msg = True

    def __init__(self, config: dict):
        try:
            self._file_storage = FileStorage(config)
            Persistence.file_storage_err_msg = None
        except Exception as e:
            Persistence.file_storage_err_msg = str(e)

    @staticmethod
    def validate_file_storage():
        if Persistence.file_storage_err_msg is not None:
            raise Exception(Persistence.file_storage_err_msg)

    def save(self, quiz: dict) -> str:
        Persistence.validate_file_storage()
        file_path = self._file_storage.save(dict)
        return 'Saved quiz text in: ' + file_path

    def get(self) -> tuple:
        Persistence.validate_file_storage()
        status_msg, file_name, quiz = self._file_storage.read()
        return status_msg, file_name, quiz

    def get_next(self) -> tuple:
        Persistence.validate_file_storage()
        self._file_storage.increment_file_index()
        status_msg, file_name, quiz = self._file_storage.read()
        return status_msg, file_name, quiz

    def get_previous(self) -> tuple:
        Persistence.validate_file_storage()
        self._file_storage.decrement_file_index()
        status_msg, file_name, quiz = self._file_storage.read()
        return status_msg, file_name, quiz

    def delete(self) -> tuple:
        Persistence.validate_file_storage()
        return self._file_storage.delete(), 'Deleted file'

    def update(self, quiz: dict) -> tuple:
        Persistence.validate_file_storage()
        file_info, update_msg = self._file_storage.update(quiz)
        return file_info, update_msg
