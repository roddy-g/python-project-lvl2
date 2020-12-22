from gendiff.generate_diff import generate_diff
from gendiff.data_loader import load_data
from gendiff.stylish_detailed import stylish_tree
from gendiff.stylish_plain import stylish_plain


def test_simple_files():
    first_file_data = load_data('tests/fixtures/simple_json_file_1.json')
    second_file_data = load_data('tests/fixtures/simple_json_file_2.json')
    diff = generate_diff(first_file_data, second_file_data, stylish_tree)
    with open('tests/fixtures/correct_diff_for_simple_files.txt', 'r') as correct_diff:
        assert diff == correct_diff.read()


def test_simple_yml_files():
    first_file_data = load_data('tests/fixtures/simple_yml_file_1.yml')
    second_file_data = load_data('tests/fixtures/simple_yml_file_2.yml')
    diff = generate_diff(first_file_data, second_file_data, stylish_tree)
    with open('tests/fixtures/correct_diff_for_simple_files.txt', 'r') as correct_diff:
        assert diff == correct_diff.read()


def test_complicated_yml_files():
    first_file_data = load_data('tests/fixtures/complicated_yml_file_1.yml')
    second_file_data = load_data('tests/fixtures/complicated_yml_file_2.yml')
    diff = generate_diff(first_file_data, second_file_data, stylish_tree)
    with open('tests/fixtures/correct_diff_for_complicated_files.txt', 'r') as correct_diff:
        assert diff == correct_diff.read()


def test_complicated_json_files():
    first_file_data = load_data('tests/fixtures/complicated_json_file_1.json')
    second_file_data = load_data('tests/fixtures/complicated_json_file_2.json')
    diff = generate_diff(first_file_data, second_file_data, stylish_tree)
    with open('tests/fixtures/correct_diff_for_complicated_files.txt', 'r') as correct_diff:
        assert diff == correct_diff.read()


def test_complicated_files_plain_style():
    first_file_data = load_data('tests/fixtures/complicated_json_file_1.json')
    second_file_data = load_data('tests/fixtures/complicated_json_file_2.json')
    diff = generate_diff(first_file_data, second_file_data, stylish_plain)
    with open('tests/fixtures/correct_plain_diff_for_complicated_files.txt', 'r') as correct_diff:
        assert diff == correct_diff.read()

