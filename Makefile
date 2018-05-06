FLASK_APP=finally_flask.py

mac: open-web-browser
	python finally/finally_open_web_browser.py "http://127.0.0.1:5000"
	cd finally && export FLASK_APP=$(FLASK_APP) && flask run

windows: open-web-browser
	cd finally && set FLASK_APP=$(FLASK_APP) && flask run

open-web-browser:
	python finally/finally_open_web_browser.py "http://127.0.0.1:5000"

deps:
	pip install -U Flask
	git submodule sync --recursive
	git submodule update --init --recursive

clean-windows:
	del /s /q *.pyc
	rmdir /s /q "finally/exports"

