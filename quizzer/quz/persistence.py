import abc
import calendar
import datetime
import glob
import json
import logging
import os.path
import traceback

log = logging.getLogger(__name__)


class AbstractPersistence(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def save(self, data_dict: dict) -> str:
        pass

    @abc.abstractmethod
    def get(self, create_domain_dct_object) -> (str, str, dict):
        pass

    @abc.abstractmethod
    def get_next(self, create_domain_dct_object) -> (str, str, dict):
        pass

    @abc.abstractmethod
    def get_previous(self, create_domain_dct_object) -> (str, str, dict):
        pass

    @abc.abstractmethod
    def delete(self) -> (str, str):
        pass

    @abc.abstractmethod
    def update(self, data_dict: dict) -> (str, str):
        pass


class JsonFileStorage:
    def __init__(self, save_dir: str, file_pfx: str):
        self._file_pfx = file_pfx
        self._save_dir = self._latest_file_number = self._active_file_index = self._files_paths = None
        self._initialize(save_dir, file_pfx)

    def _initialize(self, save_dir, file_pfx):
        self._save_dir, err_msg = JsonFileStorage._get_save_dir(save_dir)
        if err_msg is None:
            self._latest_file_number, self._files_paths = JsonFileStorage._get_file_paths(file_pfx, self._save_dir)
            self._active_file_index = len(self._files_paths) - 1
        else:
            raise Exception('JsonFileStorage failed - ' + err_msg)

    @staticmethod
    def _get_save_dir(save_dir) -> (str, str):
        save_dir = save_dir
        if save_dir.startswith("./"):
            save_dir = os.path.dirname(__file__) + save_dir[1:]
        save_dir = os.path.abspath(save_dir)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'save_dir={save_dir}')

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
    def _get_file_paths(file_pfx: str, save_dir: str) -> (str, str):
        file_paths = glob.glob(save_dir + '/' + file_pfx + '*.json')
        if len(file_paths) == 0:
            return 0, []

        file_paths.sort()
        file_nums = []
        proper_formatted_file_paths = []
        for file_path in file_paths:
            x = file_path.split('.')
            if len(x) > 0 and x[1].isnumeric():
                file_nums.append(int(x[1]))
            proper_formatted_file_paths.append(file_path)

        if len(file_nums) == 0:
            latest_file_number = 0
        else:
            latest_file_number = max(file_nums)
        return latest_file_number, proper_formatted_file_paths

    def save_file(self, data_dict: dict) -> str:
        file_num = self._latest_file_number + 1
        file_index = self._active_file_index + 1
        file_path = self._save_dir + '/' + self._file_pfx + '.' + str(file_num) + '.json'
        if file_index > len(self._files_paths):
            raise SystemError(
                f'Index Error:  _file_path_index= {file_index}' +
                f'(len(_files_paths)={len(self._files_paths)})')
        with open(file_path, "w", encoding='utf8') as f:
            json.dump(data_dict, f, ensure_ascii=False, sort_keys=False, indent=0)

        self._files_paths.append(file_path)
        self._latest_file_number = file_num
        self._active_file_index = file_index
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'file_path={file_path}')
        return file_path

    def update_file(self, data_dict: dict) -> (str, str):
        with open(self._files_paths[self._active_file_index], "w", encoding='utf8') as f:
            json.dump(data_dict, f, ensure_ascii=False, sort_keys=False, indent=0)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'file_path={self._files_paths[self._active_file_index]}')
        return self._file_info(), 'Updated: ' + self._file_name()

    def increment_file_index(self):
        self._validate_file_paths()
        if self._active_file_index != len(self._files_paths) - 1:
            self._active_file_index += 1

    def decrement_file_index(self):
        self._validate_file_paths()
        if self._active_file_index != 0:
            self._active_file_index -= 1

    def _validate_file_paths(self):
        if len(self._files_paths) == 0:
            raise FileExistsError(f'There are no "<prefix>.<unique-num>.json" files in: {self._save_dir}')

    def read_active_file(self) -> (str, str, dict):
        file_path = self._files_paths[self._active_file_index]
        try:
            with open(file_path, "r", encoding='utf8') as f:
                data_dict = json.load(f)
        except OSError:
            # reinitialize to fix for example no files found error.
            self._initialize(self._save_dir, self._file_pfx)
            file_path = self._files_paths[self._active_file_index]
            with open(file_path, "r", encoding='utf8') as f:
                data_dict = json.load(f)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'file_path={file_path}\ndata_dict=\n{data_dict}')
        return self._file_info(), self._file_name(), data_dict

    def delete_active_file(self) -> str:
        self._validate_file_paths()
        file_path = self._files_paths[self._active_file_index]
        os.remove(file_path)
        del self._files_paths[self._active_file_index]
        self._active_file_index -= 1
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'file_path={file_path}')
        return file_path

    def _file_name(self) -> str:
        file_num = str(self._active_file_index + 1)
        file_path = self._files_paths[self._active_file_index]
        file_name = os.path.basename(file_path)
        file_name = file_name[:len(file_name) - 5]
        info = file_num + '.  ' + file_name
        return info

    def _file_info(self) -> str:
        file_path = self._files_paths[self._active_file_index]
        seconds_since_created = os.path.getmtime(file_path)
        create_ts = datetime.datetime.utcfromtimestamp(seconds_since_created).isoformat()[:22]
        # remove T in, for example, create_ts = 2019-12-11T19:20:48.85
        create_ts = create_ts[2:10] + ' ' + create_ts[11:16]
        day_index = datetime.datetime.utcfromtimestamp(seconds_since_created).weekday()
        count = str(self._active_file_index + 1) + '/' + str(len(self._files_paths))
        info = count + '  ' + file_path + '  ' + create_ts + ' ' + calendar.day_name[day_index][0:3]
        return info


class FilePersistence(AbstractPersistence):
    file_storage_err_msg = True

    def __init__(self, save_dir: str, file_pfx: str):
        try:
            self._file_storage = JsonFileStorage(save_dir, file_pfx)
            self._file_pfx = file_pfx
            FilePersistence.file_storage_err_msg = None
        except Exception as e:
            FilePersistence.file_storage_err_msg = str(e)

    @staticmethod
    def validate_file_storage():
        if FilePersistence.file_storage_err_msg is not None:
            raise Exception(FilePersistence.file_storage_err_msg)

    def save(self, data_dict: dict) -> str:
        FilePersistence.validate_file_storage()
        file_path = self._file_storage.save_file(data_dict)
        return 'Saved quiz into: ' + file_path

    def get(self, create_domain_object) -> (str, str, dict):
        FilePersistence.validate_file_storage()
        status_msg, file_name, data_dict = self._file_storage.read_active_file()
        domain_object = create_domain_object(data_dict)
        return status_msg, file_name, domain_object

    def get_next(self, create_domain_dct_object) -> (str, str, dict):
        self._file_storage.increment_file_index()
        return self.get(create_domain_dct_object)

    def get_previous(self, create_domain_dct_object) -> (str, str, dict):
        print(type(create_domain_dct_object))
        self._file_storage.decrement_file_index()
        return self.get(create_domain_dct_object)

    def delete(self) -> (str, str):
        FilePersistence.validate_file_storage()
        return self._file_storage.delete_active_file(), 'Deleted file'

    def update(self, data_dict: dict) -> (str, str):
        FilePersistence.validate_file_storage()
        file_info, update_msg = self._file_storage.update_file(data_dict)
        return file_info, update_msg
