import argparse
from gendiff.diff_generator.constants import FORMAT_TREE,\
    FORMAT_PLAIN, FORMAT_JSON
from gendiff.diff_generator.generate_diff import generate_diff


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


if __name__ == '__main__':
    main()
