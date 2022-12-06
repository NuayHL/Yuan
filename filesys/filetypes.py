from yuan import Yuan
from filesys.tools import *

class _File_Type:
    def __init__(self, type_name):
        self.name = type_name
        self.is_type_fun = None
        self.load_func = None

    def set_istype(self, func):
        self.is_type_fun = func

    def set_loadfunc(self, func):
        self.load_func = func

    def load(self, file_char):
        assert self.load_func, 'Please set_loadfun for this type'
        return self.load_func(file_char)

    def is_type(self, file_char):
        assert self.is_type_fun, 'Please set_istype for this type'
        return self.is_type_fun(file_char)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, _File_Type):
            return self.name == other.name
        else:
            raise NotImplementedError('Can not using \'=\' for classes other than str or _File_Type')

class _Ext_Type(_File_Type):
    def __init__(self, ext_name):
        super(_Ext_Type, self).__init__(ext_name)
        self.set_istype()

    def set_istype(self, func=None):
        def is_this_ext(name):
            return getext(name) == self.name
        self.is_type_fun = is_this_ext

class _FileClassify(Yuan):
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
        file_type = _File_Type(type_name)
        file_type.set_istype(is_type_func)
        self.file_in_type[type_name] = list()
        self._add_type(file_type)

    def add_ext(self, ext_name:str):
        file_type = _Ext_Type(ext_name)
        self.file_in_type[ext_name] = list()
        self._add_type(file_type)

    def _add_type(self, file_type:_File_Type):
        type_name = file_type.name
        self.all_type[type_name] = file_type
        self.file_in_type[type_name] = list()




