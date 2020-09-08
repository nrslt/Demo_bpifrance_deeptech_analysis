import pandas as pd
import os

def get_data():
    path = os.path.join(os.path.dirname(__file__), 'data/deeptech_df.csv')
    df = pd.read_csv(path)
    return df

def clean_data(df):
    col_to_drop = ['about', 'angellist_url', 'app_12_months_growth_percentile', 'app_12_months_growth_relative',
                    'app_12_months_growth_unique', 'app_3_months_growth_percentile', 'app_3_months_growth_relative',
                    'app_3_months_growth_unique', 'app_6_months_growth_percentile', 'app_6_months_growth_relative',
                    'app_6_months_growth_unique', 'appstore_app_id', 'crunchbase_url', 'delivery_method', 'employee_12_months_growth_delta',
                    'employee_12_months_growth_percentile', 'employee_12_months_growth_relative', 'employee_12_months_growth_unique',
                    'employee_3_months_growth_delta', 'employee_3_months_growth_percentile', 'employee_3_months_growth_relative',
                    'employee_3_months_growth_unique', 'employee_6_months_growth_delta', 'employee_6_months_growth_percentile',
                    'employee_6_months_growth_relative', 'employee_6_months_growth_unique', 'facebook_url', 'google_url', 'launch_month',
                    'playmarket_app_id', 'similarweb_12_months_growth_delta', 'similarweb_12_months_growth_percentile',
                    'similarweb_12_months_growth_relative', 'similarweb_12_months_growth_unique', 'similarweb_3_months_growth_delta',
                    'similarweb_3_months_growth_percentile', 'similarweb_3_months_growth_relative', 'similarweb_3_months_growth_unique',
                    'similarweb_6_months_growth_delta', 'similarweb_6_months_growth_percentile', 'similarweb_6_months_growth_relative',
                    'similarweb_6_months_growth_unique', 'traffic_summary', 'twitter_url', 'Unnamed: 0', 'images']

    df = df.drop(col_to_drop, axis = 1)
    return df
