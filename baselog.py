from abc import ABC, abstractmethod
import os
import datetime
import logging
import sys


class BaseLog(ABC):
    def __init__(self, log_name):
        pass

    @abstractmethod
    def info(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def warning(self, *args, **kwargs):
        raise NotImplementedError


class BasicLog(BaseLog):
    def __init__(self, log_name):
        super(BasicLog, self).__init__(log_name)
        self.name = log_name
        self.logger = logging.getLogger(log_name)
        self.logger.propagete = False
        self.logger.setLevel(logging.INFO)
        self.log_file_path = ''
        self.set_log_file()

    def set_log_file(self):
        self.log_file_path = self.name + '.log'
        fh = logging.FileHandler(self.log_file_path)

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
