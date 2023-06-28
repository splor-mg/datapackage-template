import pytest
import pandas as pd
import petl as etl
from deepdiff import DeepDiff

def test_with_pandas(db):
    expected = pd.DataFrame({'vl_emp': [3121.0]})
    
    _sql = """
           SELECT sum(vl_emp) as vl_emp 
           FROM fact
           """
    result = db.execute(_sql).fetchdf()

    # expected.compare(result)
    assert expected.equals(result)

def test_with_petl(db):
    expected = [{'value': 3121.0}]
    
    _sql = """
        SELECT sum(vl_emp) as vl_emp 
        FROM fact
        """
    result = list((
        etl
        .fromdb(db, _sql)
        .aggregate(None, sum, 'vl_emp')
        .dicts()
    ))
    diff = DeepDiff(result, expected, verbose_level=2)
    
    if diff:
        pytest.fail(diff.pretty())
