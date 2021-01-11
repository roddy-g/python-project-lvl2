from gendiff import generate_diff
import pytest


fixtures_list = [
    (
        'tests/fixtures/simple_json/before.json',
        'tests/fixtures/simple_json/after.json',
        'tests/fixtures/simple_json/correct_diff_stylish.txt',
        ''
    ),
    (
        'tests/fixtures/simple_yml/before.yml',
        'tests/fixtures/simple_yml/after.yml',
        'tests/fixtures/simple_yml/correct_diff_stylish.txt',
        ''
    ),
    (
        'tests/fixtures/complicated_yml/before.yml',
        'tests/fixtures/complicated_yml/after.yml',
        'tests/fixtures/complicated_yml/correct_diff_stylish.txt',
        ''
    ),
(
        'tests/fixtures/complicated_yml/before.yml',
        'tests/fixtures/complicated_yml/after.yml',
        'tests/fixtures/complicated_yml/correct_diff_plain.txt',
        'plain'
    ),
    (
        'tests/fixtures/complicated_json/before.json',
        'tests/fixtures/complicated_json/after.json',
        'tests/fixtures/complicated_json/correct_diff_stylish.txt',
        ''
    ),
    (
        'tests/fixtures/complicated_json/before.json',
        'tests/fixtures/complicated_json/after.json',
        'tests/fixtures/complicated_json/correct_diff_plain.txt',
        'plain'

    )
]


@pytest.mark.parametrize('source,changed_source,correct_diff_path,style',
                         fixtures_list)
def test_generate_diff(source, changed_source, correct_diff_path, style):
    if style:
        diff = generate_diff(source, changed_source, style)
    else:
        diff = generate_diff(source, changed_source)
    with open(correct_diff_path, 'r') as correct_diff:
        assert diff == correct_diff.read()
