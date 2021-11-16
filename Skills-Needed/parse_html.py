# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import date,timedelta
import text_preprocess
import pandas as pd


def calculate_date(string):
    today=date.today()
    res = [int(i) for i in string.split() if i.isdigit()] 
    if len(res)>0:
        posting_date=today- timedelta(res[0])
    else:
        posting_date=today
        
    return  posting_date


def get_jobs(job):
    jk=job['data-jk']
#        url=base_url+'viewjob?jk='+jk    
    Title=job.find('h2', class_='title').get_text()    
    Company=job.find('span', class_='company')
    if Company:
        Company=Company.get_text()
        
        
    location=job.find('span', class_='location')
    if location:
        Address=location.get_text()
    else:
        Address=''
            
    Posting_date=calculate_date(job.find('span', class_='date').get_text())
#    print(str(Title)+' / '+str(Company)+' / '+str(Address))  
    return(Title, Company, Address, Posting_date, jk)            

def check_jobs(page):
    page_soup=BeautifulSoup(page, 'lxml')
    jobs = page_soup.find_all('div', class_='job_seen_beacon')
    return jobs

def extract_description(source_code):
    soup=BeautifulSoup(source_code, 'html.parser')
    description=soup.find('div', class_='jobsearch-JobComponent-description')
    if description:
        return description.get_text(separator=' ')
    else:        
        return False


def extract_degrees(source_code):
    soup=BeautifulSoup(source_code, 'html.parser')
    degrees=soup.find_all('li')
    degrees_list=[]
    for degree in degrees:
        degrees_list.append(degree.get_text(separator=' '))
        
    return degrees_list


def extract_requirements(source_code,job_id):
    qualifications=pd.DataFrame()
    soup=BeautifulSoup(source_code, 'html.parser')    
    qualifications_list = soup.find('ul', class_='icl-u-xs-my--none jobsearch-ReqAndQualSection-item--closedBullets')
    if qualifications_list:
        qualifications_points=qualifications_list.find_all('li')
        for point in qualifications_points:
            string=point.get_text(separator=' ')
            cleaned=text_preprocess.full_clean(string)            
            print(cleaned)
            qualifications=qualifications.append({'job_id':job_id,'requirement':cleaned},ignore_index=True)
   
    return qualifications    
