# -*- coding: utf-8 -*-
import connector
import pandas as pd


connection=connector.connect()   

# Select from table Where and condition
def get(table, selector="*",columns=False,values=False, condition='=', delimiter='"'):
    statement='SELECT '+selector+' FROM '+table
    if columns:
        statement=loop(statement, columns, values,delimiter,condition,)
        
    print(statement)    
    return pd.read_sql(statement, connection )


# Select from table where in condition
def get_in(table, selector, column, values_list):
    values_str=', '.join([str(elem) for elem in values_list])
    statement='SELECT '+selector+' FROM '+table+' WHERE '+column+' IN ('+values_str+' )' 

    return pd.read_sql(statement, connection )

# loop creating multiple "and" conditions
def loop(statement, columns, values,delimiter='"',condition='='):
    statement=statement+" WHERE "+columns[0]+condition+' '+ delimiter+str(values[0])+delimiter
    num=len(columns)
    if len(columns)>1:
        columns.pop(0)
        values.pop(0)
        for i in range(num-1):        
            statement=statement+" AND "+columns[i]+"='"+str(values[i])+"'"
        
#    print (statement)
    return statement

def to_df(table):
    return pd.read_sql('SELECT * FROM '+ table, connection )



    