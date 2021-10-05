.PHONY: make_env requirements scraper_local_run file_maker_local_run unit_test clean fix_code push_develop lint

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROFILE = default
PROJECT_NAME = notion-code-legacy
VENV_NAME = .venv
PYTHON_INTERPRETER = $(PROJECT_DIR)/$(VENV_NAME)/bin/python3
SRC_DIR = src
ENTRYPOINT_FILE = $(SRC_DIR)/app.py

## Create virtual environment
make_env:
	$(shell if [ ! -d ".venv" ]; then python3 -m venv $(VENV_NAME); fi)

## Install Python Dependencies
requirements: make_env
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

run_app: requirements
	$(PYTHON_INTERPRETER) $(ENTRYPOINT_FILE)

## Run unit tests
unit_test: requirements
	$(PYTHON_INTERPRETER) -m pytest

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Sort imports with isort & import code with Black
fix_code: clean
ifeq (,$(shell git diff --cached --exit-code))
	@echo "----- Isort -----"
	$(PYTHON_INTERPRETER) -m isort $(SRC_DIR)
	@echo "----- Black -----"
	$(PYTHON_INTERPRETER) -m black $(SRC_DIR)
	git add *
	git commit -m "black & isort clean"
else
	@echo "Files are stagged and ready to be commited. Commit them before updating requirements"
	exit 1
endif

## Update requirements and push commited changes
push_develop: fix_code
ifeq (,$(shell git diff --cached --exit-code))
	$(PYTHON_INTERPRETER) -m pip freeze > requirements.txt
	git add requirements.txt
	git commit -m "update requirements"
	git push origin develop
else
	@echo "Files are stagged and ready to be commited. Commit them before updating requirements"
	exit 1
endif

## Lint using flake8 & mypy
lint:
	@echo "----- Mypy -----"
	$(PYTHON_INTERPRETER) -m mypy $(SRC_DIR)
	@echo "----- flake8 -----"
	$(PYTHON_INTERPRETER) -m flake8 $(SRC_DIR)


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
