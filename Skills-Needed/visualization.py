# -*- coding: utf-8 -*-

import pandas as pd
import settings
import matplotlib.pyplot as plt
import seaborn as sns
import text_preprocess


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


def create_barplot(title):    
    data= pd.read_csv(settings.path_analitics+text_preprocess.url_fitting(title)+"_grouped_requirements.csv")
    data=data[(data['ratio_in_description']>=0.2) 
               &(~data.requirement.isin(education))
               &(data['lowcase']!=title.lower())
              ]
    data['ratio_in_description']=data['ratio_in_description']*100
    data=data.sort_values(by=['ratio_in_description'])  
    plt.figure(figsize = (18,8))
    graph=sns.barplot(x="ratio_in_description", y="requirement", data=data,palette="Set3")   
    graph.set(xlabel=None, ylabel=None, title=title)    
    for p in graph.patches:
        graph.annotate(
            str(round(p.get_width(),1))+' %',
#            "%.0f" % p.get_width(), 
                       xy=(p.get_width(), p.get_y()+p.get_height()/2),  xytext=(5, 0), textcoords='offset points', ha="left", va="center")
    return graph



education=["Bachelor's","Master's","Doctorate"]