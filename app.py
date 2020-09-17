import json
import joblib
# to launch api server:
# python app.py
from flask import Flask
from flask import request
from bpideep.getpatent import Patent
from bpideep.getdata import company_search
from bpideep.feateng import funding_amounts_employees, get_stage_age_ratio
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
     return 'OK'

@app.route('/predict', methods=['GET'])
def predict():
    name = request.args['name']

    # get nb of patents with Big Query
    patent = Patent()
    nb_patents = patent.get_nb_patents(name)

    # get DealRoom datas
    X = company_search(name)

    if isinstance(X,dict):
        return {"predictions": 'Problem with the Api key'}

    if X.empty:
        return {"predictions": 'Company name not found on DealRoom'}

    X['nb_patents'] = nb_patents
    X_time = pd.DataFrame(funding_amounts_employees(X), columns = ['funding_employees_ratio'])
    X_time['stage_age_ratio'] = get_stage_age_ratio(X)

    # importing models
    pipeline = joblib.load('bpideepmodel.joblib')
    model_time = joblib.load('bpideepmodel_time.joblib')
    # model_lab = joblib.load('modellab.joblib')
    # model_techno = joblib.load('modeltechno.joblib')

    # storing models results
    results = pipeline.predict(X)
    time_result = model_time.predict(X_time)
    # lab_proba = model_lab.predictproba(Xlab)
    # techno_proba = model_techno.predictproba(Xtechno)

    return {
            "predictions": str(results[0]),
            "time_predict": str(time_result[0])
            }

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
