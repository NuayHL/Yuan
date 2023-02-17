import abc
import os
import warnings
from collections import defaultdict

from filesys.tools import *
from filesys.tools import getext
from registry import Registry

FileType_Registry = Registry('file_type')

class FileManager:
    def __init__(self, path):
        super(FileManager, self).__init__()
        self._path = getabspath(path)
        self._name = getori(path)

        self._all_files = set()
        self.update()

        self.file_cls_sys = _FileClassify(*list(self._all_files))
        self.cache = defaultdict(lambda x: False)

    def remove(self, file_name):
        os.remove(self._join(file_name))
        self.update_file(file_name)

    def duplicate(self, file_name):
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
        files = os.listdir(self._path)
        self._all_files = files
        for file in files:
            self.update_file(file)

    def update_only_files(self):
        files = os.listdir(self._path)
        for file in files:
            if file not in self._all_files and self.isfile(file):
                self._all_files.append(file)
                self._in_path_files[file] = self._join(file)

    def update_only_dirs(self):
        files = os.listdir(self._path)
        for file in files:
            if file not in self._all_files and self.isdir(file):
                self._all_files.append(file)
                self._in_path_dirs[file] = self._join(file)

    def update_file(self, filename):
        if filename.startswith(('.', '__')):
            return
        abs_file_path = self._join(filename)
        if os.path.exists(abs_file_path):
            if os.path.isfile(abs_file_path):
                self._in_path_files[filename] = abs_file_path
                self.file_cls_sys.update_file(filename)
            elif os.path.isdir(abs_file_path):
                self._in_path_dirs[filename] = FileManager(abs_file_path)
            else:
                warnings.warn('File type not recognized \"%s\"' % abs_file_path)
        else:
            if filename in self._all_files:
                self._del_file_record(filename)
            else:
                warnings.warn('Can not directly find \"%s\" in \"%s\"' % (filename, self._path))

    def search_files(self, filename, find_all=False, indirs:int = 100):
        file_list = []
        find_flag = False
        if filename in self._all_files:
            file_list.append(self._join(filename))
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

    def path(self):
        return self._path

    def _del_file_record(self, name):
        self._all_files.remove(name)
        if name in self._in_path_files:
            del self._in_path_files[name]
            self.file_cls_sys.del_file(name)
        if name in self._in_path_dirs:
            del self._in_path_dirs[name]

    def isfile(self, name):
        return os.path.isfile(self._join(name))

    def isdir(self, name):
        return os.path.isfile(self._join(name))

    def __str__(self):
        return self._path

    def __eq__(self, other):
        assert isinstance(other, FileManager)
        return self._path == other.get_path()


class _FileClassify:
    def __init__(self, file_char_list):
        self.files_with_type = defaultdict(list)
        self.all_type = FileType_Registry
        for file_char in file_char_list:
            self.update_file(file_char)

    def update_file(self, file_char):
        for type_name, file_type in self.all_type.items():
            if file_type.is_type(file_char):
                self._add_type(file_char, type_name)

    def _add_type(self, file_char, type_name):
        if type_name not in self.files_with_type[file_char]:
            self.files_with_type[file_char].append(type_name)

    def del_file(self, file_char):
        assert file_char in self.files_with_type, 'File \'%s\' do not exist' % file_char
        del self.files_with_type[file_char]

    def get_type_of_file(self, file_char):
        return self.files_with_type[file_char]

    def get_files_in_type(self, type_name):
        fin_files = list()
        for file_name, file_types in self.files_with_type.items():
            if type_name in file_types:
                fin_files.append(file_name)
        return fin_files

class File_Type(abc.ABC):
    def __init__(self):
        self.name = self.__class__.__name__

    @abc.abstractmethod
    def load(self, **kwargs):
        pass

    @abc.abstractmethod
    def save(self, **kwargs):
        pass

    @abc.abstractmethod
    def is_type(self, **kwargs):
        pass

class _File_Tree:
    def __init__(self, base_name, parent_node):
        self._name = base_name
        self._all_child = set()
        self._child_node = set()
        self._parent = parent_node

    def name(self):
        return self._name

    def

    def child(self):
        return self._all_child

    def child_node(self):
        return self._child_node

    def __eq__(self, other):
        if isinstance(other, str):
            return self._name == other
        elif isinstance(other, _File_Tree):
            return self._name == other.name()
        else:
            raise NotImplementedError





