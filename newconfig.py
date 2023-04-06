import warnings

import yaml
import os

class ProhibitKeys:
    def __get__(self, instance, owner):
        return [k for k in dir(instance) if not k.startswith('_')]

class DictConfig(dict):
    builtin_keys = ProhibitKeys()

    def __init__(self, *config_dicts):
        super().__init__()
        for config_dict in config_dicts:
            assert isinstance(config_dict, dict), 'The input configs must be \'dict\' type.'
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
                                     'add new keys is prohibited. key %s dose not exist.' % k
            assert isinstance(v, DictConfig) == isinstance(self[k], DictConfig), \
                'The update_strict() only allows to update the existing key-values, add or del new keys ' \
                'are prohibited. key %s is a node/leaf, but change to leaf/node' % k
            if isinstance(v, DictConfig):
                self[k].update_strict(v)
            else:
                self[k] = v

class Config(DictConfig):
    def __init__(self, *configs, **direct_keys):
        dict_list = list()
        for config in configs:
            if isinstance(config, str):
                if _is_yaml_file(config):
                    dict_list.append(_read_from_yaml(config))
            elif isinstance(config, dict):
                dict_list.append(config)
            else:
                raise Exception('') # TODO
        dict_list.append(direct_keys)
        super().__init__(*dict_list)

    def dump_to_yaml(self):
        pass #TODO

    def read_from_yaml_files(self, *files):
        pass #TODO


def _is_yaml_file(filename):
    return filename.endswith(('.yml', '.yaml'))

def _read_from_yaml(filename):
    with open(filename, 'r') as f:
        dicts = yaml.safe_load(f)
    return dicts


