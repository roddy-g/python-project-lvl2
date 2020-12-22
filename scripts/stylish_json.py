from json import dumps


def stylish_json(raw_diff):
    data = dumps(raw_diff, sort_keys=True, indent=1)
    return data
