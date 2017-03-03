# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import MySQLdb
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
import time
import re
    
if __name__=="__main__":
    start = time.clock()
    conn = MySQLdb.connect(host='localhost',port = 3306,user='haoming',passwd='111111',db ='neuron',charset='utf8')
    cur = conn.cursor()
    engine =create_engine('mysql+mysqldb://haoming:111111@localhost:3306/neuron?charset=utf8')
    train_data = pd.DataFrame()
    test_data = pd.DataFrame()
    data_all = pd.DataFrame()
    group_data = pd.read_sql('select distinct groupID from all_cells_scaled',conn)
    for item in group_data['groupID']:   
        sql=("select neuron_name,neuron_features,total_Sum from all_cells_scaled where groupID ='%s'" %item)
        data = pd.read_sql(sql,conn)
        data = data.set_index(['neuron_name','neuron_features'])
        data = data.unstack()
        data = data.reset_index('neuron_name')
        data_all = pd.concat([data_all,data],ignore_index=True)
        '''
        X_train,X_test=train_test_split(data,test_size=0.3)
        train_data = pd.concat([train_data,X_train],ignore_index=True)
        test_data = pd.concat([test_data,X_test],ignore_index=True)
        print train_data.shape,test_data.shape
        '''
    group_ID = pd.read_sql('select distinct neuron_name, groupID from all_cells_scaled',conn)
    data_all = pd.concat([data_all,group_ID['groupID']],axis=1,ignore_index=True)
    columns_features = pd.read_sql('select distinct neuron_features from all_cells_scaled',conn)
    columns = ['neuron_name']+[item.strip() for item in columns_features['neuron_features']]+['groupID']
    data_all.columns = columns
    data_all.to_sql('all_cells_scaled_total_Sum',engine,if_exists='replace',index=False,chunksize=1000) 
    end = time.clock()
    print end-start
    