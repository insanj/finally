
all:
	python finally/finally_open_web_browser.py "http://127.0.0.1:5000"
	cd finally && set FLASK_APP=finally_flask.py && flask run

import:
	cd finally && python finally.py

deps:
	pip install -U Flask
	pip install -U xmltodict

clean-windows:
	del /s /q *.pyc
	rmdir /s /q "finally/exports"

