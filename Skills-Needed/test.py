# -*- coding: utf-8 -*-

import main
import database

def test_extract_description(test_ids):
    for id in test_ids: 
        description=main.extract_description([id])    
        if len(description)<50:
            print('test_extract_description fail')
            return False
    return True
    
    
    
def get_random_job_ids(n):
   return database.get('jobs', 'Id')




t=get_random_job_ids(5)
   
    
    
    