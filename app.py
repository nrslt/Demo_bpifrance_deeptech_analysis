import json
import joblib
# to launch api server:
# python app.py
from flask import Flask
from flask import request
from bpideep.getpatent import Patent
from bpideep.getdata import company_search, bulk_search, company_search_fuzzy
from bpideep.feateng import funding_amounts_employees, get_stage_age_ratio
import pandas as pd
import os

data_path = os.path.join(os.path.dirname(__file__), "bpideep/data")
DATA = pd.read_json(f"{data_path}/DEMO_data.json")

app = Flask(__name__)

@app.route('/')
def index():
     return 'OK'

@app.route('/predict', methods=['GET'])
def predict():
    name = request.args['name']

    # based on company name input, selects corresponding row in DATA
    X = DATA[DATA['name']==name]
    try:
        img = X['images'][0]['100x100']
    except:
        img = 'No image available'

    if isinstance(X,dict):
        return {"predictions": 'Problem with the Api key'}

    if X.empty:
        return {"predictions": 'Company name not found on DealRoom'}

    X_time = pd.DataFrame(funding_amounts_employees(X), columns = ['funding_employees_ratio'])
    X_time['stage_age_ratio'] = get_stage_age_ratio(X)

    X_lab = X.copy()

    # importing models
    pipeline = joblib.load('bpideepmodel.joblib')
    model_time = joblib.load('bpideepmodel_time.joblib')
    model_lab = joblib.load('bpideepmodel_lab.joblib')
    # model_techno = joblib.load('modeltechno.joblib')

    # storing models results
    results = pipeline.predict(X)

    # storing X preprocessed
    X_preproc_array = pipeline.named_steps['featureencoder'].transform(X)
    feat_list = pipeline.named_steps['featureencoder'].features_list
    X_preproc = pd.DataFrame(X_preproc_array, columns = feat_list).fillna(0)

    result_proba = pipeline.predict_proba(X)
    time_result = model_time.predict_proba(X_time)
    lab_result = model_lab.predict_proba(X_lab)
    # techno_proba = model_techno.predictproba(Xtechno)

    # getting company description
    try:
        company_description = X['about'][0]
    except:
        company_description = 'No description available'

    # getting company tags
    try:
        company_tags = X['tags'][0]
    except:
        company_tags = 'No tags available'

    return {
            "prediction": str(results[0]),
            "prediction_proba": str(result_proba[0][1]),
            "time_predict": str(time_result[0][1]),
            "lab_predict": str(lab_result[0][1]),
            "X_preproc": X_preproc.to_dict(),
            "image": img,
            "description": company_description,
            'tags': company_tags
            }

@app.route('/search', methods=['GET'])
def search():
    # get year and month from streamlit
    year = request.args['year']
    month = request.args['month']

    # return a df with name and funding_amount  for 10 highest fundings
    df = bulk_search(month, year)
    df = df[df.launch_year > 2010]
    df['amount'] = df.fundings.apply(lambda x : x['items'][0]['amount'])
    df = df.sort_values('amount', ascending=False).head(10)
    df = df[['name', 'amount']]


    # for every name in df predict deeptech or not deeptech
    results_dic = {'name' : [], 'amount':[],'prediction':[]}

    for i in df.index:
        name = df.loc[i,'name']
        amount = df.loc[i,'amount']

        patent = Patent()
        nb_patents = patent.get_nb_patents(name)
        X = company_search(name)
        if X.empty:
            X = company_search_fuzzy(name)
        X['nb_patents'] = nb_patents
        pipeline = joblib.load('bpideepmodel.joblib')
        results = pipeline.predict(X)

        results_dic['name'].append(str(name))
        results_dic['amount'].append(str(amount))
        results_dic['prediction'].append(str(results[0]))

    return results_dic


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
