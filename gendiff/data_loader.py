from yaml import safe_load as yaml_load
from json import load as json_load


def load_data(path_to_file):
    file = open(path_to_file)
    if path_to_file[-4:] == 'json':
        data = json_load(file)
        return data
    if path_to_file[-3:] == 'yml' or path_to_file[-4:] == 'yaml':
        data = yaml_load(file)
        return data
