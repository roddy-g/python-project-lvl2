from json import load as json_load
from yaml import safe_load as yaml_load
from gendiff.constants import FORMAT_TREE, FORMAT_PLAIN, FORMAT_JSON
from gendiff.formatters.stylish import stylish
from gendiff.formatters.stylish_json import stylish_json
from gendiff.formatters.stylish_plain import stylish_plain


def load_data(path_to_file):
    filetype = path_to_file.split('.')[-1].lower()
    with open(path_to_file) as data:
        if filetype == 'json':
            data = json_load(data)
            return data
        elif filetype in ['yml', 'yaml']:
            data = yaml_load(data)
            return data
        else:
            raise ValueError('Неверный тип данных')


def get_format_func(format_type):
    if format_type == FORMAT_TREE:
        return stylish
    elif format_type == FORMAT_PLAIN:
        return stylish_plain
    elif format_type == FORMAT_JSON:
        return stylish_json
    else:
        raise ValueError('Неверно указан тип форматтера')
