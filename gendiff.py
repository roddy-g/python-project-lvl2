import argparse
from diff_generator.functions import load_data,\
    FORMAT_TREE, FORMAT_PLAIN, FORMAT_JSON, get_format_func
from diff_generator.generate_diff import make_raw_diff


def main():
    parser = argparse.ArgumentParser(description='Generate diff.')
    parser.add_argument('path_to_first_file')
    parser.add_argument('path_to_second_file')
    parser.add_argument('-f', '--format',
                        choices=[FORMAT_TREE, FORMAT_JSON, FORMAT_PLAIN],
                        help='set format of output, valid formats are json,'
                             ' plain, tree. Default format is tree.',
                        default='stylish')
    args = parser.parse_args()
    diff = generate_diff(args.path_to_first_file,
                         args.path_to_second_file,
                         args.format)
    print(diff)


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


if __name__ == '__main__':
    main()
