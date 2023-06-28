.PHONY: all transform check build

EXT = txt
OUTPUT_DIR = build
RESOURCE_NAMES := $(shell yq e '.resources[].name' datapackage.yaml)
BUILD_FILES := $(addsuffix .csv,$(addprefix build/,$(RESOURCE_NAMES)))

all: transform check build

transform: $(BUILD_FILES)

$(BUILD_FILES): $(OUTPUT_DIR)/%.csv: data/%.$(EXT) schemas/%.yaml scripts/transform.py datapackage.yaml
	python scripts/transform.py $* $@

check: checks-python checks-rstats

checks-python:
	python -m pytest checks/python/

checks-rstats:
	Rscript checks/rstats/testthat.R

build:
	python scripts/build.py datapackage.json $(OUTPUT_DIR)
