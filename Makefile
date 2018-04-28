
all:
	python finally/finally_open_web_browser.py "http://localhost:777"
	python -m SimpleHTTPServer 777
	
python:
	cd finally && python finally.py

windows: clean-windows python

clean-windows:
	del /s /q *.pyc
	rmdir /s /q "finally/exports"

