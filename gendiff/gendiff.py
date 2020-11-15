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


def generate_diff(first_file, second_file):
    diff = []
    unique_keys = set(list(first_file.keys()) + list(second_file.keys()))
    for key in sorted(unique_keys):
        first_file_value = first_file.get(key)
        second_file_value = second_file.get(key)
        if first_file_value is not None and second_file_value is not None:
            if first_file_value == second_file_value:
                diff.append('   {}:{}'.format(key, first_file_value))
            else:
                diff.append(' - {}:{}'.format(key, first_file_value))
                diff.append(' + {}:{}'.format(key, second_file_value))
        elif second_file_value is not None:
            diff.append(' + {}:{}'.format(key, second_file_value))
        elif first_file_value is not None:
            diff.append(' - {}:{}'.format(key, first_file_value))
    return '{{\n{}\n}}'.format('\n'.join(diff))


if __name__ == '__main__':
    main()
