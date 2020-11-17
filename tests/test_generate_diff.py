from gendiff.gendiff import generate_diff
from gendiff.data_loader import load_data


def test():
    correct_diff = open('tests/fixtures/correct_diff_for_simple_files.txt').read()
    first_file_data = load_data('tests/fixtures/simple_json_file_1.json')
    second_file_data = load_data('tests/fixtures/simple_json_file_2.json')
    assert generate_diff(first_file_data, second_file_data) == correct_diff
    print("simple json test passed")
    first_file_data = load_data('tests/fixtures/simple_yml_file_1.yml')
    second_file_data = load_data('tests/fixtures/simple_yml_file_2.yml')
    assert generate_diff(first_file_data, second_file_data) == correct_diff
    print("simple yml test passed")


if __name__ == '__main__.py':
    test()
