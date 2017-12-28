.PHONY: clean-pyc

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	name '*~' -exec rm --force  {}

clean-tex:
	rm *.tex

test:
	python3 src/main.py sample/test01.hy
	python3 src/main.py sample/test02.hy
