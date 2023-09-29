build:
	python -m build

install-dev:
	python -m pip install -e .

uninstall:
	python -m pip uninstall -y gage

clean:
	rm -rf dist build

build-dist:
	pyinstaller gage.py
