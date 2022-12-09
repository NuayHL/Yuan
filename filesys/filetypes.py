import abc
from filesys.tools import *

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


class _FileClassify:
    def __init__(self, *file):
        super(_FileClassify, self).__init__()
        self.files = list(*file)

        self.all_type = dict()
        self.file_in_type = dict()

        self.update_all_exts()

    def update_all_exts(self):
        ext_list = []
        for file in self.files:
            ext = getext(file)
            if ext and ext not in ext_list:
                ext_list.append(ext)
        for ext in ext_list:
            self.update_ext(ext)

    def set_load_func(self, type_name, func):
        assert type_name in self.all_type, 'Could not find %s in file type' % type_name
        self.all_type[type_name].set_load_func(func)

    def update_files(self, *files):
        for file in files:
            if file not in self.files:
                self.files.append(file)
                self._update_file(file)

    def _update_file(self, file_name):
        for file_type in self.all_type:
            if self.all_type[file_type].is_type(file_name):
                self.all_type[file_type].append(file_name)

    def update_type(self, type_name:str, is_type_func):
        self.add_type(type_name=type_name, is_type_func=is_type_func)
        self._update_type(type_name)

    def update_ext(self, ext_name):
        self.add_ext(ext_name=ext_name)
        self._update_type(ext_name)

    def _update_type(self, type_name):
        for file in self.files:
            if self.all_type[type_name].is_type(file):
                self.file_in_type[type_name].append(file)

    def add_type(self, type_name:str, is_type_func):
        file_type = File_Type(type_name)
        file_type.set_istype(is_type_func)
        self._add_type(file_type)

    def add_ext(self, ext_name:str):
        file_type = _Ext_Type(ext_name)
        self._add_type(file_type)

    def _add_type(self, file_type:File_Type):
        type_name = file_type.name
        self.all_type[type_name] = file_type
        self.file_in_type[type_name] = list()

    def del_type(self, type_name):
        if type_name in self.all_type:
            del self.all_type[type_name]
            del self.file_in_type[type_name]
        else:
            raise 'Type %s do not exist in this place'

    def load_type_func(self, type_name, file_name=None):
        assert type_name in self.all_type
        if file_name:


        func = self.all_type[type_name].load_func
        if func is None:
            raise 'Loading a type func \'%s\' which is not defined!' % type_name
        return func





