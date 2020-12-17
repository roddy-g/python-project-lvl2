install:
	poetry install
lint:
	poetry run mypy gendiff
	poetry run flake8 gendiff
run:
	poetry run gendiff tests/fixtures/simple_json_file_1.json tests/fixtures/simple_json_file_2.json
test:
	pytest	
package-install:
	pip install --user /home/rodion/Desktop/python-project-lvl2/dist/hexlet_code-0.3.0-py3-none-any.whl
build:
	poetry build
coverage:
	poetry run pytest --cov=gendiff --cov-report xml


