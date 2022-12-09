import os
import sys
import warnings

from baselog import BaseLog

class Yuan:
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

    def console_off(self):
        self._console_print = False

    def console_on(self):
        self._console_print = True

    def log_on(self, log_name='', logger: BaseLog = None):
        self._using_log = True
        if logger:
            self._logger = logger
        elif log_name:
            self._logger = BaseLog(log_name)
        else:
            assert self._logger, 'Please complete the log file infor: path or logger instance'
            self._using_log = True
            self.warning('Turn on log')

    def log_off(self):
        self._using_log = False
        self._logger = None

    def log_temp_off(self):
        assert self._logger, 'You need to set the log before temporarily set it off'
        self.log_warning('Temporarily turn off log')
        self._using_log = False

    def print(self, *args, **kwargs):
        self.log_info(*args)
        self.console_print(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.log_warning(*args)
        self.console_warning(*args, **kwargs)

    def log_info(self, *args, **kwargs):
        if self._using_log:
            self._logger.info(*args, **kwargs)

    def log_warning(self, *args, **kwargs):
        if self._using_log:
            self._logger.warning(*args, **kwargs)

    def console_print(self, *args, **kwargs):
        if self._console_print:
            print(*args, **kwargs)

    def console_warning(self, *args, **kwargs):
        if self._console_print:
            warnings.warn(*args, **kwargs)

