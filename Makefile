# Variables
PYTHON = python3.11
SRC_DIR = eyespy
MAIN_SCRIPT = ./main.py


.PHONY: docker-build

ifndef VERSION
  VERSION := latest  # Or some other suitable default
else
  VERSION := v$(VERSION)
endif

docker-build: # Run docker build
	docker build -t registry.walld.me/wdietrich/eyespy:$(VERSION) .

.PHONY: run
run: # Run docker push
	$(PYTHON) $(MAIN_SCRIPT)


.PHONY: lint
lint: $(SRC_FILES) # Linting with flake8 (make sure flake8 is installed: pip install flake8)
	$(PYTHON) -m flake8 $(SRC_DIR)

.PHONY: format
format: # Formatting with black (make sure black is installed: pip install black)
	$(PYTHON) -m black $(SRC_DIR)


.PHONY: check-format
check-format: # Check formatting with black, but don't modify files.  Useful for CI.
	$(PYTHON) -m black --check $(SRC_DIR)


.PHONY: clean
clean: # Clean up generated files (e.g., .pyc files)
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*~" -delete # Remove backup files
	find . -name ".pytest_cache" -type d -exec rm -rf {} + # Remove pytest cache
	find . -name ".mypy_cache" -type d -exec rm -rf {} +  #remove mypy cache
