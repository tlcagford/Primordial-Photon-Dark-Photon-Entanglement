.PHONY: all clean figures data

all: figures data

figures:
	python src/main.py

clean:
	rm -rf figures/*.pdf data/*.txt

test:
	python -m pytest tests/ -v