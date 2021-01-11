def make_raw_diff(source, changed_source):
    diff = {}
    all_keys = set(list(source.keys()) + list(changed_source.keys()))
    for key in all_keys:
        if key not in changed_source:
            status = 'deleted'
            key_type = 'unique'
            value = source[key]
        elif key not in source:
            status = 'added'
            key_type = 'unique'
            value = changed_source[key]
        else:
            status = 'common'
            if isinstance(source[key], dict)\
                    and isinstance(changed_source[key], dict):
                key_type = 'node'
                value = make_raw_diff(source[key], changed_source[key])
            elif source[key] != changed_source[key]:
                key_type = 'changed'
                value = {
                    'before': source[key],
                    'after': changed_source[key]
                }
            else:
                key_type = 'unchanged'
                value = source[key]
        diff[key] = {
            'status': status,
            'key_type': key_type,
            'value': value
        }
    return diff