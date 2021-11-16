# -*- coding: utf-8 -*-

import database
import settings
import text_preprocess
import pandas as pd



#Returns Data Frame containing jobs associated with specific job title id.
#Colomns:'Id', 'Posting_date', 'Title', 'Company', 'Address', 'jk', 'description', 'lem_description', 'clean_description'
def get_data(title_id, column='*'):
    jobs_id=database.get('jobs_per_titles','job_id',['title_id'],[title_id])        
    return database.get_in('jobs', column, 'Id', jobs_id['job_id'] )


# Returns string name associated with title id 
def get_job_title(title_id):
    return database.get('job_titles','Title',['Id'],[title_id]).values[0][0]



# Returns Data Frame containing job titles, number of jobs associated with each title, and earliest and latest posting dates
def get_job_count_by_titles():    
    titles=database.to_df('job_titles')    
    for id in titles['Id']:
        print('Loading jobs with title '+titles[titles['Id']==id]['Title'].values[0])
        jobs_ids=database.get('jobs_per_titles','job_id',['title_id'],[id])
        titles.loc[titles['Id']==id,'num_of_jobs']=len(jobs_ids)        
        dates=database.get_in('jobs', 'Posting_date', 'Id', jobs_ids['job_id'] )        
        titles.loc[titles['Id']==id,'min_date']=min(dates['Posting_date'])        
        titles.loc[titles['Id']==id,'max_date']=max(dates['Posting_date'])

    
    return titles

#Prepares a CSV file containing the requirements for a particular job title
#Imput Title Id INT; Output CSV file  
def create_requirements_by_title(title_id):
    title=text_preprocess.url_fitting(get_job_title(title_id))
    jobs_ids=get_data(title_id,'Id')['Id']
    print('Creating requerements outlook for '+title)
    requirements= pd.read_csv (settings.path_analitics+'requirements.csv')
    requirements=requirements[(requirements['job_id'].isin(jobs_ids)) &(requirements['requirement'].notnull()) ]
    num=len(requirements)
    
    requirements['requirement']=[text_preprocess.full_clean(text) for text in requirements['requirement']]
    requirements['requirement']=[text_preprocess.remove_unuseful(text) for text in requirements['requirement']]
    requirements['lowcase']=[text_preprocess.charts_clean(text) for text in requirements['requirement'].str.lower() ]   
    requirements['lem']=[text_preprocess.lemmitization(text) for text in requirements['requirement'].str.lower()]    
    
    grouped_count=requirements.groupby('lem', as_index=False).count()[['lem','job_id']]
    grouped_first=requirements.groupby('lem', as_index=False).first()[['requirement','lem','lowcase']]   
    grouped_requirements=pd.merge(grouped_count, grouped_first, on="lem")
    grouped_requirements=grouped_requirements.rename(columns={"job_id": "count"})
    
    grouped_requirements['count_percentage']=(100*grouped_requirements['count'] ) /num
    grouped_requirements=grouped_requirements.replace("", float("NaN"))
    grouped_requirements=grouped_requirements.dropna(axis=0,  how='any')
    
    grouped_requirements=grouped_requirements.sort_values(by=['count_percentage'], ascending=False)    
    grouped_requirements.to_csv(settings.path_analitics+title+"_grouped_requirements.csv")  
    
    return requirements




create_requirements_by_title(get_job_count_by_titles()['Id'])