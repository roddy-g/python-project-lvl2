from gendiff import generate_diff
import json


def test(file_1='tests/fixtures/simple_json_file_1.json',
         file_2='tests/fixtures/simple_json_file_2.json',
         diff='tests/fixtures/diff_file_1_file_2.txt'):
    first_file = json.load(open(file_1))
    second_file = json.load(open(file_2))
    different_true_1 = open(diff).read()
    diffrenet_by_func = generate_diff.find_diffs(first_file, second_file)
    assert diffrenet_by_func == different_true_1
    print("test_passed")

if __name__ == '__main__.py':
    test()
