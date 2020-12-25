from gendiff import generate_diff
import pytest


simple_fixtures_list = [
    (
        'tests/fixtures/simple/json_file_1.json',
        'tests/fixtures/simple/json_file_2.json',
        'tests/fixtures/simple/correct_diff_stylish.txt'
    ),
    (
        'tests/fixtures/simple/yml_file_1.yml',
        'tests/fixtures/simple/yml_file_2.yml',
        'tests/fixtures/simple/correct_diff_stylish.txt'
    )
]
complicated_fixtures_list = [
    (
        'tests/fixtures/complicated/yml_file_1.yml',
        'tests/fixtures/complicated/yml_file_2.yml',
        'tests/fixtures/complicated/correct_diff_stylish.txt',
        ''
    ),
    (
        'tests/fixtures/complicated/json_file_1.json',
        'tests/fixtures/complicated/json_file_2.json',
        'tests/fixtures/complicated/correct_diff_stylish.txt',
        ''
    ),
    (
        'tests/fixtures/complicated/json_file_1.json',
        'tests/fixtures/complicated/json_file_2.json',
        'tests/fixtures/complicated/correct_diff_plain.txt',
        'plain'

    )
]


@pytest.mark.parametrize('source,changed_source,correct_diff_path',
                         simple_fixtures_list)
def test_simple_files(source, changed_source, correct_diff_path):
    diff = generate_diff(source, changed_source)
    with open(correct_diff_path, 'r') as correct_diff:
        assert diff == correct_diff.read()


@pytest.mark.parametrize('source,changed_source,correct_diff_path,style',
                         complicated_fixtures_list)
def test_complicated_files(source, changed_source, correct_diff_path, style)
    if style:
        diff = generate_diff(source, changed_source, style)
    else:
        diff = generate_diff(source, changed_source)
    with open(correct_diff_path, 'r') as correct_diff:
        assert diff == correct_diff.read()
