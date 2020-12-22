import argparse
from scripts.data_loader import load_data
from scripts.stylish import stylish
from scripts.stylish_plain import stylish_plain
from scripts.stylish_json import stylish_json


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
    return diff


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
    for key in source:
        if key not in changed_source:
            diff[key] = {
                'status': 'deleted',
                'value': source[key],
            }
        elif type(source[key]) == dict and type(changed_source[key]) == dict:
            child_diff = make_raw_diff(source[key], changed_source[key])
            diff[key] = {
                'status': 'common',
                'value': child_diff
            }
        elif source[key] != changed_source[key]:
            diff[key] = {
                'status': 'changed',
                'value': {
                    'before': source[key],
                    'after': changed_source[key]
                }
            }
        else:
            diff[key] = {
                'status': 'common',
                'value': source[key]
            }
    for key in changed_source:
        if key not in source:
            diff[key] = {
                'status': 'added',
                'value': changed_source[key]
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
