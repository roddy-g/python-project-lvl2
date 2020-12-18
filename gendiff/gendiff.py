import argparse
from gendiff.data_loader import load_data
from gendiff.stylish import stylish_tree


def main():
    parser = argparse.ArgumentParser(description='Generate diff.')
    parser.add_argument('path_to_first_file')
    parser.add_argument('path_to_second_file')
    parser.add_argument('-f', '--format',
                        help='set format of output', default=stylish_tree)
    args = parser.parse_args()
    if args.format == 'stylish_tree':
        formatter = stylish_tree
    first_file_data = load_data(args.path_to_first_file)
    second_file_data = load_data(args.path_to_second_file)
    diff = generate_diff(first_file_data, second_file_data, formatter)
    print(diff)
    return diff


def generate_diff(source, changed_source, formatter, level=0):
    diff = {}
    for key in source:
        if key not in changed_source:
            diff[key] = {
                'status': 'deleted',
                'value': source[key]
            }
        elif type(source[key]) == dict and type(changed_source[key]) == dict:
            child_diff = generate_diff(source[key], changed_source[key],
                                       formatter, level=level+1)
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
    return formatter(diff, level=level)


if __name__ == '__main__':
    main()
