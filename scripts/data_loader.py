from yaml import safe_load as yaml_load
from json import load as json_load


def load_data(path_to_file):
    with open(path_to_file) as data:
        if path_to_file[-5:] == '.json':
            data = json_load(data)
            return data
        if path_to_file[-4:] == '.yml' or path_to_file[-5:] == '.yaml':
            data = yaml_load(data)
            return data
