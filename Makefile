.PHONY: all transform check load

RESOURCE_NAMES := $(shell yq e '.resources[].name' datapackage.yaml)
BUILD_FILES := $(addsuffix .csv,$(addprefix build/,$(RESOURCE_NAMES)))

all: transform check load

transform: $(BUILD_FILES)

$(BUILD_FILES): build/%.csv: data/%.txt schemas/%.yaml scripts/transform.py datapackage.yaml
	python scripts/transform.py $* $@

check: checks-python checks-rstats

checks-python:
	python -m pytest checks/python/

checks-rstats:
	Rscript checks/rstats/testthat.R

load: 
	find build -type f | xargs rm
	python scripts/load.py
