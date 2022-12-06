import os
import sys
import warnings

from logging import Logging

class Yuan:
    def __init__(self):
        self._logname = ''
        self._logger = None
        self._console_print = True

    def console_off(self):
        self._console_print = False

    def console_on(self):
        self._console_print = True

    def log_on(self, path):
        self._logname = path
        self._logger = Logging(path)

    def log_off(self):
        self._logname = ''
        self._logger = None

    def print(self, *args, **kwargs):
        self.log_info(*args)
        self.console_print(*args, **kwargs)

    def warning(self, *args):
        self.log_warning(*args)
        self.warning(*args)

    def log_info(self, *args, **kwargs):
        if self._logger:
            self._logger.info(*args, **kwargs)

    def log_warning(self, *args, **kwargs):
        if self._logger:
            self._logger.warning(*args, **kwargs)

    def console_print(self, *args, **kwargs):
        if self._console_print:
            print(*args, **kwargs)

    def console_warning(self, *args, **kwargs):
        if self._console_print:
            warnings.warn(*args, **kwargs)
    
