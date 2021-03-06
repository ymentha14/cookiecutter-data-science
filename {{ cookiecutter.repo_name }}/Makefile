.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = {{ cookiecutter.s3_bucket }}
PROFILE = {{ cookiecutter.aws_profile }}
PROJECT_NAME = {{ cookiecutter.repo_name }}
PYTHON_INTERPRETER = {{ cookiecutter.python_interpreter }}


############## Virtual Env ##############

# Create pypi virtual env
create_env:
	@echo ">>> Create environment...\n"
	@$(PYTHON_INTERPRETER) -m venv env
	@echo ">>> Environment successfully created!\n"

## Install Python Dependencies for development
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel ipykernel
	$(PYTHON_INTERPRETER) -m pip install -r requirements_dev.txt
	$(PYTHON_INTERPRETER) -m ipykernel install --user --name=$(PROJECT_NAME)_env

## Install Python Dependencies for production
requirements_prod:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Install jupyter lab extensions
jupy_install:
	./.install_scripts/jupy_extensions.sh



#################################################################################
# Docker
#################################################################################

# build the explorer image
docker_build:
	@docker build -t $(PROJECT_NAME)

# We mount as volume precisely those files that are copied in the dockerfile for development purpose
run_container_dev:
	@docker run -it \
	-e USER=$USER \
	-e REPO_DIR=/app \
	-v `pwd`/data:/app/data \
	-v `pwd`/Makefile:/app/Makefile \
	-v `pwd`/requirements.txt:/app/requirements.txt \
	-v `pwd`/src:/app/src \
	-v `pwd`/scripts:/app/scripts \
	-v notebooks:/app/notebooks \
	-p 8080:8501 \
	$(PROJECT_NAME) \
	/bin/bash


run_container:
	@docker run \
	-v `pwd`/data:/app/data \
	-p 8080:8501 \
	-d \
	--rm \
	$(PROJECT_NAME)



run_container:
	@docker run -it \
	-e USER=$USER \
	-e REPO_DIR=/app \
	-w /app \
	-v `pwd`/data:/app/data \
	-v `pwd`/src:/app/src \
	-v `pwd`/notebooks:/app/notebooks \
	-p 8080:8080 \
	$(PROJECT_NAME)

# start a container of the image
#-w workdir in container
docker_run: check_config
	@docker run --rm \
	-p 8123:5000  \
	--env-file ~/.dj/config \
    -v src:/app/src \
    -w /app \
	-v <local_volume_dir>:<container_volume_dir> \
	--user nobody \
	-it \
	--entrypoint python3 <image_name> <path_2_script>

# start a interactive shell in the image
docker_shell:
	@docker run --rm \
	-p 8123:5000  \
	--env-file ~/.dj/config \
	-w /app \
	-it /bin/bash


#################################################################################
# Data
#################################################################################

## Make Dataset
data: requirements
	$(PYTHON_INTERPRETER) src/data/make_dataset.py data/raw data/processed

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src

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
