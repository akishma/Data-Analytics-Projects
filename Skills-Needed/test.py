# -*- coding: utf-8 -*-

import scrapping
import database
import pandas as pd
import settings

def test_extract_description(test_ids):
    print('Extract description testing')    
    for id in test_ids:        
        description=scrapping.extract_description(id)
        updated_description=database.get('jobs','clean_description',['Id'],[id])['clean_description'][0]               
        if len(description)<50:
            print('fail len')
            return False
        
        if description!=updated_description:
            print('fail update')
            return False  

        
    print('PASS')   
    return True
    
 
    
def get_random_job_ids(x):
    df=database.get('jobs', 'Id')
    sample=df['Id'].sample(n=x)
    return sample

def test_requirements_group(file):
    requirements= pd.read_csv(file)
    requirements['diff']=requirements.apply(lambda x: 1 if x['requirement'].lower() == x['lem'] else 0, axis=1)
    return  requirements[requirements['diff']==0]
    

def full_system_test(x):
    if ~test_extract_description(get_random_job_ids(x)):
        return False
   
    print('_________________________') 
    
    
t=test_requirements_group(settings.path_analitics+'Data-engineer_grouped_requirements.csv')   
#full_system_test(5)    
    
    