from diff_generator.constants import TEMPLATE_REMOVED, TEMPLATE_UPDATED,\
    TEMPLATE_ADDED, COMMON, ADDED, DELETED, NODE, CHANGED
from diff_generator.formatters.format_built_in_consts\
    import format_built_in_constants


def stylish_plain(raw_diff, parent=''):
    format_built_in_constants(raw_diff)
    styled_diff = []
    for key in sorted(raw_diff.keys()):
        data = raw_diff[key]
        key_parent = format_parent(parent, key)
        if data['status'] == ADDED:
            value = format_value(data['value'])
            styled_diff.append(TEMPLATE_ADDED.format(key_parent, value))
        elif data['status'] == DELETED:
            styled_diff.append(TEMPLATE_REMOVED.format(key_parent, key))
        elif data['status'] == COMMON:
            if data['key_type'] == CHANGED:
                value_before = format_value(data['value']['before'])
                value_after = format_value(data['value']['after'])
                styled_diff.append(TEMPLATE_UPDATED.format(
                    key_parent, value_before, value_after))
            elif data['key_type'] == NODE:
                child_diff = stylish_plain(data['value'], parent=key_parent)
                styled_diff.append(child_diff)
    styled_diff = '\n'.join(styled_diff)
    return styled_diff


def format_value(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif value in ['true', 'false', 'null']:
        return "{}".format(value)
    elif isinstance(value, str):
        return "'{}'".format(value)
    return value


def format_parent(parent, key):
    if parent:
        formatted_parent = '.'.join([parent, key])
    else:
        formatted_parent = '{}'.format(key)
    return formatted_parent
