from diff_generator.generate_diff import generate_diff
import pytest

base_path = 'tests/fixtures/'
fixtures_list = [
    (
        base_path + 'simple_json/before.json',
        base_path + 'simple_json/after.json',
        base_path + 'simple_json/correct_diff_stylish.txt',
        ''
    ),
    (
        base_path + 'simple_yml/before.yml',
        base_path + 'simple_yml/after.yml',
        base_path + 'simple_yml/correct_diff_stylish.txt',
        ''
    ),
    (
        base_path + 'complicated_yml/before.yml',
        base_path + 'complicated_yml/after.yml',
        base_path + 'complicated_yml/correct_diff_stylish.txt',
        ''
    ),
    (
        base_path + 'complicated_yml/before.yml',
        base_path + 'complicated_yml/after.yml',
        base_path + 'complicated_yml/correct_diff_plain.txt',
        'plain'
    ),
    (
        base_path + 'complicated_json/before.json',
        base_path + 'complicated_json/after.json',
        base_path + 'complicated_json/correct_diff_stylish.txt',
        ''
    ),
    (
        base_path + 'complicated_json/before.json',
        base_path + 'complicated_json/after.json',
        base_path + 'complicated_json/correct_diff_plain.txt',
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
