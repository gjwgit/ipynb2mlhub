test:
	python3 ipynb2mlhub.py >| demo.py
	python3 demo.py

convert:
	python3 ipynb2mlhub.py >| demo.py
	cat demo.py
