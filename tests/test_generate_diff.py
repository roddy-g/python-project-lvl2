from gendiff.gendiff import generate_diff
from gendiff.data_loader import load_data
from gendiff.gendiff import stylish_tree


def test_simple_files():
    first_file_data = load_data('tests/fixtures/simple_json_file_1.json')
    second_file_data = load_data('tests/fixtures/simple_json_file_2.json')
    data = generate_diff(first_file_data, second_file_data)
    with open('tests/fixtures/correct_diff_for_simple_files.txt', 'r') as correct_diff:
        assert stylish_tree(data) == correct_diff.read()


def test_simple_yml_files():
    first_file_data = load_data('tests/fixtures/simple_yml_file_1.yml')
    second_file_data = load_data('tests/fixtures/simple_yml_file_2.yml')
    data = generate_diff(first_file_data, second_file_data)
    with open('tests/fixtures/correct_diff_for_simple_files.txt', 'r') as correct_diff:
        assert stylish_tree(data) == correct_diff.read()


def test_complicated_yml_files():
    first_file_data = load_data('tests/fixtures/complicated_yml_file_1.yml')
    second_file_data = load_data('tests/fixtures/complicated_yml_file_2.yml')
    data = generate_diff(first_file_data, second_file_data)
    with open('tests/fixtures/correct_diff_for_complicated_files.txt', 'r') as correct_diff:
        assert stylish_tree(data) == correct_diff.read()


def test_complicated_json_files():
    first_file_data = load_data('tests/fixtures/complicated_json_file_1.json')
    second_file_data = load_data('tests/fixtures/complicated_json_file_2.json')
    data = generate_diff(first_file_data, second_file_data)
    with open('tests/fixtures/correct_diff_for_complicated_files.txt', 'r') as correct_diff:
        assert stylish_tree(data) == correct_diff.read()
