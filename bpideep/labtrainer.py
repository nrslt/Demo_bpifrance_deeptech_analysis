from bpideep.getdata import getjson, getfulldata
from bpideep.feateng import zip_code
from bpideep.encoders import FeatEncoder, LabFeatEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import joblib
import os




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

        patent_transformer = make_pipeline(
                                SimpleImputer(missing_values=np.nan, strategy='constant', fill_value = 0),
                                RobustScaler())

        features_transformer = ColumnTransformer(
            [("column_filler", SimpleImputer(missing_values=np.nan, strategy='constant', fill_value = 0), \
                                    ['doctor_yesno', 'department']),
             ("patents_preproc", patent_transformer, ['nb_patents'])], remainder = 'drop')

        pipemodel = Pipeline(steps=[
                            ('featureencoder', LabFeatEncoder()),
                            ('features', features_transformer),
                            ('model', LogisticRegression())]
                            )
        self.pipeline = pipemodel

    def train(self):
        self.set_pipeline()
        self.pipeline.fit(self.X, self.y)


    def save_model(self):
        '''
        Save the model into a .joblib
        '''
        joblib.dump(self.pipeline, 'bpideepmodel_lab.joblib')
        print("bpideepmodel_lab.joblib saved locally")



if __name__ == "__main__":

    # importing data
    company_dict = getjson('deeptech.csv', 'non_deeptech.csv', 'almost_deeptech.csv')
    X, y = getfulldata(company_dict, 'fields_list.txt')

    t = Trainer(X, y)
    t.train()
    t.save_model()
