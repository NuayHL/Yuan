import os.path
import warnings
import yaml
import ast
from copy import deepcopy

class ProhibitKeys:
    def __get__(self, instance, owner):
        return [k for k in dir(instance) if not k.startswith('_')] + ['dicts_like']

class DictConfig(dict):
    builtin_keys = ProhibitKeys()

    def __init__(self, *config_dicts):
        super().__init__()
        for config_dict in config_dicts:
            assert isinstance(config_dict, dict), ('The input configs must be \'dict\' type but received \'%s\''
                                                   % type(config_dict))
            for key, val in config_dict.items():
                self._check_builtin_keys(key)
                self[key] = self._hook(val)

    def _hook(self, value):
        if isinstance(value, dict):
            return DictConfig(value)
        return value

    def _check_builtin_keys(self, key):
        assert key not in self.builtin_keys, 'The key \'%s\' is in the builtin name, please change a key name' % key

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __deepcopy__(self, memo=None, _nil=[]):
        if memo is None:
            memo = {}
        d = id(self)
        y = memo.get(d, _nil)
        if y is not _nil:
            return y
        copy_dict = DictConfig()
        memo[d] = id(copy_dict)
        for key in self.keys():
            copy_dict.__setattr__(deepcopy(key, memo), deepcopy(self.__getattr__(key), memo))
        return copy_dict

    # for multiprocessing or multithreading
    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state):
        self.__dict__.update(state)

    def update(self, dicts_like=None, **other_keys):
        dicts_like = self._gather_dicts(dicts_like=dicts_like, **other_keys)
        for k, v in dicts_like.items():
            self._check_builtin_keys(k)
            self[k] = v

    def update_compatible(self, dicts_like=None, **other_keys):
        dicts_like = self._gather_dicts(dicts_like=dicts_like, **other_keys)
        for k, v in dicts_like.items():
            if isinstance(v, dict) and k in self.keys():
                self[k].update_compatible(v)
            else:
                self._check_builtin_keys(k)
                self[k] = v

    def update_strict(self, dicts_like=None, **other_keys):
        dicts_like = self._gather_dicts(dicts_like=dicts_like, **other_keys)
        for k, v in dicts_like.items():
            assert k in self.keys(), 'The update_strict() only allows to update the existing key-values, ' \
                                     'adding new keys is prohibited. key \'%s\' does not exist.' % k
            assert isinstance(v, DictConfig) == isinstance(self[k], DictConfig), \
                'The update_strict() only allows to update the existing key-values, adding or deleting new keys '\
                'are prohibited. key \'%s\' is a node/leaf, but changes to leaf/node' % k
            if isinstance(v, DictConfig):
                self[k].update_strict(v)
            else:
                self[k] = v

    def _update(self, update_type='default', dicts_like=None, **other_keys):
        if update_type == 'default':
            self.update(dicts_like=dicts_like, **other_keys)
        elif update_type == 'compatible':
            self.update_compatible(dicts_like=dicts_like, **other_keys)
        elif update_type == 'strict':
            self.update_strict(dicts_like=dicts_like, **other_keys)
        else:
            raise NotImplementedError(f'Unsupported update type \'{update_type}\'')

    @staticmethod
    def _gather_dicts(dicts_like, **other_keys):
        if isinstance(dicts_like, dict):
            if not isinstance(dicts_like, DictConfig):
                dicts_like = DictConfig(dicts_like)
            other_keys = DictConfig(other_keys)
            dict.update(dicts_like, other_keys)
        else:
            if dicts_like is not None:
                warnings.warn('the type of the given variable for update is not \'dict\' or \'DictConfig\', ignored')
            dicts_like = DictConfig(other_keys)
        return dicts_like

    def dump_to_dict(self, exclude=None):
        if exclude:
            if isinstance(exclude, str):
                exclude = [exclude]
            assert isinstance(exclude, list), 'exclude list must be one str key or a list of str key'
        output_dict = dict()
        for k, v in self.items():
            if exclude:
                if k in exclude:
                    continue
            if isinstance(v, DictConfig):
                output_dict[k] = v.dump_to_dict(exclude=exclude)
            else:
                output_dict[k] = v
        return output_dict

    def __str__(self):
        def make_indent(in_str, num_spaces):
            format_str = in_str.split("\n")
            if len(format_str) == 1:
                return in_str
            first = format_str.pop(0)
            format_str = [(num_spaces * " ") + line for line in format_str]
            format_str = "\n".join(format_str)
            format_str = first + "\n" + format_str
            return format_str

        r = ""
        s = []
        for k, v in self.items():
            seperator = "\n" if isinstance(v, DictConfig) else " "
            attr_str = "{}:{}{}".format(str(k), seperator, str(v))
            attr_str = make_indent(attr_str, 2)
            s.append(attr_str)
        r += "\n".join(s)
        return r

class Config(DictConfig):
    def __init__(self, *configs, **direct_keys):
        dict_list = list()
        for config in configs:
            if isinstance(config, str):
                dict_list.append(self._file_to_dict(config))
            elif isinstance(config, dict):
                dict_list.append(config)
            else:
                raise Exception('unknown type of config, currently supported: type(dict), file(.yaml), file(.py)')
        dict_list.append(direct_keys)
        super().__init__(*dict_list)

    def _hook(self, value):
        if isinstance(value, dict):
            return Config(value)
        return value

    def dump_to_yaml(self, filename):
        with open(filename + '.yaml', 'w') as f:
            print(str(self), file=f)

    def update_from_files(self, *files, type='compatible'):
        for file in files:
            temp_dict = self._file_to_dict(file)
            if type == 'compatible':
                self.update_compatible(temp_dict)
            elif type == 'strict':
                self.update_strict(temp_dict)
            elif type == 'default':
                self.update(temp_dict)
            else:
                raise Exception('updata type should be in [deault, compatiable, strict], received \'%s\'' % type)

    @staticmethod
    def _file_to_dict(filename):
        return _Config_File_IO.read(filename)

    def find_key_value(self, key):
        """return all the node value which has the key name. If the node is a Config, return True"""
        key_dict = dict()
        for k, v in self.items():
            if k == key:
                if not isinstance(v, Config):
                    key_dict[k] = v
                else:
                    key_dict[k] = True
            if isinstance(v, Config):
                _key_dict = v.find_key_value(key)
                _key_dict = self._update_key_dict(k, _key_dict)
                key_dict.update(_key_dict)
        return key_dict

    @staticmethod
    def _update_key_dict(pre_key: str, key_dict: dict):
        fin_key_dict = dict()
        for k, v in key_dict.items():
            fin_key_dict[pre_key+'.'+k] = key_dict[k]
        return fin_key_dict


_MAIN_CONFIG_KEY = 'config'
_EXTRA_CONFIG_KEY = '_extra_'
_BASE_CONFIG_KEY = '_base_'
_CONFIG_PATH_KEY = '_path_'
_CONFIG_TYPE_KEY = '_type_'

from pathlib import Path
class ConfigTree:
    def __init__(self, config_dict, base_list, extra_list):
        self._dict = config_dict
        self._base = base_list
        self._extra = extra_list

    def generate(self):
        fin_dict = DictConfig(self._dict)
        for node in self._base:
            _type = node['update_type']
            _base_node = node['node'].generate()
            _base_node._update(_type, fin_dict)
            fin_dict = _base_node
        for node in self._extra:
            _type = node['update_type']
            fin_dict._update(_type, node['node'].generate())
        return fin_dict

class _Config_File_IO:
    @classmethod
    def read(cls, filename):
        return cls._file2node(filename).generate()

    @classmethod
    def _file2node(cls, filename, incoming_filename: Path=None, from_node=None):
        _read_func = None
        if _is_yaml_file(filename):
            _read_func = _read_from_yaml
        elif _is_py_file(filename):
            _read_func = _read_from_py
        else:
            raise Exception(f'Cannot load unknown type file "{filename}" to config')
        _temp_dict, _extra_files, _base_files = _read_func(filename)

        # remove the cycle citation and warning if have
        current_dir = os.path.dirname(filename)
        current_file = Path(filename).resolve()
        extra_dict_list = list()
        base_dict_list = list()
        for base_dict in _base_files:
            _target_file = Path(os.path.join(current_dir, base_dict[_CONFIG_PATH_KEY])).resolve()
            if from_node == 'extra' and _target_file == incoming_filename:
                warnings.warn(f'Cycle citation happened between {current_file} and {_target_file}')
                continue
            base_dict_list.append(dict(node=_Config_File_IO._file2node(filename=str(_target_file),
                                                                       incoming_filename=current_file,
                                                                       from_node='base'),
                                       update_type=base_dict[_CONFIG_TYPE_KEY]))
        for extra_dict in _extra_files:
            _target_file = Path(os.path.join(current_dir, extra_dict[_CONFIG_PATH_KEY])).resolve()
            if from_node == 'base' and _target_file == incoming_filename:
                warnings.warn(f'Cycle citation happened between {current_file} and {_target_file}')
                continue
            extra_dict_list.append(dict(node=_Config_File_IO._file2node(filename=str(_target_file),
                                                                        incoming_filename=current_file,
                                                                        from_node='extra'),
                                        update_type=extra_dict[_CONFIG_TYPE_KEY]))
        return ConfigTree(_temp_dict, base_dict_list, extra_dict_list)

def _CHECK_LIST(things):
    if not isinstance(things, list):
        things = [things]
    return things

# File IO for yaml file
def _is_yaml_file(filename):
    return filename.endswith(('.yml', '.yaml'))

def _read_from_yaml(filename):
    with open(filename, 'r') as f:
        dicts = yaml.safe_load(f)
    if _EXTRA_CONFIG_KEY in dicts.keys():
        extra_config = _CHECK_LIST(dicts[_EXTRA_CONFIG_KEY])
        del dicts[_EXTRA_CONFIG_KEY]
    else:
        extra_config = []
    if _BASE_CONFIG_KEY in dicts.keys():
        base_config = _CHECK_LIST(dicts[_BASE_CONFIG_KEY])
        del dicts[_BASE_CONFIG_KEY]
    else:
        base_config = []
    return dicts, extra_config, base_config

# File IO for .py file
def _is_py_file(filename):
    return filename.endswith('.py')

def _read_from_py(filename):
    with open(filename, encoding='utf-8') as f:
        codes = ast.parse(f.read())
    codeobj = compile(codes, '', mode='exec')
    global_locals_var = dict()
    eval(codeobj, global_locals_var, global_locals_var)
    fin_dict = global_locals_var[_MAIN_CONFIG_KEY]
    extra_list = _CHECK_LIST(global_locals_var[_EXTRA_CONFIG_KEY])\
        if _EXTRA_CONFIG_KEY in global_locals_var.keys() else []
    base_list = _CHECK_LIST(global_locals_var[_BASE_CONFIG_KEY]) \
        if _BASE_CONFIG_KEY in global_locals_var.keys() else []
    return fin_dict, extra_list, base_list


