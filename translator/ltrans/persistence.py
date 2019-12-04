from ltrans.userinput import UserInput
import glob
import json
import logging
import os.path
import traceback

LOG = logging.getLogger(__name__)


class Persistence:
    def __init__(self, config: dict):
        self._save_dir, self._err_msg = Persistence._get_save_dir(config)
        self._file_path_index = -1
        if self._err_msg is None:
            self._latest_trans_number, self._files_paths = Persistence._get_filepaths(self._save_dir)
            self._file_path_index = len(self._files_paths) - 1

    @property
    def file_path_index(self) -> int:
        return self._file_path_index

    @staticmethod
    def _get_save_dir(config: dict) -> tuple:
        if config is None or config.get('SAVED_TRANSLATIONS_DIR') is None:
            return None, 'config missing parameter "SAVED_TRANSLATIONS_DIR"'
        save_dir = config['SAVED_TRANSLATIONS_DIR']
        if save_dir.startswith("./"):
            save_dir = os.path.dirname(__file__) + save_dir[1:]
        save_dir = os.path.abspath(save_dir)
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug(f'dict_file_path={save_dir}')

        if not os.path.exists(save_dir):
            try:
                os.mkdir(save_dir, 0o777)
                LOG.info(f'Created dir ' + save_dir)
            except Exception as e:
                trace = str(e) + '\n\t' + traceback.format_exc()
                LOG.error(trace)
                return None, str(e)
        return save_dir, None

    @staticmethod
    def _get_filepaths(save_dir: str) -> tuple:
        filepaths = glob.glob(save_dir + '/*.json')
        print('-------',save_dir, filepaths)
        if len(filepaths) == 0:
            return 0, []

        trans_nums = []
        translation_filepaths = []
        for filepath in filepaths:
            x = filepath.split('.')
            if len(x) > 0 and x[1].isnumeric():
                trans_nums.append(int(x[1]))
                translation_filepaths.append(filepath)

        if len(trans_nums) == 0:
            latest_trans_number = 0
        else:
            latest_trans_number = max(trans_nums)
        return latest_trans_number, translation_filepaths

    def save_translation(self, user_input: UserInput, translated_text: str) -> str:
        if translated_text.strip() == '':
            return 'Cannot save translation - incomplete attributes'
        if self._err_msg is not None:
            raise Exception('cannot save file - ' + self._err_msg)
        self._latest_trans_number += 1
        self._file_path_index += 1
        filepath = self._save_dir + '/' + user_input.src_language + '-' + user_input.dest_language + '.' + str(
            self._latest_trans_number) + '.json'
        self._files_paths.append(filepath)
        if self._file_path_index > (len(self._files_paths) - 1):
            raise Exception(
                f'Index Error:  _file_path_index= {self._file_path_index}' + \
                f'(len(_files_paths)={len(self._files_paths)}-1)')
        if filepath != self._files_paths[self._file_path_index]:
            raise Exception(
                f'filepath  {filepath} != _files_paths[{self._file_path_index}]  ' + \
                f'(_files_paths={self._files_paths}-1)')
        translation = {'text_lines': user_input.text_lines,
                       'src_language': user_input.src_language,
                       'dest_language': user_input.dest_language,
                       'is_add_src': user_input.is_add_src,
                       'is_add_transliteration': user_input.is_add_transliteration,
                       'translated_text': translated_text,
                       'description': user_input.description
                       }
        with open(filepath, "w", encoding='utf8') as f:
            json.dump(translation, f, ensure_ascii=False, sort_keys=False, indent=0)
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug(f'filepath={filepath}')
        return filepath

    def read_next(self) -> dict:
        if self._err_msg is not None:
            raise Exception('cannot read any files - ' + self._err_msg)
        if len(self._files_paths) == 0:
            raise Exception(f'There are no translation files in: {self._save_dir}')
        if self._file_path_index != len(self._files_paths) - 1:
            self._file_path_index += 1
        return self._read_translation()

    def read_prev(self) -> dict:
        if self._err_msg is not None:
            raise Exception('cannot read any files - ' + self._err_msg)
        if len(self._files_paths) == 0:
            raise Exception(f'There are no translation files in: {self._save_dir}')
        if self._file_path_index != 0:
            self._file_path_index -= 1
        return self._read_translation()

    def _read_translation(self) -> dict:
        filepath = self._files_paths[self._file_path_index]
        with open(filepath, "r", encoding='utf8') as f:
            translation = json.load(f)
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug(f'filepath={filepath}\ntranslation=\n{translation}')
        return translation

    def delete_translation(self) -> str:
        filepath = self._files_paths[self._file_path_index]
        os.remove(filepath)
        del self._files_paths[self._file_path_index]
        self._file_path_index -= 1
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug(f'filepath={filepath}')
        return filepath
