import argparse
from gendiff.data_loader import load_data


def main():
    parser = argparse.ArgumentParser(description='Generate diff.')
    parser.add_argument('path_to_first_file')
    parser.add_argument('path_to_second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    first_file_data = load_data(args.path_to_first_file)
    second_file_data = load_data(args.path_to_second_file)
    result = generate_diff(first_file_data, second_file_data)
    print(result)


def generate_diff(first_file_data, second_file_data):
    diff = []
    first_file_keys = set(first_file_data.keys())
    second_file_keys = set(second_file_data.keys())
    common_keys = first_file_keys.intersection(second_file_keys)
    changed_keys = set([key for key in common_keys if first_file_data[key]
                        != second_file_data[key]])
    unchanged_keys = common_keys - changed_keys
    deleted_keys = first_file_keys.difference((second_file_keys))
    added_keys = second_file_keys.difference(first_file_keys)
    unique_keys = first_file_keys.union(second_file_keys)
    for key in sorted(unique_keys):
        first_file_value = first_file_data.get(key)
        second_file_value = second_file_data.get(key)
        if key in unchanged_keys:
            diff.append('   {}:{}'.format(key, first_file_value))
        elif key in changed_keys:
            diff.append(' - {}:{}'.format(key, first_file_value))
            diff.append(' + {}:{}'.format(key, second_file_value))
        elif key in deleted_keys:
            diff.append(' - {}:{}'.format(key, first_file_value))
        elif key in added_keys:
            diff.append(' + {}:{}'.format(key, second_file_value))
    return '{{\n{}\n}}'.format('\n'.join(diff))


if __name__ == '__main__':
    main()
