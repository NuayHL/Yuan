import abc
import os
import warnings
from collections import defaultdict

from filesys.tools import *

class FileManager:
    def __init__(self, path):
        super(FileManager, self).__init__()
        self._path = getabspath(path)
        self._name = getori(path)
        self._free = True
        self._num_files = len(self)

        self.cache = defaultdict(lambda x: False)

    def remove(self, file_name):
        assert self._free, 'Not allowed to remove files during iteration'
        os.remove(self._join(file_name))

    def duplicate(self, file_name):
        assert self._free, 'Not allowed to duplicate files during iteration'
        pass

    def getpath(self, file_name):
        return self._join(file_name)

    def check(self, full_file_name):
        return self._check(full_file_name)

    def _check(self, full_file_name):
        return os.path.exists(self._join(full_file_name))

    def _join(self, name):
        return os.path.join(self._path, name)

    def update(self):
        self._all_files = os.listdir(self._path)

    def __iter__(self):
        self._num_files = len(self)
        self._counts = 0
        self._free = False
        return self

    def __next__(self):
        current_counts = self._counts
        self._counts += 1
        if self._counts == self._num_files:
            self._free = True
            self._counts = 0
            raise StopIteration
        return self._join(self._all_files[current_counts])

    def __len__(self):
        self.update()
        return len(self._all_files)

    def path(self):
        return self._path

    def isfile(self, name):
        return os.path.isfile(self._join(name))

    def isdir(self, name):
        return os.path.isfile(self._join(name))

    def __str__(self):
        return self._path

    def __eq__(self, other):
        assert isinstance(other, FileManager)
        return self._path == other.path()






