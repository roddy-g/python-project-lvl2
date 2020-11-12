install:
	poetry install
lint:
	poetry run flake8 gendiff
run:
	poetry run gendiff gendiff/tests/fixtures/simple_json_file_1.json gendiff/tests/fixtures/simple_json_file_2.json 
test:
	poetry run tests	
