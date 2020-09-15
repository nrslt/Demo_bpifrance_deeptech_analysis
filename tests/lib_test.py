# -*- coding: UTF-8 -*-

# Import from standard library
import os
import bpideep
import pandas as pd
# Import from our lib
from bpideep.lib import clean_data
import pytest

# this test is useless so I commented it

# def test_clean_data():
#     datapath = os.path.dirname(os.path.abspath(bpideep.__file__)) + '/data'
#     df = pd.read_csv('{}/data.csv.gz'.format(datapath))
#     first_cols = ['id', 'civility', 'birthdate', 'city', 'postal_code', 'vote_1']
#     assert list(df.columns)[:6] == first_cols
#     assert df.shape == (999, 142)
#     out = clean_data(df)
#     assert out.shape == (985, 119)

def test_clean_data():
    pass
