SHELL := /bin/bash

publish: header
	pip3 install build twine
	rm -rf dist/*
	python3 -m build
	twine upload dist/*

header:
	clang -E ../../c/uwapi-c/uwapi/bots.h ../../c/uwapi-c/uwapi/common.h > uw/bots.h