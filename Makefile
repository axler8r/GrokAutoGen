# global settings
SHELL = /usr/bin/env zsh

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
.PHONY: all                                                          \
		clean clean-resources clean-logs clean-output clean-runfiles \
		check format spell                                           \
		test test-verbose                                            \
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
	@echo "Cleaning $(OUT_DIR)..."
	@if [ -d "$(OUT_DIR)" ]; then 						\
		echo "Cleaning $(OUT_DIR) directory..."; 		\
		rm -rf $(OUT_DIR)/*; 							\
	else 												\
		echo "$(OUT_DIR) directory does not exist."; 	\
	fi

clean-logs:
	@echo "Cleaning $(LOG_DIR)..."
	@if [ -d "$(LOG_DIR)" ]; then 						\
		echo "Cleaning $(LOG_DIR) directory..."; 		\
		rm -rf $(LOG_DIR)/*; 							\
	else 												\
		echo "$(LOG_DIR) directory does not exist."; 	\
	fi

clean-resources:
	@echo "Cleaning $(RES_DIR)..."
	@if [ -d "$(RES_DIR)" ]; then 						\
		echo "Cleaning $(RES_DIR) directory..."; 		\
		rm -rf $(RES_DIR)/*; 							\
	else 												\
		echo "$(RES_DIR) directory does not exist."; 	\
	fi
	rm -f $(RES_DIR)/*

clean: clean-runfiles clean-output clean-logs clean-resources

format:
	@echo "Formatting $(PROJECT_NAME)..."
	ruff format

check:
	@echo "Checking $(PROJECT_NAME)..."
	ruff check

test:
	@echo "Testing $(TST_DIR)..."
	$(PYTHON) -m pytest $(TST_DIR)

test-verbose:
	@echo "Testing $(TST_DIR)..."
	$(PYTHON) -m pytest --verbose $(TST_DIR)

changelog:
	@echo "Generating $(PROJECT_NAME)'s latest changelog..."
	git cliff --bump --config .cliff.toml --unreleased

spell:
	@echo "Checking spelling..."
	foreach file in **/*.md; do if [[ -f "$$file" ]]; then aspell --lang=en_GB check "$$file"; fi; done
	foreach file in **/*.py; do if [[ -f "$$file" ]]; then aspell --lang=en_GB check "$$file"; fi; done

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  all:             Format, check, and test the project"
	@echo "  init:            Initialize the project"
	@echo "  activate:        Activate poetry shell"
	@echo "  deactivate:      Deactivate the existing poetry shell"
	@echo "  clean:           Clean all generated files"
	@echo "  clean-resources: Clean resource files"
	@echo "  clean-logs:      Clean log files"
	@echo "  clean-output:    Clean output files"
	@echo "  clean-runfiles:  Clean run files"
	@echo "  format:          Format the project"
	@echo "  check:           Check implementation"
	@echo "  test:            Test the project"
	@echo "  test-verbose:    Test the project with verbose output"
	@echo "  changelog:       Update the changelog"
	@echo "  help:            Show this help message"
