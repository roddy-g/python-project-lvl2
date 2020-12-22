BASE_INDENT = '    '
TEMPLATE_DELETED = '{}  - {}: {}'
TEMPLATE_ADDED = '{}  + {}: {}'
TEMPLATE_COMMON = '{}    {}: {}'


def stylish_tree(raw_diff, level=0):
    indent = BASE_INDENT * level
    styled_diff = []
    for key in sorted(raw_diff.keys()):
        data = raw_diff[key]
        try:
            if type(data['value']) == dict:
                formatted_value = stylish_tree(data['value'], level=level + 1)
                styled_diff.append(TEMPLATE_COMMON.format(
                    indent, key, formatted_value))
                continue
        except (TypeError, KeyError):
            pass
        if data['status'] == 'changed':
            formatted_value_before = format_child_value(
                data['value']['before'], level=level + 1)
            formatted_value_after = format_child_value(
                data['value']['after'], level=level + 1)
            styled_diff.append(TEMPLATE_DELETED.format(
                indent, key, formatted_value_before))
            styled_diff.append(TEMPLATE_ADDED.format(
                indent, key, formatted_value_after))
            continue
        formatted_value = format_child_value(data['value'], level=level + 1)
        if data['status'] == 'deleted':
            styled_diff.append(TEMPLATE_DELETED.format(
                indent, key, formatted_value))
        elif data['status'] == 'added':
            styled_diff.append(TEMPLATE_ADDED.format(
                indent, key, formatted_value))
        elif data['status'] == 'common':
            styled_diff.append(TEMPLATE_COMMON.format(
                indent, key, formatted_value))
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
            result.append(TEMPLATE_COMMON.format(
                indent, key, data[key]))
        else:
            value = format_child_value(data[key], level=level + 1)
            result.append(TEMPLATE_COMMON.format(
                indent, key, value))
    result = make_wrapped_string(result, indent)
    return result


def make_wrapped_string(data, indent):
    data.insert(0, '{')
    data.append('{}}}'.format(indent))
    data = '\n'.join(data)
    return data
