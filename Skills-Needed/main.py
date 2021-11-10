# -*- coding: utf-8 -*-

import database
import settings
import os
import text_preprocess
import pandas as pd
import parse_html


#Returns Data Frame containing jobs associated with specific job title id.
#Colomns:'Id', 'Posting_date', 'Title', 'Company', 'Address', 'jk', 'description', 'lem_description', 'clean_description'
def get_data(title_id):
    jobs_id=database.get('jobs_per_titles','job_id',['title_id'],[title_id])        
    return database.get_in('jobs', '*', 'Id', jobs_id['job_id'] )


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


def extract_requirements(full_updating=False):    
    if full_updating:
         metas_ids=database.get('jobs_meta','job_id',['requirements_list'],[1])                    
         files_ids.extend(metas_ids)        
         requirements=pd.DataFrame()
    else:
         requirements= pd.read_csv (settings.path_analitics+'requirements.csv')
         files_ids=[x for x in files_ids if int(x) not in requirements['job_id'] ]
           
    for id in files_ids:
        print(id)
        with open(settings.path_jobs+str(id)+'.html', 'r', encoding='utf-8') as HtmlFile:
            source_code = HtmlFile.read()
            id_requirements=parse_html.extract_requirements(source_code,id)
            title=database.get('jobs_per_titles','Title_id',['Job_id'],[id])
            print(title)
            print(title[0])
            id_requirements['title']=title[0]
            requirements=requirements.append(id_requirements,ignore_index=True)
            print(id_requirements)
            print('_______________________________')
            if len(id_requirements)>0:
                if id not in metas_ids:                    
                    database.insert('jobs_meta', ['job_id','requirements_list'], [id,1])             
                    
            else:
                if id not in metas_ids:
                    database.insert('jobs_meta', ['job_id','requirements_list'], [id,0])
                
            HtmlFile.close()    
            requirements.to_csv(settings.path_analitics+"requirements.csv",index=False)       
    return 

def extract_description():
    print('hey')
    
    
    
def extract_info_from_html(full_updating=False):
    files=os.listdir(settings.path_jobs)
    files_ids=[text_preprocess.extract_id(item) for item in files]
    existing_ids=database.get('jobs','Id',['description'],['IS NOT NULL'],'',delimiter='') 
#    extract_description()    
#    extract_requirements()
    return existing_ids

t=extract_info_from_html()
