
all:
	cd finally && python finally.py

windows: clean-windows all

clean-windows:
	del /s /q *.pyc
	rmdir /s /q "finally/exports"