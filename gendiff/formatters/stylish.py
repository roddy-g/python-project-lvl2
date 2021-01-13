from gendiff.diff_generator.constants import\
    COMMON, ADDED, DELETED, UNIQUE, NODE, CHANGED, UNCHANGED, BASE_INDENT,\
    INDENT_DELETED, INDENT_ADDED, INDENT_COMMON, BASE_TEMPLATE
from gendiff.formatters.format_built_in_consts\
    import format_built_in_constants


def stylish(raw_diff, level=0):
    format_built_in_constants(raw_diff)
    indent = BASE_INDENT * level
    styled_diff = []
    for key in sorted(raw_diff.keys()):
        data = raw_diff[key]
        special_indent = get_indent_type(data['status'])
        if data['key_type'] in [UNIQUE, UNCHANGED]:
            value = format_value(data['value'], level=level + 1)
            styled_diff.append(BASE_TEMPLATE.format(
                indent, special_indent, key, value))
        elif data['key_type'] == CHANGED:
            value_before = format_value(
                data['value']['before'], level=level + 1)
            value_after = format_value(
                data['value']['after'], level=level + 1)
            styled_diff.append(BASE_TEMPLATE.format(
                indent, INDENT_DELETED, key, value_before))
            styled_diff.append(BASE_TEMPLATE.format(
                indent, INDENT_ADDED, key, value_after))
        elif data['key_type'] == NODE:
            child_value = stylish(data['value'], level=level + 1)
            styled_diff.append(BASE_TEMPLATE.format(
                indent, special_indent, key, child_value))
    styled_diff = make_wrapped_string(styled_diff, indent)
    return styled_diff


def get_indent_type(status):
    if status == DELETED:
        return INDENT_DELETED
    elif status == ADDED:
        return INDENT_ADDED
    elif status == COMMON:
        return INDENT_COMMON


def format_value(data, level):
    result = []
    indent = BASE_INDENT * level
    if not isinstance(data, dict):
        return data
    for key in data:
        if isinstance(data[key], dict):
            value = format_value(data[key], level=level + 1)
        else:
            value = data[key]
        result.append(BASE_TEMPLATE.format(BASE_INDENT, indent, key, value))
    result = make_wrapped_string(result, indent)
    return result


def make_wrapped_string(data, indent):
    data.insert(0, '{')
    data.append('{}}}'.format(indent))
    data = '\n'.join(data)
    return data
