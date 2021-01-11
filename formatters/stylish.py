BASE_INDENT = '    '
INDENT_DELETED = '  - '
INDENT_ADDED = '  + '
INDENT_COMMON = '    '
TEMPLATE = '{}{}{}: {}'


def stylish(raw_diff, level=0):
    indent = BASE_INDENT * level
    styled_diff = []
    for key in sorted(raw_diff.keys()):
        data = raw_diff[key]
        if data['status'] == 'deleted':
            special_indent = INDENT_DELETED
        elif data['status'] == 'added':
            special_indent = INDENT_ADDED
        elif data['status'] == 'common':
            special_indent = INDENT_COMMON
        if data['key_type'] in ['unique', 'unchanged']:
            value = format_child_value(data['value'], level=level + 1)
            styled_diff.append(TEMPLATE.format(indent, special_indent, key, value))
        elif data['key_type'] == 'node':
            value = stylish(data['value'], level=level + 1)
            styled_diff.append(TEMPLATE.format(indent, special_indent, key, value))
        elif data['key_type'] == 'changed':
            value_before = format_child_value(data['value']['before'], level=level + 1)
            styled_diff.append(TEMPLATE.format(indent, INDENT_DELETED, key, value_before))
            value_after = format_child_value(data['value']['after'], level=level + 1)
            styled_diff.append(TEMPLATE.format(indent, INDENT_ADDED, key, value_after))
    styled_diff = make_wrapped_string(styled_diff, indent)
    styled_diff = styled_diff.replace('True', 'true')
    styled_diff = styled_diff.replace('False', 'false')
    styled_diff = styled_diff.replace('None', 'null')
    return styled_diff


def format_child_value(data, level):
    result = []
    indent = BASE_INDENT * level
    if type(data) != dict:
        return data
    for key in data:
        if type(data[key]) != dict:
            result.append('{}{}{}: {}'.format(
                BASE_INDENT, indent, key, data[key]))
        else:
            value = format_child_value(data[key], level=level + 1)
            result.append('{}{}{}: {}'.format(
                BASE_INDENT, indent, key, value))
    result = make_wrapped_string(result, indent)
    return result


def make_wrapped_string(data, indent):
    data.insert(0, '{')
    data.append('{}}}'.format(indent))
    data = '\n'.join(data)
    return data
