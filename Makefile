.PHONY: all
all: clean readme build upload

.PHONY: build
build:
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf ./bpsrender.egg-info
	rm -rf ./build
	rm -rf ./dist/*

readme:
	pandoc README.md -o README.rst

upload:
	twine upload dist/*

info:
	python3 setup.py egg_info
