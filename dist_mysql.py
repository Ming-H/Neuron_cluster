# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import MySQLdb
from sqlalchemy import create_engine
import time
import os
os.chdir("F:/result-2.28")
import re

def eachFile(filepath):
    pathDir = os.listdir(filepath)
    reg = '= (.*)'
    recom = re.compile(reg,re.S)
    data = []
    for item in pathDir:
        L = []
        file_object = open(item)
        for line in file_object:
            L.append(line.split()[-1])
        data.append(L)
    columns = ['input1','input2','esa1','esa2','biesa','dsa','pds']   
    result =  pd.DataFrame(data,columns=columns) 
    print result    
    return result      
    
    
if __name__=="__main__":
    start = time.clock()
    conn = MySQLdb.connect(host='localhost',port = 3306,user='haoming',passwd='111111',db ='neuron',charset='utf8')
    cur = conn.cursor()
    engine =create_engine('mysql+mysqldb://haoming:111111@localhost:3306/neuron?charset=utf8')
    
    filepath = 'F:/result-2.28'
    data = eachFile(filepath)
    data.to_sql('all_cells_scaled_distance',engine,if_exists='replace',index=True,chunksize=1000)    
    
    end = time.clock()
    print end-start
    