import json
import joblib
# to launch api server:
# python app.py
from flask import Flask
from flask import request
from bpideep.getpatent import Patent
from bpideep.getdata import company_search
from bpideep.feateng import feat_eng_new_entry

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
        return 'Problem with the Api key'

    if X.empty:
        return 'Company name not found on DealRoom'


    X['nb_patents'] = nb_patents
    X = feat_eng_new_entry(X)
    print(f'X TYPE :  {type(X)}')
    print(f'ICCCCCCCI XXXXXX :  {X.iloc[1,-3:]}')
    print(f'ICCCCCCCI XXXXXX :  {nb_patents}')
    print(f'ICCCCCCCI XXXXXX :  {X['nb_patents']}')

    pipeline = joblib.load('bpideepmodel.joblib')
    results = pipeline.predict(X)
    return {"predictions": str(results[0])}



# if __name__ == '__main__':
#     import ipdb;

#     ipdb.set_trace()
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
