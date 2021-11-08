# -*- coding: utf-8 -*-

import database



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




t=get_job_title(2)


