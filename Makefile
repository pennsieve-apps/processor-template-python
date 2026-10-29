.PHONY: help test run clean

.DEFAULT: help

help:
	@echo "make test   - run the app over sample-input/ with Python (no Docker)"
	@echo "make run    - run it in Docker over sample-input/, writing to data/output/"
	@echo "make clean  - remove data/output/"

test: clean
	INPUT_DIR=sample-input OUTPUT_DIR=data/output python3 -m processor.main
	@cat data/output/results/summary.json

run: clean
	docker compose down --remove-orphans
	docker compose build
	docker compose up --exit-code-from processor

clean:
	rm -rf data/output
