import pandas as pd
from google.cloud import bigquery


class Patent():

    def __init__(self):
        pass

    def name_clean(self,column_name):
        '''Clean the name column for Big Query'''
        name_clean = column_name.str.replace('-', ' ').str.replace("'", '').str.upper()
        return name_clean

    def get_bulk_patents(self,data):
        '''return all patents for companies by searching each companies' names in Big Query
           names needs to be harmonized with name_clean() before using this function'''
        client = bigquery.Client(project='gold-hybrid-288409')
        dataset_ref = client.dataset('bpius')

        #Empty df to put every searchings
        df = pd.DataFrame(columns=['id', 'id_patents', 'country_code', 'harmonized_assignee', 'top_terms', 'nb_similar'])

        if 'clean_name' not in data.columns:
            return print('clean_name is not a column of the input dataFrame')

        for i in data.index:
            name = data.loc[i,'clean_name']
            ids = data.loc[i,'id']

            sql = ( 'SELECT patents.publication_number, patents.country_code, ARRAY(SELECT name FROM UNNEST(patents.assignee_harmonized)), '
                    'google.top_terms, (SELECT COUNT(publication_number) FROM UNNEST(google.similar)) AS similar '
                    'FROM `patents-public-data.patents.publications_202004` AS patents '
                    'LEFT JOIN `patents-public-data.google_patents_research.publications_202004` AS google ON patents.publication_number = google.publication_number '
                    f'WHERE "{name}" in UNNEST(ARRAY(SELECT name FROM UNNEST(patents.assignee_harmonized)))' )

            query = client.query(sql)
            results = query.result()

            # Dictionnary to add the query's results
            r_dic = {'id':[], 'id_patents': [],'country_code':[],'harmonized_assignee':[],'top_terms':[],'nb_similar':[] }

            for row in results:
                r_dic['id'].append(ids)
                r_dic['id_patents'].append(row[0])
                r_dic['country_code'].append(row[1])
                r_dic['harmonized_assignee'].append(row[2])
                r_dic['top_terms'].append(row[3])
                r_dic['nb_similar'].append(row[4])

            # Concatenate the query and df
            r_df = pd.DataFrame.from_dict(r_dic)
            df = pd.concat([df,r_df])

        return df

    def new_companies(self,old_df, new_df):
        ''' Get the names of the new companies added to the dataset'''
        new_companies = pd.concat([old_df[['id']],new_df[['id']]]).drop_duplicates(keep=False)
        new_companies.dropna(subset = ['name'], inplace = True)
        return new_companies

    def get_patents(self, company_name):
        '''Get patents informations for one company '''
        clean_name = company_name.replace('-', ' ').replace("'", '').upper()
        client = bigquery.Client(project='gold-hybrid-288409')
        dataset_ref = client.dataset('bpius')

        sql = ( 'SELECT patents.publication_number, patents.country_code, ARRAY(SELECT name FROM UNNEST(patents.assignee_harmonized)), '
                'google.top_terms, (SELECT COUNT(publication_number) FROM UNNEST(google.similar)) AS similar '
                'FROM `patents-public-data.patents.publications_202004` AS patents '
                'LEFT JOIN `patents-public-data.google_patents_research.publications_202004` AS google ON patents.publication_number = google.publication_number '
                f'WHERE "{clean_name}" in UNNEST(ARRAY(SELECT name FROM UNNEST(patents.assignee_harmonized)))' )

        query = client.query(sql)
        results = query.result()

        results_dic = { 'id_patents': [],'country_code':[],'harmonized_assignee':[],'top_terms':[],'nb_similar':[] }

        for row in results:
            results_dic['id_patents'].append(row[0])
            results_dic['country_code'].append(row[1])
            results_dic['harmonized_assignee'].append(row[2])
            results_dic['top_terms'].append(row[3])
            results_dic['nb_similar'].append(row[4])

        # Concatenate the query and df
        results_df = pd.DataFrame.from_dict(results_dic)

        return results_df

    def get_nb_patents(self, company_name):
        '''Get number of patents for one company '''
        clean_name = company_name.replace('-', ' ').replace("'", '').upper()
        client = bigquery.Client(project='gold-hybrid-288409')
        dataset_ref = client.dataset('bpius')

        sql = ( 'SELECT COUNT(*) '
                'FROM `patents-public-data.patents.publications_202004` AS patents '
                'LEFT JOIN `patents-public-data.google_patents_research.publications_202004` AS google ON patents.publication_number = google.publication_number '
                f'WHERE "{clean_name}" in UNNEST(ARRAY(SELECT name FROM UNNEST(patents.assignee_harmonized)))' )

        query = client.query(sql)
        results = query.result()

        # results_dic = { 'id_patents': [],'country_code':[],'harmonized_assignee':[],'top_terms':[],'nb_similar':[] }

        for row in results:
            n_patents = row[0]


        return n_patents







