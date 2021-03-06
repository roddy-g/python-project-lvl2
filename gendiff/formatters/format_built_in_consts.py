def format_built_in_constants(raw_diff):
    for key in raw_diff:
        if isinstance(raw_diff[key], dict):
            format_built_in_constants(raw_diff[key])
        else:
            raw_diff[key] = transform_built_in(raw_diff[key])


def transform_built_in(value):
    if value is True:
        return 'true'
    elif value is False:
        return 'false'
    elif value is None:
        return 'null'
    else:
        return value
