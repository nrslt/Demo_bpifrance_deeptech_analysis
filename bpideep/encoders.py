from bpideep.feateng import feat_eng, zip_code
from sklearn.base import BaseEstimator, TransformerMixin


class FeatEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.features_list = None


    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = feat_eng(X)
        self.features_list = X.columns.tolist()
        return X


class LabFeatEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass


    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = zip_code(X)
        return X
