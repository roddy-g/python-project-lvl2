import argparse
from gendiff.data_loader import load_data
from gendiff.stylish_tree import stylish_tree
from gendiff.stylish_plain import stylish_plain
from gendiff.stylish_json import stylish_json


def main():
    parser = argparse.ArgumentParser(description='Generate diff.')
    parser.add_argument('path_to_first_file')
    parser.add_argument('path_to_second_file')
    parser.add_argument('-f', '--format',
                        help='set format of output', default=stylish_tree)
    args = parser.parse_args()
    formatter = stylish_tree
    if args.format == 'plain':
        formatter = stylish_plain
    if args.format == 'json':
        formatter = stylish_json
    first_file_data = load_data(args.path_to_first_file)
    second_file_data = load_data(args.path_to_second_file)
    diff = generate_diff(first_file_data, second_file_data, formatter)
    if formatter == stylish_json:
        print(diff)
    return diff


def generate_diff(source, changed_source, formatter):
    raw_diff = make_raw_diff(source, changed_source)
    styled_dif = formatter(raw_diff)
    return styled_dif


def make_raw_diff(source, changed_source):
    diff = {}
    for key in source:
        if key not in changed_source:
            diff[key] = {
                'status': 'deleted',
                'value': source[key]
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
                'value': [source[key], changed_source[key]]
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


if __name__ == '__main__':
    main()
