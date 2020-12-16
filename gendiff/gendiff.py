import argparse
from gendiff.data_loader import load_data

INDENT_IF_UNCNAHGED = '    '
INDENT_IF_DELETED = '  - '
INDENT_IF_ADDED = '  + '

def main():
    parser = argparse.ArgumentParser(description='Generate diff.')
    parser.add_argument('path_to_first_file')
    parser.add_argument('path_to_second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    first_file_data = load_data(args.path_to_first_file)
    second_file_data = load_data(args.path_to_second_file)
    diff = generate_diff(first_file_data, second_file_data)
    return stylish(diff)


def generate_diff(first_file_data, second_file_data):
    diff = {}
    for key in first_file_data:
        if key not in second_file_data:
            diff[key] = {'status': 'deleted',
                         'value': first_file_data[key]}
            continue
        elif first_file_data[key] == second_file_data[key]:
            diff[key] = {'status': 'unchanged',
                         'value': first_file_data[key]}
            continue
        elif first_file_data[key] != second_file_data[key]:
            if first_file_data[key] is dict and second_file_data is dict:
                diff_child = generate_diff(first_file_data[key], second_file_data[key])
                diff[key] = {'status': 'changed',
                             'child_diff_value': diff_child}
            else:
                diff[key] = {'status': 'changed',
                             'value_before': first_file_data[key],
                             'value_after': second_file_data[key]}
    for key in second_file_data:
        if key not in first_file_data:
            diff[key] = {'status': 'added',
                         'value': second_file_data[key]}
    print(stylish(diff))
    return stylish(diff)


def stylish(diff, level=0):
    result = []
    indent = '    ' * level
    for key in sorted(diff.keys()):
        if diff[key]['status'] == 'unchanged':
            result.append('{}{}{}:{}'.format(indent, INDENT_IF_UNCNAHGED, key, diff[key]['value']))
        elif diff[key]['status'] == 'changed':
            if diff[key].get('child_diff_value'):
                stylish(diff[key]['child_diff_value'], level=level+1)
            else:
                result.append('{}{}{}:{}'.format(indent, INDENT_IF_DELETED, key, diff[key]['value_before']))
                result.append('{}{}{}:{}'.format(indent, INDENT_IF_ADDED, key, diff[key]['value_after']))
        elif diff[key]['status'] == 'deleted':
            result.append('{}{}{}:{}'.format(indent, INDENT_IF_DELETED, key, diff[key]['value']))
        elif diff[key]['status'] == 'added':
            result.append('{}{}{}:{}'.format(indent, INDENT_IF_ADDED, key, diff[key]['value']))
    wrap(result)
    formatted_diff = '\n'.join(result)
    return formatted_diff


def wrap(data):
    data.insert(0, '{')
    data.append('}')

if __name__ == '__main__':
    main()
