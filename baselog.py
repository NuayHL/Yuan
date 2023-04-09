from abc import ABC, abstractmethod
import os
import datetime
import logging
import sys


class BaseLog(ABC):
    @abstractmethod
    def info(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def warning(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def error(self, *args, **kwargs):
        raise NotImplementedError


class BasicLog(BaseLog):
    def __init__(self, log_name, log_dir_path=''):
        self.name = log_name
        self.log_dir_path = log_dir_path
        self.logger = logging.getLogger(log_name)
        self.logger.propagete = False
        self.logger.setLevel(logging.INFO)
        self.log_path = ''
        self._set_log_file()

    def _set_log_file(self):
        self.log_path = os.path.join(self.log_dir_path, self.name + '.log')
        fh = logging.FileHandler(self.log_path)

        def _utc8_aera(timestamp):
            now = datetime.datetime.utcfromtimestamp(timestamp) + datetime.timedelta(hours=8)
            return now.timetuple()

        formatter = logging.Formatter('[%(asctime)s][%(levelname)s]:%(message)s')
        formatter.converter = _utc8_aera
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)
