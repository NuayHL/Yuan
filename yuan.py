import os
import sys
import warnings

from colorstr import ColorStr as Co
from baselog import BasicLog

# define the log class

class Yuan:
    MYLOG = BasicLog
    """
    A fundamental recorder for any action
    """
    def __init__(self):
        self._using_log = False
        self._logger = None
        self._console_print = True

    def silent(self):
        self.console_off()
        if self._using_log:
            self.log_temp_off()
        else:
            self.log_off()

    def on(self):
        self.console_on()
        try:
            self.log_on()
        except:
            self.warning('Your have not set main log, consider using \'self.console_on()\' instead of \'self.on()\'')

    def console_off(self):
        self._console_print = False

    def console_on(self):
        self._console_print = True

    def log_on(self, log_name, log_dir_path='', logger: MYLOG = None):
        if logger:
            self._logger = logger
        elif log_dir_path:
            self._logger = Yuan.MYLOG(log_name=log_name, log_dir_path=log_dir_path)
        else:
            assert self._logger, 'Please complete the log file infor: path or logger instance'
            self._using_log = True
            self.warning('--LOG ON--')
        self._using_log = True

    def log_off(self):
        self._using_log = False
        if self._logger is not None:
            self.log_warning('--LOG END--')
        self._logger = None

    def log_temp_off(self):
        assert self._logger, 'You need to set the log before temporarily set it off'
        self.log_warning('Temporarily turn off log')
        self._using_log = False

    def print(self, *args):
        self.log_info(*args)
        self.console_print(*args)

    def warning(self, *args):
        self.log_warning(*args)
        self.console_warning(*args)

    def log_info(self, *args, **kwargs):
        if self._using_log:
            args = [Co.de_format(strings) for strings in args]
            self._logger.info(*args, **kwargs)

    def log_warning(self, *args, **kwargs):
        if self._using_log:
            args = [Co.de_format(strings) for strings in args]
            self._logger.warning(*args, **kwargs)

    def log_error(self, *args, **kwargs):
        if self._using_log:
            args = [Co.de_format(strings) for strings in args]
            self._logger.error(*args, **kwargs)

    def console_print(self, *args, **kwargs):
        if self._console_print:
            print(*args, **kwargs)

    def console_warning(self, *args, **kwargs):
        if self._console_print:
            warnings.warn(*args, **kwargs)

    def debug2txt(self, *args, debug_file_name='debug.txt'):
        with open(debug_file_name, 'a') as f:
            print(*args, file=f)


