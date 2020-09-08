import requests
import pandas as pd
import os
import json
from dotenv import load_dotenv
load_dotenv()

class CompaniesFilter():  #Class to get an overview of the filters usable in the API with form_data parameter


    def __init__(self):
        self.filters = ['company_type',
                        'client_focus',
                         'revenues',
                         'fundings',
                         'industries',
                         'sub_industries',
                         'achievements',
                         'tags',
                         'hq_locations',
                         'tg_locations',
                         'delivery_methods',
                         'growth_stages',
                         'company_status',
                         'employees',
                         'payments',
                         'technologies',
                         'income_streams',
                         'has_website_url',
                         'last_round_year',
                         'last_round_month',
                         'launch_year',
                         'total_funding_min',
                         'total_funding_max']   #empty filters : 'last_updated','last_updated_utc', 'launch_year_min','launch_year_max'


    def get_categories(self, filt):
        ''' functions that return all the categories of a given filter'''
        path = os.path.join(os.path.dirname(__file__), 'data/companies_filters.txt')
        with open(path, 'r') as f:
            r_json = json.load(f)
            r_json = r_json['items']

        categories = []
        for dic in r_json:
            if dic['key'] == filt:
                for d in dic['items']:
                    categories.append(d['name'])
                return categories
        print('filter not found')


    # def get_filters(self):
    #     '''Method to get the list of filters '''
    #     URL = 'https://api.dealroom.co/api/v1/companies/filters'

    #     env_path = os.path.join(os.path.dirname(__file__), ".env")
    #     load_dotenv(dotenv_path = env_path)
    #     APIKEY = os.getenv('DEALROOMAPIKEY')

    #     r = requests.post(URL ,auth=(APIKEY,'')).json()

    #     path = os.path.join(os.path.dirname(__file__), 'data/companies_filters.txt')

    #     with open(path, 'w') as outfile:
    #         json.dump(r, outfile)







