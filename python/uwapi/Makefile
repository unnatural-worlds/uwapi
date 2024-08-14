SHELL := /bin/bash

publish: header
	pip3 install build twine
	rm -rf dist/*
	python3 -m build
	twine upload dist/* --verbose

header:
	clang -Iheaders -E ../../c/uwapi/uwapi/bots.h > uw/bots.h

version:
	@grep UW_VERSION ../../c/uwapi/uwapi/bots.h
