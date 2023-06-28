import pandas as pd

def test_pandas():
    df = pd.read_csv('build/fact.csv')
    assert df['vl_emp'].sum() == 3121