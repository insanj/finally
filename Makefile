FLASK_APP=finally_flask.py


all:
	python finally/finally_open_web_browser.py "http://127.0.0.1:5000"
	cd finally && set FLASK_APP=$(FLASK_APP) && export FLASK_APP=$(FLASK_APP) && flask run

deps:
	pip install -U Flask
	git submodule sync --recursive
	git submodule update --init --recursive

clean-windows:
	del /s /q *.pyc
	rmdir /s /q "finally/exports"

