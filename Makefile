VENV=. venv/bin/activate

all: venv/touchfile run

venv/touchfile: requirements.txt
	test -d venv || virtualenv venv
	$(VENV); pip install -Ur requirements.txt
	touch venv/touchfile

run: venv/touchfile
	$(VENV); PYTHONPATH=. fava example/sample.bc

clean:
	rm -rf venv
	find -iname "*.pyc" -delete
