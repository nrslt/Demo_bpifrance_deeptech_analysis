# here we create:
    # - API calls functions (possibly several depending on needs)
    # - each function returns a df

import pandas as pd
import requests
from dotenv import load_dotenv, find_dotenv

import os



def getbatchdata(company_id_list, fields):
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path = env_path)
    APIKEY = os.getenv('DEALROOMAPIKEY')
    URL = 'https://api.dealroom.co/api/v1'

    response = requests.get(
                        url = f"{URL}/companies/batch?ids={company_id_list}&fields={fields}",\
                        auth = (APIKEY, '')

                        )
    data = response.json()['items']
    return pd.DataFrame(data)

# def getfulldata():
#     for i in np.arange(0, len(id_deeptech), 50):
#     if i <= 400:
#         (id_deeptech[i:i+50])
#     if i == 450:
#         print(id_deeptech[450:len(id_deeptech)])
#         print(len(id_deeptech[450:len(id_deeptech)]))

# for loop in order to iterate by batch on the csv file

def bulk_search(**kwargs):
    '''Bulk search is for searching multiple company by keywords in the name or the website'''

    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path = env_path)
    APIKEY = os.getenv('DEALROOMAPIKEY')
    URL = 'https://api.dealroom.co/api/v1/companies/bulk'

    response = requests.post(
                        url = URL,\
                        auth = (APIKEY, ''),\
                        data = kwargs)

    data = response.json()['items']
    return pd.DataFrame(data)

