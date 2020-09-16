from bpideep.getdata import getjson, getfulldata
from bpideep.feateng import feat_eng
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import classification_report
import numpy as np
import joblib
import statsmodels.formula.api as smf



class Trainer():
    def __init__(self, X, y):
        '''
        instantiate trainer object with X and y
        '''
        self.pipeline = None
        self.X = X
        self.y = y


    def set_pipeline(self):
        '''
        create the pipeline and logisticregression model
        '''

        ratio_transformer = make_pipeline(
                                SimpleImputer(missing_values=np.nan, strategy='mean'),
                                StandardScaler())

        patent_transformer = make_pipeline(
                                SimpleImputer(missing_values=np.nan, strategy='constant', fill_value = 0),
                                RobustScaler())

        constant_adder = make_pipeline(
                                smf.tools.tools.add_constant(data, prepend=True, has_constant='skip')
                                 )

        features_transformer = ColumnTransformer(
            ["constant_adder" ; constant_adder, x.columns)
            ("feature_encoder"; FeatEncoder(), x.columns),
            ("ratio_preproc", ratio_transformer, ['funding_employees_ratio', 'stage_age_ratio']),
            ("patents_preproc", patent_transformer, ['nb_patents']),
            ], remainder = 'passthrough')


        pipemodel = Pipeline(steps=[
                            ('features', features_transformer),
                            ('model', smf.logit(  ))]
                                         )
        self.pipeline = pipemodel


    def train(self):
        self.set_pipeline()
        self.pipeline.fit(self.X, self.y)


    def save_model(self):
        '''
        Save the model into a .joblib
        '''
        joblib.dump(self.pipeline, 'bpideepmodel_time.joblib')
        print("bpideepmodel.joblib saved locally")



if __name__ == "__main__":

    # importing data
    company_dict = getjson('deeptech.csv', 'non_deeptech.csv', 'almost_deeptech.csv')
    data = getfulldata(company_dict, 'fields_list.txt')

    # supposes that patents is stored as a 'patents.csv' file in /data/

    t = Trainer(data)
    t.train()
    t.save_model()
