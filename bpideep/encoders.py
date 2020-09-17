from bpideep.feateng import feat_eng_cols, feat_eng, get_kept_cols
from sklearn.base import BaseEstimator, TransformerMixin


class FeatEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.features_dict = None


    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = feat_eng(X)
        return X
