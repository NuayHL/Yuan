import warnings
import yaml

class ProhibitKeys:
    def __get__(self, instance, owner):
        return [k for k in dir(instance) if not k.startswith('_')] + ['dicts_like']

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
                if _is_yaml_file(config):
                    dict_list.append(_read_from_yaml(config))
                else:
                    raise Exception('unknown type of config file, currently supported: yaml')
            elif isinstance(config, dict):
                dict_list.append(config)
            else:
                raise Exception('unknown type of config, currently supported: type(dict), file(.yaml)')
        dict_list.append(direct_keys)
        super().__init__(*dict_list)

    def _hook(self, value):
        if isinstance(value, dict):
            return Config(value)
        return value

    def dump_to_yaml(self, filename):
        with open(filename + '.yaml', 'w') as f:
            print(str(self), file=f)

    def update_from_yamls(self, *yamlfiles):
        for file in yamlfiles:
            with open(file, 'r') as f:
                conf_dict = yaml.safe_load(f)
                self.update(conf_dict)

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


def _is_yaml_file(filename):
    return filename.endswith(('.yml', '.yaml'))

def _read_from_yaml(filename):
    with open(filename, 'r') as f:
        dicts = yaml.safe_load(f)
    return dicts


