import argparse
from scripts.data_loader import load_data
from formatters.stylish import stylish
from formatters.stylish_plain import stylish_plain
from formatters.stylish_json import stylish_json


def main():
    parser = argparse.ArgumentParser(description='Generate diff.')
    parser.add_argument('path_to_first_file')
    parser.add_argument('path_to_second_file')
    parser.add_argument('-f', '--format',
                        help='set format of output, valid formats are json,'
                             ' plain, tree. Default format is tree.',
                        default='stylish')
    args = parser.parse_args()
    formatter = args.format
    diff = generate_diff(args.path_to_first_file,
                         args.path_to_second_file,
                         formatter)
    print(diff)


def generate_diff(path_to_first_file,
                  path_to_second_file,
                  formatter='stylish'):
    source = load_data(path_to_first_file)
    changed_source = load_data(path_to_second_file)
    if type(source) != dict and type(changed_source) != dict:
        return 'Incorrect input data'
    formatter = get_format_func(formatter)
    raw_diff = make_raw_diff(source, changed_source)
    styled_dif = formatter(raw_diff)
    return styled_dif


def make_raw_diff(source, changed_source):
    diff = {}
    all_keys = set(list(source.keys())+list(changed_source.keys()))
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
            if type(source[key]) == dict and type(changed_source[key]) == dict:
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
    if format_type == 'stylish':
        return stylish
    elif format_type == 'plain':
        return stylish_plain
    elif format_type == 'json':
        return stylish_json


if __name__ == '__main__':
    main()
