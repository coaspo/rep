import os


class WebSite:
    def __init__(self, target_dirs):
        self.__file_paths = WebSite.get_search_file_paths(target_dirs)

    @staticmethod
    def get_search_file_paths(target_dirs):
        file_paths = []
        for subdir, dirs, files in os.walk("."):
            is_target_dir = False
            for target_dir in target_dirs:
                if subdir.startswith(target_dir):
                    is_target_dir = True
                    break
            if is_target_dir:
                for file in files:
                    p = os.path.join(subdir, file)[2:]
                    file_paths.append([p, os.path.getmtime(p)])
        file_paths.sort(key=lambda x: x[0])
        return file_paths

    def save_search_file_paths(save_file, file_paths):
        with open(save_file, 'w') as f:
            f.writelines('/' + x[0] + '\n' for x in file_paths)
        log('Updated ' + save_file)
        global msg
        msg += '\nSaved search file paths in: ' + save_file

    def update_contents(file_paths):
        (version, lines) = get_version()
        if version is None:
            exit()
        try:
            with open('contents.html', 'w') as f:
                for line in lines:
                    if line.startswith('<br><br>'):
                        f.write(line + '\n')
                        append_version_and_content_links(version, file_paths, f)
                        break
                    f.write(line + '\n')
        except Exception as e:
            print(traceback.format_exc())
            with open('contents.html', 'w') as f:
                for line in lines:
                    f.write(line + '\n')
            raise

        global msg
        msg += '\nupdated version: ' + version + ' and contents in contents.html'
        return version

    @property
    def file_paths(self) -> list:
        return self.__file_paths

    def __str__(self) -> str:
        return f'UserInput: src = {self.src_language},  dest = {self.destination_language}, ' + \
               f' is_add_src = {self.is_add_src},  is_add_transliteration = {self.is_add_transliteration}, ' + \
               f' text = {self.text_lines} '
