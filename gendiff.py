import argparse
from scripts.data_loader import load_data
from formatters.stylish import stylish
from formatters.stylish_plain import stylish_plain
from formatters.stylish_json import stylish_json

FORMATTER_STYLISH = 'stylish'
FORMATTER_PLAIN = 'plain'
FORMATTER_JSON = 'json'


def main():
    parser = argparse.ArgumentParser(description='Generate diff.')
    parser.add_argument('path_to_first_file')
    parser.add_argument('path_to_second_file')
    parser.add_argument('-f', '--format', choices=['stylish', 'plain', 'json'],
                        help='set format of output, valid formats are json,'
                             ' plain, tree. Default format is tree.',
                        default='stylish')
    args = parser.parse_args()
    diff = generate_diff(args.path_to_first_file,
                         args.path_to_second_file,
                         args.format)
    print(diff)


def generate_diff(path_to_first_file,
                  path_to_second_file,
                  formatter_name=FORMATTER_STYLISH):
    source = load_data(path_to_first_file)
    changed_source = load_data(path_to_second_file)
    if isinstance(source, dict) and isinstance(changed_source, dict):
        formatter = get_format_func(formatter_name)
        raw_diff = make_raw_diff(source, changed_source)
        styled_dif = formatter(raw_diff)
        return styled_dif


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


def get_format_func(format_type):
    if format_type == FORMATTER_STYLISH:
        return stylish
    elif format_type == FORMATTER_PLAIN:
        return stylish_plain
    elif format_type == FORMATTER_JSON:
        return stylish_json
    else:
        raise AttributeError('Неверно указан тип форматтера')


if __name__ == '__main__':
    main()
