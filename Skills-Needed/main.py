# -*- coding: utf-8 -*-

import database
import settings
import text_preprocess
import pandas as pd
from os.path import exists
import visualization


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
    requirements['lem']=[text_preprocess.lemmitization(text) for text in requirements['lowcase']]    
    
    grouped_count=requirements.groupby('lem', as_index=False).count()[['lem','job_id']]
    grouped_first=requirements.groupby('lem', as_index=False).first()[['requirement','lem','lowcase']]   
    grouped_requirements=pd.merge(grouped_count, grouped_first, on="lem")
    grouped_requirements=grouped_requirements.rename(columns={"job_id": "count"})
    
    grouped_requirements['count_percentage']=(100*grouped_requirements['count'] ) /num
    grouped_requirements=grouped_requirements.replace("", float("NaN"))
    grouped_requirements=grouped_requirements.dropna(axis=0,  how='any')
    
    grouped_requirements=grouped_requirements.sort_values(by=['count_percentage'], ascending=False)    
    grouped_requirements.to_csv(settings.path_analitics+title+"_grouped_requirements.csv",index=False)  
    
    return grouped_requirements



# Identifying job requirements from a job description
# Input Title id INT; Output two CSV files containing the number of times each requirement is mentioned in the job description
def search_for_requerements_in_descriptions(title_id):
    jobs=get_data(title_id)
    title=text_preprocess.url_fitting(get_job_title(title_id))
    jobs=jobs[jobs['cleared']==1]
    jobs["clean_description"]=[' '+text_preprocess.charts_clean(text)+' ' for text in jobs["clean_description"]]
    if exists(settings.path_analitics+title+"_grouped_requirements.csv"):     
        requirements= pd.read_csv(settings.path_analitics+title+"_grouped_requirements.csv")  
    else:
        requirements=create_requirements_by_title(title_id)
    
    requirements=requirements[requirements['count']>1]
    jobs['requirements']=0     
    i=0
    for requirement in requirements['lowcase']:
        i=i+1        
        requirement=' '+requirement+' '
        found=jobs["clean_description"].str.find(requirement)
        found=found.apply(lambda x: 0 if x <0 else 1)
        if found.sum()>0:
            jobs['requirements']=jobs['requirements']+found        
            jobs[requirement.strip()]=found
            
        requirements.loc[requirements['lowcase']==requirement.strip(), 'in_description']=len(found.drop(labels=found[found<1].index.values)) 

    num_of_jobs=len(jobs)    
    requirements['ratio_in_description']=requirements['in_description']/num_of_jobs
    requirements.to_csv(settings.path_analitics+title+"_grouped_requirements.csv",index=False)
    jobs.to_csv(settings.path_analitics+title+"_jobs_found.csv",index=False )
    return  requirements 

data_titles_ids=[1,2,3]

search_for_requerements_in_descriptions(2)
#visualization.education_bars([text_preprocess.url_fitting(get_job_title(title_id)) for title_id in data_titles_ids])
visualization.create_barplot(get_job_title(2))
   