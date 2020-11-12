install:
	poetry install
lint:
	poetry run flake8 gendiff
run:
	poetry run gendiff 1.json 2.json 
	
