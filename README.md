# lt-technical-showcase
jsonplaceholder.typicode album explorer

## Environment Expectations
This code was written on Linux with Python 3.9, but should work crossplatform with a variety of Python3 versions.

[Creating a virtual environment is recommended.](https://docs.python.org/3/library/venv.html)

To install dependencies, run:
`pip install -r requirements.txt -r requirements-dev.txt`

## Usage
To run tests, run:
`python -m unittest`

To lint, run:
`pylint app && flake8 --ignore=E501,W504 app`

To run the application, run:
`python -m app --help`
