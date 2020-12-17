from gendiff.gendiff import generate_diff
from gendiff.data_loader import load_data
from gendiff.gendiff import main, stylish


def test_simple_files():
    correct_diff = open('tests/fixtures/correct_diff_for_simple_files.txt').read()
    first_file_data = load_data('tests/fixtures/simple_json_file_1.json')
    second_file_data = load_data('tests/fixtures/simple_json_file_2.json')
    data = generate_diff(first_file_data, second_file_data)
    print(data)
    assert stylish(data) == correct_diff
    print("simple json test passed")
    first_file_data = load_data('tests/fixtures/simple_yml_file_1.yml')
    second_file_data = load_data('tests/fixtures/simple_yml_file_2.yml')
    data = generate_diff(first_file_data, second_file_data)
    assert stylish(data) == correct_diff
    print("simple yml test passed")


def test_complicated_files():
    first_file_data = load_data('tests/fixtures/complicated_json_file_1.json')
    second_file_data = load_data('tests/fixtures/complicated_json_file_2.json')
    data = generate_diff(first_file_data, second_file_data)
    with open('tests/fixtures/correct_diff_for_complicated_files.txt', 'r') as correct_diff_for_complicated_files:
        assert stylish(data) == correct_diff_for_complicated_files.read()
