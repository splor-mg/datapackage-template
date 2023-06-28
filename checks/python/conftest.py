import pytest
from frictionless import Package
import duckdb

@pytest.fixture(scope='session')
def package():
    result = Package('datapackage.yaml')
    return result

@pytest.fixture(scope='session')
def db(package):
    conn = duckdb.connect(database=':memory:', read_only=False)
    for resource in package.resource_names:
        _sql = f"""
        CREATE TABLE '{resource}' AS 
        SELECT * FROM read_csv_auto('build/{resource}.csv')
        """
        conn.execute(_sql)
    
    yield conn
    conn.close()
