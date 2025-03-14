# command aliases
PYTHON = python3

# location aliases
PROJECT_NAME = $(shell basename $(CURDIR) | tr '[:upper:]' '[:lower:]')
SRC_DIR = $(PROJECT_NAME)
DOC_DIR = documentation
NBK_DIR = notebook
LOG_DIR = log
OUT_DIR = output
RES_DIR = resource
TST_DIR = test

# phony targets
.PHONY: all                                                              \
		clean-all clean-resources clean-logs clean-output clean-runfiles \
		check check-test                                                 \
		test test-verbose                                                \
		help

# targets
all: format check test

init:
	@echo "Initializing $(PROJECT_NAME)..."
	uv venv
	uv sync
	nbstripout --install --attributes .gitattributes

clean-runfiles:
	rm -rf **/__pycache__
	rm -rf **/.ipynb_checkpoints

clean-output:
	rm -f $(OUT_DIR)/*

clean-logs:
	rm -f $(LOG_DIR)/*

clean-resources:
	rm -f $(RES_DIR)/*

clean-all: clean-runfiles clean-output clean-logs clean-resources

format:
	@echo "Formatting $(PROJECT_NAME)..."
	ruff format

check:
	@echo "Checking $(PROJECT_NAME)..."
	ruff check

check-test:
	@echo "Checking $(PROJECT_NAME)..."
	$(PYTHON) -m mypy $(TST_DIR)

test:
	@echo "Testing $(TST_DIR)..."
	$(PYTHON) -m pytest $(TST_DIR)

test-verbose:
	@echo "Testing $(TST_DIR)..."
	$(PYTHON) -m pytest --verbose $(TST_DIR)

changelog:
	@echo "Generating $(PROJECT_NAME)'s latest changelog..."
	git cliff --bump --config .cliff.toml >> CHANGELOG.md

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  all:             Format, check, and test the project"
	@echo "  init:            Initialize the project"
	@echo "  activate:        Activate poetry shell"
	@echo "  deactivate:      Deactivate the existing poetry shell"
	@echo "  clean-all:       Clean all generated files"
	@echo "  clean-resources: Clean resource files"
	@echo "  clean-logs:      Clean log files"
	@echo "  clean-output:    Clean output files"
	@echo "  clean-runfiles:  Clean run files"
	@echo "  format:          Format the project"
	@echo "  check:           Check implementation"
	@echo "  check-tests:     Check tests"
	@echo "  test:            Test the project"
	@echo "  test-verbose:    Test the project with verbose output"
	@echo "  changelog:       Update the changelog"
	@echo "  help:            Show this help message"
