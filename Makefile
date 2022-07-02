.PHONY: test
test:
	python -m pytest -vv


.PHONY: app
run:
	python main.py
