# -*- coding: utf-8 -*-

import json

def write_json_conf(path, config):
    with open(path, 'w') as f:
        json.dump(config, f)

def get_json_conf(path):
    with open(path, 'r') as f:
        config = json.load(f)
    return config


config = {'key1': 'value1',
          'key2': 'value2'}
path = 'config.json'
# write_json_conf(config=config, path=path)
print get_json_conf(path)