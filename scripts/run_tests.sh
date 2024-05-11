echo "Run pytest suite"
pytest
coverage erase
echo "Run doctest suite"
cd docs && make doctest
