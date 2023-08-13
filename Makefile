build:
	python -m build

install-dev:
	python -m pip install -e .

uninstall:
	python -m pip uninstall -y vistaml
