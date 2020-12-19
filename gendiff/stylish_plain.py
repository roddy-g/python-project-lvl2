TEMPLATE_REMOVED = "Property '{}' was removed"
TEMPLATE_UPDATED = "Property '{}' was updated. From {} to {}"
TEMPLATE_ADDED = "Property '{}' was added with value: {}"


def stylish_plain(raw_diff, parent=''):
    styled_diff = []
    if type(raw_diff) != dict:
        return
    for key in sorted(raw_diff.keys()):
        data = raw_diff[key]
        try:
            status = data.get('status')
        except (AttributeError, TypeError, KeyError):
            continue
        formatted_parent = format_parent(parent, key)
        if status == 'added':
            formatted_value = format_value(data['value'])
            styled_diff.append(TEMPLATE_ADDED.format(
                formatted_parent, formatted_value))
        elif status == 'deleted':
            styled_diff.append(TEMPLATE_REMOVED.format(formatted_parent, key))
        elif status == 'changed':
            formatted_value_before = format_value(data['value']['before'])
            formatted_value_after = format_value(data['value']['after'])
            styled_diff.append(TEMPLATE_UPDATED.format(formatted_parent,
                                                       formatted_value_before,
                                                       formatted_value_after))
        try:
            child_data = data.get('value')
        except (AttributeError, TypeError, KeyError):
            continue
        child_diff_parent = format_parent(parent, key)
        child_diff = stylish_plain(child_data, parent=child_diff_parent)
        if child_diff:
            styled_diff.append(child_diff)
    styled_diff = '\n'.join(styled_diff)
    styled_diff = styled_diff.replace('True', 'true')
    styled_diff = styled_diff.replace('False', 'false')
    styled_diff = styled_diff.replace('None', 'null')
    return styled_diff


def format_value(value):
    if type(value) == dict:
        return '[complex value]'
    if type(value) == str:
        return "'{}'".format(value)
    return value


def format_parent(parent, key):
    if parent:
        formatted_parent = '.'.join([parent, key])
    else:
        formatted_parent = '{}'.format(key)
    return formatted_parent
