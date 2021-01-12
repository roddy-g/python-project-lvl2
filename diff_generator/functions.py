from json import load as json_load
from yaml import safe_load as yaml_load
from diff_generator.constants import FORMAT_TREE, FORMAT_PLAIN, FORMAT_JSON
from diff_generator.formatters.stylish import stylish
from diff_generator.formatters.stylish_json import stylish_json
from diff_generator.formatters.stylish_plain import stylish_plain


def load_data(path_to_file):
    with open(path_to_file) as data:
        if path_to_file[-5:] == '.json':
            data = json_load(data)
            return data
        if path_to_file[-4:] == '.yml' or path_to_file[-5:] == '.yaml':
            data = yaml_load(data)
            return data


def get_format_func(format_type):
    if format_type == FORMAT_TREE:
        return stylish
    elif format_type == FORMAT_PLAIN:
        return stylish_plain
    elif format_type == FORMAT_JSON:
        return stylish_json
    else:
        raise AttributeError('Неверно указан тип форматтера')
