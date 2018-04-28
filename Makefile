
all:
	cd finally && python finally.py

clean-windows:
	del /s /q *.pyc
	rmdir /s /q "finally/exports"