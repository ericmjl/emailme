clean:
	rm dist/*

buildwheel:
	python setup.py sdist bdist_wheel

release: clean buildwheel
	twine upload dist/*