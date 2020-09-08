# here we create:
    # - API calls functions (possibly several depending on needs)
    # - each function returns a df

import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv, find_dotenv

import os

FIELDS = 'id,name,path,tagline,about,url,website_url,twitter_url,facebook_url,linkedin_url,google_url,crunchbase_url,angellist_url,playmarket_app_id,appstore_app_id,images,employees,employees_latest,industries,sub_industries,corporate_industries,service_industries,technologies,income_streams,growth_stage,traffic_summary,hq_locations,tg_locations,client_focus,revenues,tags,ownerships,payments,achievements,delivery_method,launch_year,launch_month,has_strong_founder,has_super_founder,total_funding,total_funding_source,last_funding,last_funding_source,company_status,last_updated,last_updated_utc,facebook_likes_chart,alexa_rank_chart,twitter_tweets_chart,twitter_followers_chart,twitter_favorites_chart,employees_chart,similarweb_3_months_growth_unique,similarweb_3_months_growth_percentile,similarweb_3_months_growth_relative,similarweb_3_months_growth_delta,similarweb_6_months_growth_unique,similarweb_6_months_growth_percentile,similarweb_6_months_growth_relative,similarweb_6_months_growth_delta,similarweb_12_months_growth_unique,similarweb_12_months_growth_percentile,similarweb_12_months_growth_relative,similarweb_12_months_growth_delta,app_3_months_growth_unique,app_3_months_growth_percentile,app_3_months_growth_relative,app_6_months_growth_unique,app_6_months_growth_percentile,app_6_months_growth_relative,app_12_months_growth_unique,app_12_months_growth_percentile,app_12_months_growth_relative,employee_3_months_growth_unique,employee_3_months_growth_percentile,employee_3_months_growth_relative,employee_3_months_growth_delta,employee_6_months_growth_unique,employee_6_months_growth_percentile,employee_6_months_growth_relative,employee_6_months_growth_delta,employee_12_months_growth_unique,employee_12_months_growth_percentile,employee_12_months_growth_relative,employee_12_months_growth_delta,kpi_summary,team,investors,fundings,traffic,similarweb_chart,job_openings'

# reading the id_deeptech.csv file and storing it as a python list
def deeptech_tolist(csv):
    """takes the csv name of deeptech id list and returns the flatten python list"""

    # stores the csv path inside csv_path
    # csv_path = os.path.join(os.path.dirname(__file__), "data/", csv)
    deeptech = pd.read_csv(f"data/{csv}")
    # stores the list of list of companies id inside deeptech
    deeptech = deeptech.values.astype(str).tolist()

    # flattens the list of list and stores it as a simple python list
    deeptech_list = [item for sublist in deeptech for item in sublist]
    return deeptech_list


def getbatchdata(company_id_list, fields = FIELDS):
    """takes a company_id_list and a fields parameter, \
    which is a list of fields for the Dealroom API

    returns a pandas dataframe with each row corresponding to a company \
    and the columns corresponding to the fields list"""

    # stores env_path for api key in .env file
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path = env_path)
    APIKEY = os.getenv('DEALROOMAPIKEY')
    URL = 'https://api.dealroom.co/api/v1'

    # converts the company_id_list to a string of company ids separated by commas
    companies_string = ",".join(company_id_list)

    # performs get request on dealroom api
    response = requests.get(
                        url = f"{URL}/companies/batch?ids={companies_string}&fields={fields}",\
                        auth = (APIKEY, '')
                        )

    data = response.json()['items']
    return pd.DataFrame(data)

def getfulldata(csv):
    """the only parameter needed is the deeptech.csv name of the companies id csv \
    the function calls deeptech_tolist to the csv file in order to retrieve the entire python list of companies id \
    then the function calls getbatchdata on each 50id batches from id_deeptech list"""

    # storing the id_deeptech companies id list
    id_deeptech = deeptech_tolist(csv)

    # instantiating data with the first 50 companies from id_deeptech
    first_batch = id_deeptech[0:50]
    data = getbatchdata(first_batch)

    for i in np.arange(50, len(id_deeptech), 50):
        if i <= 400:
            i_batch = id_deeptech[i:i+50]
            data_i = getbatchdata(i_batch)
            data = pd.concat([data, data_i], axis=0)
        elif i == 450:
            i_batch = id_deeptech[450:len(id_deeptech)]
            data_i = getbatchdata(i_batch)
            data = pd.concat([data, data_i], axis=0)

    data.to_csv('deeptech_df.csv')

    return data


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
