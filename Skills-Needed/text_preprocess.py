# -*- coding: utf-8 -*-

import re
from nltk.stem import WordNetLemmatizer
import nltk

#from nltk.corpus import wordnet as wn
from textblob import Word


lst_stopwords=nltk.corpus.stopwords.words("english")

words_remove=['professional','relevant','related','work']
words_replace={'cyber security' :'cybersecurity', 'undergraduate': 'bachelor','advanced degree':'masters',   'bs':'bachelor of science', 'ba':'bachelor of arts', 'bachelors': 'bachelor', 'masters': 'master', 'graduate':'master', 
               'phd':'doctorate',
               'dba':'database administrator',
               }

wordnet_lemmatizer = WordNetLemmatizer()

def url_fitting(text):
    formatted=text.replace(" ", "-")
    return formatted


def extract_title(string):
    splitted=string.split('_')
    title=splitted[0].replace("-", " ")
    return title


def sql_fitting(string):
    formatted=string.replace('"','')
    return formatted

def extract_id(string):
    splitted=string.split('.')    
    return splitted[0]

def remove_unuseful(text):    
    text = re.sub(r'\d years', '', text)
    text = re.sub(r'\d year', '', text)
    text=' '+str(text)+' '
    text = re.sub(r' \d ', '', text)
    text=remove_words(text)
    return text.strip()

def remove_words(text,custom=False):    
    if  custom:
        return  [word for word in text if word not in custom] 
    else:
        lst_text=[word for word in text.split(' ') if word not in words_remove]
        return  " ".join(lst_text) 

def remove_stop_words(text):    
    return [word for word in text if word not in lst_stopwords]
     


def full_clean(text):
    text=text.replace("\\",' ')
    text=text.replace("/",' ')
    text=text.replace("+", " plus")
    text = re.sub(r"[^\w\'\s\$\d#\-]", '', str(text).strip())
    lst_text = text.split()    
    lst_text =remove_stop_words(lst_text)    
    text = " ".join(lst_text)
    text=text.strip()
    text=text.lower()    
    return replace(text)

def charts_clean(text):
    text=text.replace("'s",'')
    return re.sub(r"[^\w\s]", ' ', str(text).strip())

    
def replace(text):    
     for words in words_replace:
         text= text.replace(' '+words+" "," "+words_replace[words]+' ')
     return text    
         
def lemmitization(text):    
    lst_text=text.split()
    lst_text = [wordnet_lemmatizer.lemmatize(word) for word in lst_text ]     
    text = " ".join(lst_text)    
    return text.strip()



def test(word):
    print(word)
    word=remove_unuseful(word)
    print(word)
    word=full_clean(word)
    print(word)
    word=lemmitization(word)
    print(word)
        
    


     