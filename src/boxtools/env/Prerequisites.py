#!/usr/bin/env python3

from boxtools.data.access.fileAccess import get_file_as_list, get_python_box_path


class Prerequisites:
    min_python_version: str | None = None

    def __init__(self, min_python_version: str):
        self.min_python_version = min_python_version
        self.git_libs = get_file_as_list(get_python_box_path().joinpath('install').joinpath('requirements'))

    def validate_python_version(self) -> bool:
        from platform import python_version_tuple
        from os import system
        # Confirm Python version
        python_client_v = list(map(int, python_version_tuple()))
        a_python_min_v = list(map(int, self.min_python_version.split('.')))
        from boxtools.Logs import LogDisplay
        log: LogDisplay = LogDisplay().get_log_display()
        log.show_debug_log(' - Prerequisites#validate_python_version - Python version > ' + str(python_client_v) + ' | Python min version > ' + str(a_python_min_v))
        if (python_client_v[0] < a_python_min_v[0]) \
                or (python_client_v[0] == a_python_min_v[0] and python_client_v[1] < a_python_min_v[1]) \
                or (python_client_v[0] == a_python_min_v[0] and python_client_v[1] == a_python_min_v[1]
                   and python_client_v[2] < a_python_min_v[2]):
            log.show_log('')
            log.show_critical_log('Your Python version is not supported! Please upgrade to version ' + self.min_python_version
                  + ' or above')
            log.show_log('Your current/active Python version is:')
            system('python --version')
            log.show_log('')
            log.show_log('Note: if you\'re using pyenv, you might want to add `pyenv local 3.13.0` (replace version with your actual version number) at the end of your `$HOME/.zshrc` file to fix this.')

            return False
        return True

    def validate_python_libs(self, suggest_install: bool = False) -> bool:
        from boxtools.Logs import LogDisplay
        log: LogDisplay = LogDisplay().get_log_display()
        log.show_debug_log(' - Validating Python required libraries...')
        pip_packages = self.get_pip_packages()
        log.show_debug_log(pip_packages)
        for lib in self.git_libs:
            log.show_debug_log(f' -- Validating library ---> {lib}')
            if lib in pip_packages:
                log.show_debug_log(f' - Library {lib} is installed in pip packages')
                # Installed through pip
                continue
            #elif lib in modules:
            #    log.show_debug_log(f' - Library {lib} exists in sys.modules')
            #    # Exists in sys.modules
            #    continue
            else:
                log.show_critical_log(f' - Missing Python library: {lib}')
                if suggest_install:
                    from boxtools.data.input import ask_for_choice
                    choice: str = ask_for_choice('Do you want to install this library? (Uses pip)', ['Yes', 'No'])
                    if choice is not None and choice.lower() == 'y' or choice.lower() == 'yes':
                        from os import system
                        system(f'pip install {lib}')
                    else:
                        return False
        return True

    @staticmethod
    def get_pip_packages():
        from subprocess import check_output
        from sys import executable
        reqs = check_output([executable, '-m', 'pip', 'freeze'])
        return [r.decode().split('==')[0] for r in reqs.split()]