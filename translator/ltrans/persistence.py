import datetime
import calendar
from ltrans.userinput import UserInput
from ltrans.userinput import UserInputError
import glob
import json
import logging
import os.path
import traceback

log = logging.getLogger(__name__)


class FileStorage:
    def __init__(self, config: dict):
        self._save_dir, err_msg = FileStorage._get_save_dir(config)
        if err_msg is None:
            self._latest_file_number, self._files_paths = FileStorage._get_filepaths(self._save_dir)
            self._file_paths_index = len(self._files_paths) - 1
        else:
            raise Exception('FileStorage failed - ' + err_msg)

    @staticmethod
    def _get_save_dir(config: dict) -> tuple:
        if config is None or config.get('SAVED_TRANSLATIONS_DIR') is None:
            return None, 'config missing parameter "SAVED_TRANSLATIONS_DIR"'
        save_dir = config['SAVED_TRANSLATIONS_DIR']
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
    def _get_filepaths(save_dir: str) -> tuple:
        file_paths = glob.glob(save_dir + '/*.json')
        if len(file_paths) == 0:
            return 0, []

        file_paths.sort()
        trans_nums = []
        proper_formatted_filepaths = []
        for file_path in file_paths:
            x = file_path.split('.')
            if len(x) > 0 and x[1].isnumeric():
                trans_nums.append(int(x[1]))
            proper_formatted_filepaths.append(file_path)

        if len(trans_nums) == 0:
            latest_file_number = 0
        else:
            latest_file_number = max(trans_nums)
        return latest_file_number, proper_formatted_filepaths

    def save(self, translation: dict, file_pfx) -> str:
        print('---------', self._files_paths)
        trans_number = self._latest_file_number + 1
        file_index = self._file_paths_index + 1
        filepath = self._save_dir + '/' + file_pfx + '.' + str(
            trans_number) + '.json'
        if file_index > len(self._files_paths):
            raise SystemError(
                f'Index Error:  _file_path_index= {file_index}' + \
                f'(len(_files_paths)={len(self._files_paths)})')
        with open(filepath, "w", encoding='utf8') as f:
            json.dump(translation, f, ensure_ascii=False, sort_keys=False, indent=0)

        self._files_paths.append(filepath)
        self._latest_file_number = trans_number
        self._file_paths_index = file_index
        print('+++++++', self._files_paths)
        print('+++++++', file_index)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'filepath={filepath}')
        return 'Saved screen into: ' + filepath

    def update(self, translation: dict) -> tuple:
        with open(self._files_paths[self._file_paths_index], "w", encoding='utf8') as f:
            json.dump(translation, f, ensure_ascii=False, sort_keys=False, indent=0)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'filepath={self._files_paths[self._file_paths_index]}')
        return self._files_paths[self._file_paths_index], 'File updated'

    def read_next(self) -> tuple:
        self._validate_file_paths()
        if self._file_paths_index != len(self._files_paths) - 1:
            self._file_paths_index += 1
        return self._read_json_file()

    def read_prev(self) -> tuple:
        self._validate_file_paths()
        if self._file_paths_index != 0:
            self._file_paths_index -= 1
        return self._read_json_file()

    def _validate_file_paths(self):
        if len(self._files_paths) == 0:
            raise UserInputError(f'There are no translation JSON files in: {self._save_dir}')

    def _read_json_file(self) -> tuple:
        filepath = self._files_paths[self._file_paths_index]
        with open(filepath, "r", encoding='utf8') as f:
            translation = json.load(f)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'filepath={filepath}\ntranslation=\n{translation}')
        return filepath, self.file_info(), translation

    def delete(self) -> tuple:
        self._validate_file_paths()
        filepath = self._files_paths[self._file_paths_index]
        os.remove(filepath)
        del self._files_paths[self._file_paths_index]
        self._file_paths_index -= 1
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'filepath={filepath}')
        return filepath, 'Deleted file'

    def file_info(self):
        file_path = self._files_paths[self._file_paths_index]
        seconds_since_created = os.path.getmtime(file_path)
        create_ts = datetime.datetime.utcfromtimestamp(seconds_since_created).isoformat()[:22]
        # remove T in, for example, create_ts = 2019-12-11T19:20:48.85
        create_ts = create_ts[:10] + ' ' + create_ts[11:16]
        day_index = datetime.datetime.utcfromtimestamp(seconds_since_created).weekday()
        count = str(self._file_paths_index + 1) + '/' + str(len(self._files_paths))
        file_name = os.path.basename(file_path)
        file_name = file_name[:len(file_name) - 5]
        info = count + ' ' + file_name + ' ' + create_ts[2:] + calendar.day_name[day_index][0:3]
        return info


class Persistence:
    TRANSLATION_KEYS = {'text_lines',
                        'src_language',
                        'dest_language',
                        'is_add_src',
                        'is_add_transliteration',
                        'translated_text'}
    err_msg = None

    def __init__(self, config: dict):
        try:
            self._file_storage = FileStorage(config)
            Persistence.err_msg = None
        except Exception as e:
            Persistence.err_msg = str(e)

    @staticmethod
    def _transaltion(user_input: UserInput, translated_text: str) -> dict:
        return {'dest_language': user_input.dest_language,
                'is_add_src': user_input.is_add_src,
                'is_add_transliteration': user_input.is_add_transliteration,
                'src_language': user_input.src_language,
                'text_lines': user_input.text_lines,
                'translated_text': translated_text
                }

    def save_translation(self, user_input: UserInput, translated_text: str) -> str:
        if Persistence.err_msg is not None:
            raise Exception(Persistence.err_msg)
        file_pfx = user_input.src_language + '-' + user_input.dest_language
        translation = Persistence._transaltion(user_input, translated_text)
        file_path = self._file_storage.save(translation, file_pfx)
        return 'Saved translation in: ' + file_path

    def next_translation(self) -> tuple:
        if Persistence.err_msg is not None:
            raise Exception(Persistence.err_msg)
        file_path, msg, translation = self._file_storage.read_next()
        self._validate_keys(translation)
        return file_path, msg, translation

    def previous_translation(self) -> tuple:
        if Persistence.err_msg is not None:
            raise Exception(Persistence.err_msg)
        file_path, msg, translation = self._file_storage.read_prev()
        self._validate_keys(translation)
        return file_path, msg, translation

    def delete_translation(self) -> tuple:
        if Persistence.err_msg is not None:
            raise Exception(Persistence.err_msg)
        return self._file_storage.delete()

    def update_translation(self, user_input: UserInput, translated_text: str) -> tuple:
        if Persistence.err_msg is not None:
            raise Exception(Persistence.err_msg)
        translation = Persistence._transaltion(user_input, translated_text)
        return self._file_storage.update(translation)

    def _validate_keys(self, translation: dict):
        keys = set(translation.keys())
        if keys != Persistence.TRANSLATION_KEYS:
            raise Exception(f'invalid translation keys: {keys}')
