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

# reading demo data
data_path = os.path.join(os.path.dirname(__file__), "bpideep/data")
DATA = pd.read_json(f"{data_path}/DEMO_data.json")

MAY_2019 = pd.read_csv(f"{data_path}/DEMO_may_2019.csv", index_col = 0)
MAY_2020 = pd.read_csv(f"{data_path}/DEMO_may_2020.csv", index_col = 0)
SEP_2019 = pd.read_csv(f"{data_path}/DEMO_september_2019.csv", index_col = 0)
SEP_2020 = pd.read_csv(f"{data_path}/DEMO_september_2020.csv", index_col = 0)

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
        img = X['images'].iloc[0]['100x100']
    except:
        img = 'No image currently available'

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
        company_description = X['about'].iloc[0]
    except:
        company_description = 'No description available'

    # getting company tags
    try:
        company_tags = X['tags'].iloc[0]
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

    search_data = {
            'MAY_2019': MAY_2019,
            'MAY_2020': MAY_2020,
            'SEP_2019': SEP_2019,
            'SEP_2020': SEP_2020
    }

    search_df = search_data[f'{month}_{year}']

    search_dict = {
        'amount': search_df['amount'].tolist(),
        'name': search_df['name'].tolist(),
        'prediction': search_df['prediction'].tolist()
    }

    return search_dict


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
