.PHONY: all transform check load

RESOURCE_NAMES := $(shell yq e '.resources[].name' datapackage.yaml)
DATA_FILES := $(addsuffix .csv,$(addprefix data/,$(RESOURCE_NAMES)))

all: transform check load

transform: $(DATA_FILES)

$(DATA_FILES): data/%.csv: data/raw/%.txt schemas/%.yaml scripts/transform.py datapackage.yaml
	python scripts/transform.py $*

check: checks-python

checks-python:
	python -m pytest checks/python/

load: 
	find build -type f | xargs rm
	python scripts/load.py
