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
        if isinstance(dicts_like, dict):
            if not isinstance(dicts_like, DictConfig):
                dicts_like = DictConfig(dicts_like)
            other_keys = DictConfig(other_keys)
            dict.update(dicts_like, other_keys)
        else:
            if dicts_like is not None:
                warnings.warn('the type of the given variable for update is not \'dict\' or \'DictConfig\', ignored')
            dicts_like = DictConfig(other_keys)
        for k, v in dicts_like.items():
            self._check_builtin_keys(k)
            self[k] = v

    def update_strict(self, dicts_like=None, **other_keys):
        if isinstance(dicts_like, dict):
            if not isinstance(dicts_like, DictConfig):
                dicts_like = DictConfig(dicts_like)
        else:
            if dicts_like is not None:
                warnings.warn('the type of the given variable for update is not \'dict\' or \'DictConfig\', ignored')
        dicts_like.update(other_keys)
        for k, v in dicts_like.items():
            assert k in self.keys(), 'The update_strict() only allows to update the existing key-values, ' \
                                     'add new keys is prohibited. key %s does not exist.' % k
            assert isinstance(v, DictConfig) == isinstance(self[k], DictConfig), \
                'The update_strict() only allows to update the existing key-values, add or del new keys ' \
                'are prohibited. key %s is a node/leaf, but change to leaf/node' % k
            if isinstance(v, DictConfig):
                self[k].update_strict(v)
            else:
                self[k] = v

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
                dict_list.extend(self._file_to_dict(config))
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

    def update_from_files(self, *files, strict=True):
        for file in files:
            temp_dict_list = self._file_to_dict(file)
            for temp_dict in temp_dict_list:
                if strict:
                    self.update_strict(temp_dict)
                else:
                    self.update(temp_dict)

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


class _Config_File_IO:
    @classmethod
    def read(cls, filename):
        _read_func = None
        if _is_yaml_file(filename):
            _read_func = _read_from_yaml
        elif _is_py_file(filename):
            _read_func = _read_from_py
        else:
            raise Exception(f'Cannot load unknown type file "{filename}" to config')
        _temp_dicts, config_files_list = _read_func(filename)
        current_path = os.path.dirname(filename)
        dict_list = [_temp_dicts]
        for config_file in config_files_list:
            dict_list.extend(cls.read(os.path.join(current_path, config_file)))
        return dict_list


_MAIN_CONFIG_KEY = 'config'
_EXTRA_CONFIG_KEY = '_extra_'

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
        return dicts, extra_config
    else:
        return dicts, []

# File IO for .py file
def _is_py_file(filename):
    return filename.endswith('.py')

def _read_from_py(filename):
    with open(filename, encoding='utf-8') as f:
        codes = ast.parse(f.read())
    codeobj = compile(codes, '', mode='exec')
    # Support load global variable in nested function of the
    # config.
    global_locals_var = dict()
    eval(codeobj, global_locals_var, global_locals_var)
    fin_dict = global_locals_var[_MAIN_CONFIG_KEY]
    extra_list = _CHECK_LIST(global_locals_var[_EXTRA_CONFIG_KEY])\
        if _EXTRA_CONFIG_KEY in global_locals_var.keys() else []
    return fin_dict, extra_list


