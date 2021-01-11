from json import load as json_load
from yaml import safe_load as yaml_load
from diff_generator.formatters.stylish import stylish
from diff_generator.formatters.stylish_json import stylish_json
from diff_generator.formatters.stylish_plain import stylish_plain

FORMAT_TREE = 'stylish'
FORMAT_PLAIN = 'plain'
FORMAT_JSON = 'json'


def make_raw_diff(source, changed_source):
    diff = {}
    all_keys = set(list(source.keys()) + list(changed_source.keys()))
    for key in all_keys:
        if key not in changed_source:
            status = 'deleted'
            key_type = 'unique'
            value = source[key]
        elif key not in source:
            status = 'added'
            key_type = 'unique'
            value = changed_source[key]
        else:
            status = 'common'
            if isinstance(source[key], dict)\
                    and isinstance(changed_source[key], dict):
                key_type = 'node'
                value = make_raw_diff(source[key], changed_source[key])
            elif source[key] != changed_source[key]:
                key_type = 'changed'
                value = {
                    'before': source[key],
                    'after': changed_source[key]
                }
            else:
                key_type = 'unchanged'
                value = source[key]
        diff[key] = {
            'status': status,
            'key_type': key_type,
            'value': value
        }
    return diff


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
