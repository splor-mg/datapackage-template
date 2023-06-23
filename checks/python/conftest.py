import pytest
from frictionless import Package

@pytest.fixture()
def package():
    result = Package('datapackage.yaml')
    return result
