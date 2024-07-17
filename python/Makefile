SHELL := /bin/bash

publish: header
	pip3 install build twine
	python3 -m build
	twine upload dist/*

header:
	clang -E ../c/uwapi-c/uwapi/bots.h ../c/uwapi-c/uwapi/common.h > uw/bots.h

pypy:
	strip-hints --to-empty main.py -o main.pypy
	pypy main.pypy