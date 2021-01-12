from diff_generator.functions import load_data, get_format_func
from diff_generator.constants import COMMON, ADDED, DELETED, UNIQUE, NODE, \
    CHANGED, UNCHANGED, FORMAT_TREE


def generate_diff(path_to_first_file,
                  path_to_second_file,
                  formatter_name=FORMAT_TREE):
    source = load_data(path_to_first_file)
    changed_source = load_data(path_to_second_file)
    if isinstance(source, dict) and isinstance(changed_source, dict):
        formatter = get_format_func(formatter_name)
        raw_diff = make_raw_diff(source, changed_source)
        styled_dif = formatter(raw_diff)
        return styled_dif


def make_raw_diff(source, changed_source):
    diff = {}
    all_keys = set(list(source.keys()) + list(changed_source.keys()))
    for key in all_keys:
        if key not in changed_source:
            status = DELETED
            key_type = UNIQUE
            value = source[key]
        elif key not in source:
            status = ADDED
            key_type = UNIQUE
            value = changed_source[key]
        else:
            status = COMMON
            key_type, value = compare_common_keys_values(
                source[key], changed_source[key])
        diff[key] = {
            'status': status,
            'key_type': key_type,
            'value': value
        }
    return diff


def compare_common_keys_values(value_1, value_2):
    if isinstance(value_1, dict) \
            and isinstance(value_2, dict):
        key_type = NODE
        value = make_raw_diff(value_1, value_2)
    elif value_1 != value_2:
        key_type = CHANGED
        value = {
            'before': value_1,
            'after': value_2
        }
    else:
        key_type = UNCHANGED
        value = value_2
    return key_type, value
