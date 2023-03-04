import shutil
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
        assert self._check_free(file_name), 'Not allowed to remove other files during iteration'
        os.remove(self._join(file_name))

    def copy(self, file_name, dst_name=None):
        assert self.check(file_name), '\'%s\' does not exits' % file_name
        assert self._check_free(file_name), 'Not allowed to duplicate other files during iteration'
        if dst_name:
            dst_name = self.check_repeat(dst_name)
        else:
            dst_name = self.check_repeat(file_name)
        shutil.copy(self._join(file_name), self._join(dst_name))
        return dst_name

    def move(self, file_name, dst_name):
        assert self.check(file_name), '\'%s\' does not exits' % file_name
        assert self._check_free(file_name), 'Not allowed to move other files during iteration'
        return shutil.move(self._join(file_name), self._join(dst_name))

    def rename(self, file_name, dst_name):
        assert self.check(file_name), '\'%s\' does not exits' % file_name
        assert self._check_free(file_name), 'Not allowed to rename other files during iteration'
        dst_name = self.check_repeat(dst_name)
        os.rename(self._join(file_name), self._join(dst_name))
        return dst_name

    def getfullpath(self, file_name):
        return self._join(file_name)

    def check(self, full_file_name):
        return self._check(full_file_name)

    def check_repeat(self, file_name):
        no_ext = getnoext(file_name)
        ext = getext(file_name)
        repeat_idx = 1
        while os.path.exists(self._join(file_name)):
            file_name = no_ext + '_%d' % repeat_idx + ext
            repeat_idx += 1
        return file_name

    def _check(self, full_file_name):
        return os.path.exists(self._join(full_file_name))

    def _join(self, name):
        return os.path.join(self._path, name)

    def update(self):
        self._all_files = os.listdir(self._path)

    def _check_free(self, file_name):
        return self._free or file_name == self._current_file

    def __iter__(self):
        self._num_files = len(self)
        self._counts = 0
        self._free = False
        self._current_file = None
        return self

    def __next__(self):
        self._current_file = self._all_files[self._counts]
        self._counts += 1
        if self._counts == self._num_files:
            self._free = True
            self._counts = 0
            raise StopIteration
        return self._join(self._current_file)

    def __len__(self):
        self.update()
        return len(self._all_files)

    def basepath(self):
        return self._path

    def isfile(self, name):
        return os.path.isfile(self._join(name))

    def isdir(self, name):
        return os.path.isdir(self._join(name))

    def __str__(self):
        return self._path

    def __eq__(self, other):
        assert isinstance(other, FileManager)
        return self._path == other.basepath()






