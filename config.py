import yaml
import os
from yacs.config import CfgNode as _CN
from copy import deepcopy

class Config(_CN):
    def dump_to_file_yaml(self, yaml_name=None, path=''):
        cfg_string = self.dump()
        if yaml_name is None:
            assert hasattr(self, 'exp_name')
            file_name = self.exp_name
        else:
            file_name = yaml_name
        with open(os.path.join(path,file_name + '.yaml'), "w") as f:
            f.write(cfg_string)

    def dump_to_file(self, yaml_name=None, path=''):
        if yaml_name is None:
            assert hasattr(self, 'exp_name')
            file_name = self.exp_name
        else:
            file_name = yaml_name
        with open(os.path.join(path,file_name + '.yaml'), "w") as f:
            print(self, file=f)

    def dump_to_split_file(self, yaml_name=None, path='', split_keys=[]):
        index = 1
        fin_path = deepcopy(path)
        if os.path.exists(path):
            fin_path = path + '_%d' % index
            index += 1
        if not os.path.exists(fin_path):
            os.makedirs(fin_path)
        if yaml_name is None:
            assert hasattr(self, 'exp_name')
            file_name = self.exp_name
        else:
            file_name = yaml_name
        for key in split_keys:
            self.dump_key(key, file_name, fin_path)
        self.dump_except_key(split_keys, file_name, fin_path)

    def merge_from_files(self, file_path):
        if '.yaml' in file_path:
            self.merge_from_file(file_path)
        elif os.path.exists(file_path):
            cfg_files = os.listdir(file_path)
            for cfg in cfg_files:
                if '.yaml' not in cfg: continue
                self.merge_from_file(os.path.join(file_path, cfg))
        else:
            print(file_path)
            raise FileNotFoundError('Config path not exists')

    def dump_key(self, key, file_name, path=''):
        if not hasattr(self, key):
            raise AttributeError
        dummy_cn = Config()
        dummy_cn.__setattr__(key,deepcopy(self.__getattr__(key)))
        dummy_cn.dump_to_file(file_name + '_'+key, path)

    def dump_except_key(self, keys, file_name, path=''):
        dummy_cn = Config()
        for key in self.keys():
            if key not in keys:
                dummy_cn.__setattr__(key, deepcopy(self.__getattr__(key)))
        dummy_cn.dump_to_file(file_name + '_else', path)
