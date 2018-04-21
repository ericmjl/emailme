build:
	python setup.py sdist bdist_wheel

release:
	twine upload dist/*