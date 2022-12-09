import os
import warnings
from collections import defaultdict
from filesys.filetypes import _FileClassify
from filesys.tools import *

class FileManager:
    def __init__(self, path):
        super(FileManager, self).__init__()
        self._path = abspath(path)
        self._name = getori(path)

        self._all_files = list()
        self._in_path_files = dict()
        self._in_path_dirs = dict()
        self.update()

        self.file_cls_sys = _FileClassify(*self._in_path_files.keys())
        self.cache = defaultdict(lambda x: False)

    def update(self):
        files = os.listdir(self._path)
        self._all_files = files
        for file in files:
            self.update_file(file)

    def update_only_files(self):
        files = os.listdir(self._path)
        for file in files:
            if file not in self._all_files and self.isfile(file):
                self._all_files.append(file)
                self._in_path_files[file] = self.join(file)

    def update_only_dirs(self):
        files = os.listdir(self._path)
        for file in files:
            if file not in self._all_files and self.isdir(file):
                self._all_files.append(file)
                self._in_path_dirs[file] = self.join(file)

    def update_file(self, filename):
        if filename.startswith(('.', '__')):
            return
        abs_file_path = self.join(filename)
        if os.path.exists(abs_file_path):
            if os.path.isfile(abs_file_path):
                self._in_path_files[filename] = abs_file_path
            elif os.path.isdir(abs_file_path):
                self._in_path_dirs[filename] = FileManager(abs_file_path)
            else:
                warnings.warn('File type not recognized \"%s\"' % abs_file_path)
        else:
            if filename in self._all_files:
                self.del_file(filename)
            else:
                warnings.warn('Can not directly find \"%s\" in \"%s\"' % (filename, self._path))

    def search_files(self, filename, find_all=False, indirs:int = 100):
        file_list = []
        find_flag = False
        if filename in self._all_files:
            file_list.append(self.join(filename))
            if not find_all:
                return file_list[0]
            find_flag = True
        if indirs > 0:
            for in_dir in self._in_path_dirs.values():
                return_val = in_dir.search_files(filename=filename, find_all=find_all, indirs=indirs-1)
                if return_val:
                    if not find_all:
                        return return_val
                    file_list += return_val
                    find_flag = True
        if find_flag:
            return file_list
        else:
            return False

    def get_path(self, filename):
        return self.search_files(filename=filename)

    def path(self):
        return self._path

    def join(self, name):
        return os.path.join(self._path, name)

    def del_file(self, name):
        self._all_files.remove(name)
        if name in self._in_path_files:
            del self._in_path_files[name]
        if name in self._in_path_dirs:
            del self._in_path_dirs[name]

    def isfile(self, name):
        return os.path.isfile(self.join(name))

    def isdir(self, name):
        return os.path.isfile(self.join(name))

    def check(self, name):
        return os.path.exists(self.join(name))


    def __str__(self):
        return self._path

    def __eq__(self, other):
        assert isinstance(other, FileManager)
        return self._path == other.get_path()



