.PHONY: all extract transform check build publish

EXT = txt
INPUT_DIR = data-raw
OUTPUT_DIR = data
RESOURCE_NAMES := $(shell yq e '.resources[].name' datapackage.yaml)
OUTPUT_FILES := $(addsuffix .csv,$(addprefix $(OUTPUT_DIR)/,$(RESOURCE_NAMES)))

all: transform check build

transform: $(OUTPUT_FILES)

$(OUTPUT_FILES): $(OUTPUT_DIR)/%.csv: $(INPUT_DIR)/%.$(EXT) schemas/%.yaml scripts/transform.py datapackage.yaml
	python scripts/transform.py $* $@

check: checks-python checks-rstats

checks-python:
	python -m pytest checks/python/

checks-rstats:
	Rscript checks/rstats/testthat.R

build:
	python scripts/build.py $(OUTPUT_DIR)

print: 
	@echo $(OUTPUT_FILES)