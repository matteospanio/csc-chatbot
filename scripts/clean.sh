# clean build files
rm -fr build/
rm -fr dist/
rm -fr .eggs/
find . -name '*.egg-info' -exec rm -fr {} +
find . -name '*.egg' -exec rm -fr {} +

# clean python file artifacts
find . -name '*.pyc' -exec rm -f {} +
find . -name '*.pyo' -exec rm -f {} +
find . -name '*~' -exec rm -f {} +
find . -name '__pycache__' -exec rm -fr {} +

# clean test and coverage artifacts
rm -fr .tox/
rm -f .coverage
rm -fr htmlcov/
rm -rf .hypothesis
rm -fr .pytest_cache
rm -fr .mypy_cache