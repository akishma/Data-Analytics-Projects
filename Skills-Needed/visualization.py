# -*- coding: utf-8 -*-

import pandas as pd
import settings
import matplotlib.pyplot as plt
import seaborn as sns


def education_bars(titles):
    degrees=pd.DataFrame()
    for title in titles:
        data= pd.read_csv(settings.path_analitics+title+"_grouped_requirements.csv")
        temp=data[data['requirement'].isin(education)]
        temp['Title']=title
        degrees=degrees.append(temp)        
    
    degrees['ratio_in_description']=degrees['ratio_in_description']*100   
    plt.figure(figsize = (18,8))     
    graph=sns.barplot(x="Title", y='ratio_in_description', data=degrees.sort_values("ratio_in_description", ascending=False), hue='requirement' ,palette="Set2") 
    graph.set(ylabel='The percentage of jobs that require education', title='Education requirements by job titles')             
    return graph   





education=["Bachelor's","Master's","Doctorate"]