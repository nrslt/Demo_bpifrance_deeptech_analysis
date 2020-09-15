import pandas as pd
import matplotlib.pyplot as plt
import ast
import os
import numpy as np
from bpideep import list_industries,list_technologies,list_tags,list_background_team,list_degree_team,list_income_streams,list_investors_name,list_investor_type

data_path = os.path.join(os.path.dirname(__file__), "data")
patents_df = pd.read_csv(f"{data_path}/patents.csv")

def encoder(data, column):
    '''
    encoder function that takes a pandas dataframe (data) \
    and a column name (str) as parameters
    returns a new_df with OHE-like columns
    '''

    def return_list(data,column):
        list_ = []
        data_ = data[column]
        for x in range(len(data_)):
            if type(data_.iloc[x]) == str:
                data_1 = ast.literal_eval(data_.iloc[x])
                for y in range(len(data_1)):
                    if data_1[y] not in list_:
                        list_.append(data_1[y])
            elif type(data_.iloc[x]) == list:
                data_1 = data_.iloc[x]
                for y in range(len(data_1)):
                    if data_1[y] not in list_:
                        list_.append(data_1[y])
        return list_
    list_ = return_list(data,column)
    new_df = pd.DataFrame(columns= list_)
    for u in range(len(data)):
        data_ = data[column][u]
        dict_ = {}
        for n in list_:
            if type(data_) == str:
                company_ = ast.literal_eval(data_)
                if n in company_:
                    encoder = 1
                else:
                    encoder = 0
                dict_[n] = encoder
            elif type(data_) == list:
                company_ = data_
                if n in company_:
                    encoder = 1
                else:
                    encoder = 0
                dict_[n] = encoder
        new_df.loc[u] = dict_
    return new_df



def return_filling(data, column):
    '''
    function that returns features 'presence' for each type \
    (deeptech, non-deeptech, all companies) in data dataframe
    '''

    def return_value(x) :
        if type(x) == str :
            if ast.literal_eval(x):
                return 1
            else :
                return 0
        if type(x) == list :
            if x:
                return 1
            else :
                return 0
    data['return_filling'] = data[column].map(lambda x : return_value(x))
    print(f'deeptech : {data[data["target"]==1]["return_filling"].value_counts()[1]/len(data[data["target"]==1])}')
    print(f'non deeptech : {data[data["target"]==0]["return_filling"].value_counts()[1]/len(data[data["target"]==0])}')
    print(f'total : {data["return_filling"].value_counts()[1] / len(data)}')



def background(x):
    '''
    function that extracts info from 'team' column
    enables a mapping to create a new feature:
    data['background_team'] = data['team'].map(lambda x:background(x))
    '''

    backgrounds_list = []
    team = x
    for y in range(len(team['items'])):
            backgrounds= team['items'][y]['backgrounds']
            for u in range(len(backgrounds)):
                backgrounds_list.append(backgrounds[u]['name'])
    return backgrounds_list




def degree(x):
    '''
    function that extracts the degree name from the 'team' column in data
    enables a mapping to be applied on 'team':
    data['degree_team'] = data['team'].map(lambda x:degree(x))
    '''

    degree_list = []
    team = x
    for y in range(len(team['items'])):
            universities= team['items'][y]['universities']['items']
            if universities and universities[0]['degree'] is not None :
                degree = universities[0]['degree']['name']
                degree_list.append(degree)
    return degree_list




def degree_quant(x):
    '''
    function that encodes whether or not a doctor works within the company,
    works in pair with the function degree
    enables a mapping to be applied on 'degree_team':
    data['doctor'] = data['degree_team'].map(lambda x: degree_quant(x))
    '''

    if len(x) == 0:
        return 0
    else :
        for n in range(len(x)):
            if x[n] in ['Doctor','PhD'] :
                return 1
            else :
                return 0



def funding_amounts_employees(data):
    '''
    function that performs the ratio between funding and employees
    '''

    funding = data['total_funding_source']
    employees = data['employees_latest']

    return funding/employees



def growth_stage_num(data):
    '''
    function that maps the 'growth stage' as an ordinal feature
    '''

    stage_status = data['growth_stage'].map({'mature' : 4,
                                            'late growth' : 3,
                                            'early growth' : 2,
                                            'seed' : 1})
    return stage_status


def industries(x):
    '''
    function that extracts info from 'industries' column through mapping
    data['industries_list'] = data['industries'].map(lambda x: industries(x))
    '''

    industries_list = []
    industries = x
    for u in range(len(industries)):
            industries_list.append(industries[u]['name'])
    return industries_list


def investors_name(x) :
    investors_list = []
    investors = x
    if investors['total'] > 0 :
        for y in range(len(investors['items'])):
                investors_list.append(investors['items'][y]['name'])
    return investors_list



def investors_type(x) :
    investors_list = []
    investors = x
    if investors['total'] > 0 :
        for y in range(len(investors['items'])):
                investors_list.append(investors['items'][y]['type'])
    return investors_list





def tags_reduction(encoded_dataframe, threshold = 0.02):
    '''
    function that performs a dimension reduction operation: \
    selects only tags that appear above a certain threshold (ex: 0.02)
    to be applied on the encoded tags dataframe
    '''

    tags_series_count = encoded_dataframe[encoded_dataframe == 1].sum()\
    .sort_values(ascending = False)/encoded_dataframe.shape[0]
    retained_tags = tags_series_count[tags_series_count > threshold].index.tolist()

    return encoded_dataframe[retained_tags]




def substract_date(x):
    return 2020 - x



def return_ratio(x):
    '''
    function that computes the growth stage over years of existance ratio
    '''

    if x['year_of_existence'] >0 :
        return x['growth_stage_num']/x['year_of_existence']
    return x['growth_stage_num']




def feat_eng(data):
    '''
    takes a pandas df as input
    global feature engineering function that performs all above mentioned \
    transformations and returns a new dataframe
    '''

    # new features in data as columns
    data['background_team'] = data['team'].map(lambda x:background(x))
    data['degree_team'] = data['team'].map(lambda x:degree(x))
    data['doctor_yesno'] = data['degree_team'].map(lambda x: degree_quant(x))
    data['funding_employees_ratio'] = funding_amounts_employees(data)
    data['has_strong_founder'] = data['has_strong_founder'].map({True : 1,
                                                                False : 0})
    data['has_super_founder'] = data['has_super_founder'].map({True : 1,
                                                               False : 0})
    data['growth_stage_num'] = growth_stage_num(data)
    data['industries_list'] = data['industries'].map(lambda x: industries(x))

    data['year'] = pd.DataFrame({'year': data['launch_year']})
    data['year_of_existence'] = data['year'].map(lambda x : substract_date(x))
    data['stage_age_ratio'] = data[['year_of_existence','growth_stage_num']]\
                                .apply(return_ratio,axis=1)
    data['investors_name'] = data['investors'].map(lambda x:investors_name(x))
    data['investors_type'] = data['investors'].map(lambda x:investors_type(x))



    # encoded features
    background_team_encoded_df = encoder(data, 'background_team')
    degree_team_encoded_df = encoder(data,'degree_team')
    industries_encoded_df = encoder(data,'industries_list')
    income_streams_encoded_df = encoder(data,'income_streams')
    technologies_encoded_df = encoder(data,'technologies')
    tags_encoded_df = encoder(data,'tags')
    investors_name_encoded_df = encoder(data, 'investors_name')
    investors_type_encoded_df = encoder(data, 'investors_type')


    # processed encoded features
    # tags_retained = tags_reduction(tags_encoded_df, threshold = 0.02)
    # background_retained = tags_reduction(background_team_encoded_df, threshold = 0.01)
    # industries_retained = tags_reduction(industries_encoded_df, threshold = 0.01)

    # to concat
    concat_df = pd.concat([
                        data[['id',
                            'doctor_yesno',
                            'funding_employees_ratio',
                            'has_strong_founder',
                            'has_super_founder',
                            'stage_age_ratio'
                            ]],
                        tags_encoded_df.drop(columns = 'health'),
                        background_team_encoded_df,
                        industries_encoded_df,
                        degree_team_encoded_df,
                        income_streams_encoded_df,
                        technologies_encoded_df,
                        investors_name_encoded_df,
                        investors_type_encoded_df,
                        data[['target']]
                        ], axis = 1)

    # merge concat_df with patents to get patents info
    concat_df = concat_df.merge(patents_df[['nb_patents', 'id']], on = 'id', how = 'left')

    # we keep a trace of all features list (by group of features)
    simple_features = ['id',
                        'doctor_yesno',
                        'funding_employees_ratio',
                        'has_strong_founder',
                        'has_super_founder',
                        'stage_age_ratio',
                        'nb_patents']
    # tags_features = tags_retained.columns.tolist()
    # background_features = background_retained.columns.tolist()
    # industries_features = industries_retained.columns.tolist()
    # degree_team_features = degree_team_encoded_df.columns.tolist()
    # income_streams_features = income_streams_encoded_df.columns.tolist()
    # technologies_features = technologies_encoded_df.columns.tolist()
    # investors_name_features = investors_name_encoded_df.columns.tolist()
    # investors_type_features = investors_type_encoded_df.columns.tolist()


    # and store these lists in a dict that is returned along with the new concat_df
    # features_dict = {}
    # features_dict['simple_features'] = simple_features
    # features_dict['tags_features'] = tags_features
    # features_dict['background_features'] = background_features
    # features_dict['industries_features'] = industries_features
    # features_dict['degree_team_features'] = degree_team_features
    # features_dict['income_streams_features'] = income_streams_features
    # features_dict['technologies_features'] = technologies_features
    # features_dict['investors_name'] = investors_name_features
    # features_dict['investors_type'] = investors_type_features


    # selection of columns to keep
    kept_tags = ['technical',
                 'health',
                 'semiconductors',
                 'energy',
                 'commission',
                 'biotechnology',
                 'neurology',
                 'saas',
                 'fund',
                 'Agoranov']

    kept_columns = simple_features + kept_tags
    kept_columns.append('target')

    return concat_df[kept_columns]




def feat_eng_new_entry(data):
    '''
    takes a pandas df as input
    global feature engineering function that performs all above mentioned \
    transformations and returns a new dataframe
    '''

    # new features in data as columns
    data['background_team'] = data['team'].map(lambda x:background(x))
    data['degree_team'] = data['team'].map(lambda x:degree(x))
    data['doctor_yesno'] = data['degree_team'].map(lambda x: degree_quant(x))
    data['funding_employees_ratio'] = funding_amounts_employees(data)
    data['has_strong_founder'] = data['has_strong_founder'].map({True : 1,
                                                                False : 0})
    data['has_super_founder'] = data['has_super_founder'].map({True : 1,
                                                               False : 0})
    data['growth_stage_num'] = growth_stage_num(data)
    data['industries_list'] = data['industries'].map(lambda x: industries(x))

    data['year'] = pd.DataFrame({'year': data['launch_year']})
    data['year_of_existence'] = data['year'].map(lambda x : substract_date(x))
    data['stage_age_ratio'] = data[['year_of_existence','growth_stage_num']]\
                                .apply(return_ratio,axis=1)
    data['investors_name'] = data['investors'].map(lambda x:investors_name(x))
    data['investors_type'] = data['investors'].map(lambda x:investors_type(x))

    def encoder_predict(data, column, list_):
    '''
    encoder function that takes a pandas dataframe (data) \
    and a column name (str) as parameters
    returns a new_df with OHE-like columns
    '''
        list_ = return_list(data,column)
        new_df = pd.DataFrame(columns= list_)
        for u in range(len(data)):
            data_ = data[column][u]
            dict_ = {}
            for n in list_:
                if type(data_) == str:
                    company_ = ast.literal_eval(data_)
                    if n in company_:
                        encoder = 1
                    else:
                        encoder = 0
                    dict_[n] = encoder
                elif type(data_) == list:
                    company_ = data_
                    if n in company_:
                        encoder = 1
                    else:
                        encoder = 0
                    dict_[n] = encoder
            new_df.loc[u] = dict_
        return new_df


    # encoded features

    background_team_encoded_df = encoder_predict(data, 'background_team', list_background_team)
    degree_team_encoded_df = encoder_predict(data,'degree_team',list_degree_team)
    industries_encoded_df = encoder_predict(data,'industries_list',list_industries)
    income_streams_encoded_df = encoder_predict(data,'income_streams',list_income_streams)
    technologies_encoded_df = encoder_predict(data,'technologies',list_technologies)
    tags_encoded_df = encoder_predict(data,'tags',list_tags)
    investors_name_encoded_df = encoder_predict(data, 'investors_name',list_investors_name)
    investors_type_encoded_df = encoder_predict(data, 'investors_type',list_investor_type)

    # to concat
    concat_df = pd.concat([
                        data[['id',
                            'doctor_yesno',
                            'funding_employees_ratio',
                            'has_strong_founder',
                            'has_super_founder',
                            'stage_age_ratio'
                            ]],
                        tags_encoded_df.drop(columns = 'health'),
                        background_team_encoded_df,
                        industries_encoded_df,
                        # degree_team_encoded_df,
                        income_streams_encoded_df,
                        technologies_encoded_df,
                        investors_name_encoded_df,
                        investors_type_encoded_df,
                        data[['target']]
                        ], axis = 1)


    # we keep a trace of all features list (by group of features)
    simple_features = ['id',
                        'doctor_yesno',
                        'funding_employees_ratio',
                        'has_strong_founder',
                        'has_super_founder',
                        'stage_age_ratio',
                        'nb_patents']


    # selection of columns to keep
    kept_tags = ['technical',
                 'health',
                 'semiconductors',
                 'energy',
                 'commission',
                 'biotechnology',
                 'neurology',
                 'saas',
                 'fund',
                 'Agoranov']

    kept_columns = simple_features + kept_tags
    kept_columns.append('target')

    return concat_df[kept_columns]











