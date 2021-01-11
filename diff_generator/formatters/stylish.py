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
        special_indent = get_indent_type(data['status'])
        if data['key_type'] in ['unique', 'unchanged']:
            value = format_value(data['value'], level=level + 1)
            styled_diff.append(TEMPLATE.format(indent,
                                               special_indent, key, value))
        elif data['key_type'] == 'node':
            value = stylish(data['value'], level=level + 1)
            styled_diff.append(TEMPLATE.format(indent,
                                               special_indent, key, value))
        elif data['key_type'] == 'changed':
            value_before = format_value(
                data['value']['before'], level=level + 1)
            styled_diff.append(TEMPLATE.format(
                indent, INDENT_DELETED, key, value_before))
            value_after = format_value(
                data['value']['after'], level=level + 1)
            styled_diff.append(TEMPLATE.format(
                indent, INDENT_ADDED, key, value_after))
    styled_diff = make_wrapped_string(styled_diff, indent)
    styled_diff = styled_diff.replace('True', 'true')
    styled_diff = styled_diff.replace('False', 'false')
    styled_diff = styled_diff.replace('None', 'null')
    return styled_diff


def get_indent_type(status):
    if status == 'deleted':
        return INDENT_DELETED
    elif status == 'added':
        return INDENT_ADDED
    elif status == 'common':
        return INDENT_COMMON


def format_value(data, level):
    result = []
    indent = BASE_INDENT * level
    if not isinstance(data, dict):
        return data
    for key in data:
        if isinstance(data[key], dict):
            value = format_value(data[key], level=level + 1)
            result.append(TEMPLATE.format(
                BASE_INDENT, indent, key, value))
        else:
            result.append(TEMPLATE.format(
                BASE_INDENT, indent, key, data[key]))
    result = make_wrapped_string(result, indent)
    return result


def make_wrapped_string(data, indent):
    data.insert(0, '{')
    data.append('{}}}'.format(indent))
    data = '\n'.join(data)
    return data
