REMOVED = "Property '{}' was removed"
UPDATED = "Property '{}' was updated. From {} to {}"
ADDED = "Property '{}' was added with value: {}"


def stylish_plain(raw_diff, parent=''):
    styled_diff = []
    for key in sorted(raw_diff.keys()):
        data = raw_diff[key]
        formatted_parent = format_parent(parent, key)
        if data['status'] == 'added':
            formatted_value = format_value(data['value'])
            styled_diff.append(ADDED.format(
                formatted_parent, formatted_value))
        elif data['status'] == 'deleted':
            styled_diff.append(REMOVED.format(formatted_parent, key))
        elif data['status'] == 'common':
            if data['key_type'] == 'changed':
                formatted_value_before = format_value(data['value']['before'])
                formatted_value_after = format_value(data['value']['after'])
                styled_diff.append(UPDATED.format(formatted_parent,
                                                  formatted_value_before,
                                                  formatted_value_after))
            elif data['key_type'] == 'node':
                child_diff = stylish_plain(data['value'],
                                           parent=formatted_parent)
                styled_diff.append(child_diff)
    styled_diff = '\n'.join(styled_diff)
    styled_diff = styled_diff.replace('True', 'true')
    styled_diff = styled_diff.replace('False', 'false')
    styled_diff = styled_diff.replace('None', 'null')
    return styled_diff


def format_value(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, str):
        return "'{}'".format(value)
    return value


def format_parent(parent, key):
    if parent:
        formatted_parent = '.'.join([parent, key])
    else:
        formatted_parent = '{}'.format(key)
    return formatted_parent
