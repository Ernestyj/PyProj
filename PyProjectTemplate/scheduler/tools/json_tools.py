# -*- coding: utf-8 -*-
import json


class JsonConf():
    def __init__(self):
        pass

    def write_json_conf(self, path, config):
        with open(path, 'w') as f:
            json.dump(config, f)

    def get_json_conf(self, path):
        with open(path, 'r') as f:
            config = json.load(f)
        return config

