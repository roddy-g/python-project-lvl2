import argparse
from gendiff.data_loader import load_data

INDENT_IF_DELETED = '  - '
INDENT_IF_ADDED = '  + '
BASE_INDENT = '    '


def main():
    parser = argparse.ArgumentParser(description='Generate diff.')
    parser.add_argument('path_to_first_file')
    parser.add_argument('path_to_second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    first_file_data = load_data(args.path_to_first_file)
    second_file_data = load_data(args.path_to_second_file)
    diff = generate_diff(first_file_data, second_file_data)
    result = stylish(diff)
    print(result)
    return result


def generate_diff(source, changed_source):
    diff = {}
    for key in source:
        if key not in changed_source:
            diff[key] = {
                'status': 'deleted',
                'value': source[key]
            }
            continue
        if type(source[key]) == dict and type(changed_source[key]) == dict:
            child_diff = generate_diff(source[key], changed_source[key])
            diff[key] = {
                'status': 'common',
                'value': child_diff
            }
            continue
        if source[key] == changed_source[key]:
            diff[key] = {
                'status': 'common',
                'value': source[key]
            }
            continue
        if source[key] != changed_source[key]:
            diff[key] = {
                'status': 'changed',
                'value': [source[key], changed_source[key]]
            }
            continue
    for key in changed_source:
        if key not in source:
            diff[key] = {
                'status': 'added',
                'value': changed_source[key]
            }
    return diff


def stylish(raw_diff, level=0):
    indent = BASE_INDENT * level
    styled_diff = []
    for key in sorted(raw_diff.keys()):
        data = raw_diff[key]
        try:
            if type(data['value']) == dict:
                formatted_value = stylish(data['value'], level=level+1)
                styled_diff.append('{}{}{}: {}'.format(
                    indent, BASE_INDENT, key, formatted_value))
                continue
        except (TypeError, KeyError):
            pass
        if data['status'] == 'changed':
            formatted_value_before = represent(
                data['value'][0], level=level + 1)
            formatted_value_after = represent(
                data['value'][1], level=level + 1)
            styled_diff.append('{}{}{}: {}'.format(
                indent, INDENT_IF_DELETED, key, formatted_value_before))
            styled_diff.append('{}{}{}: {}'.format(
                indent, INDENT_IF_ADDED, key, formatted_value_after))
            continue
        formatted_value = represent(data['value'], level=level + 1)
        if data['status'] == 'deleted':
            styled_diff.append('{}{}{}: {}'.format(
                indent, INDENT_IF_DELETED, key, formatted_value))
        elif data['status'] == 'added':
            styled_diff.append('{}{}{}: {}'.format(
                indent, INDENT_IF_ADDED, key, formatted_value))
        elif data['status'] == 'common':
            styled_diff.append('{}{}{}: {}'.format(
                indent, BASE_INDENT, key, formatted_value))
    styled_diff = wrap(styled_diff, indent)
    styled_diff = styled_diff.replace('True', 'true')
    styled_diff = styled_diff.replace('False', 'false')
    styled_diff = styled_diff.replace('None', 'null')
    return styled_diff


def represent(data, level):
    result = []
    indent = BASE_INDENT * level
    if type(data) != dict:
        return data
    for key in data:
        if type(data[key]) != dict:
            result.append('{}{}{}: {}'.format(
                indent, BASE_INDENT, key, data[key]))
        else:
            value = represent(data[key], level=level+1)
            result.append('{}{}{}: {}'.format(
                indent, BASE_INDENT, key, value))
    result = wrap(result, indent)
    return result


def wrap(data, indent):
    data.insert(0, '{')
    data.append('{}}}'.format(indent))
    data = '\n'.join(data)
    return data


if __name__ == '__main__':
    main()
