# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import MySQLdb
from sqlalchemy import create_engine
import time
import re
import os
os.chdir('F:/neuron/neuron_data/All_Cells_Scaled')


if __name__=="__main__":
    start = time.clock()
    conn = MySQLdb.connect(host='localhost',port = 3306,user='haoming',passwd='111111',db ='neuron',charset='utf8')
    cur = conn.cursor()
    engine =create_engine('mysql+mysqldb://haoming:111111@localhost:3306/neuron?charset=utf8')
    
    ## data to mysql
    data = pd.read_csv('simmat.txt',sep=' ')
    data = data.drop(['Unnamed: 379'],axis=1)
    #print data.shape
    #print data.columns
    data.to_sql('all_cells_scaled_simmat',engine,if_exists='replace',index=False,chunksize=1000)    
    
    
    ## get name lists
    name_list = pd.DataFrame(data.columns)
    name_list.to_sql('all_cells_scaled_namelist',engine,if_exists='replace',index=False,chunksize=1000)   
    
    ## normlized
    data_value = data.values
    print data_value
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            data_value[i,j] = data_value[i,j] / max((data_value[i,i], data_value[j,j]))

    data_norm = pd.DataFrame(data_value)
    #print data_norm.shape
    data_norm.to_sql('all_cells_scaled_simmat_norm',engine,if_exists='replace',index=False,chunksize=1000)    

    end = time.clock()
    print end-start
            