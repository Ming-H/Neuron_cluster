# -*- coding: utf-8 -*-
#/***************************************************************************
# * Copyright (c) 2016 ksrs.com, Inc. All Rights Reserved
# **************************************************************************/
# * @author Haoming
# * @date 2017/01/13
# * @modified 
# * cluster by label propagation alogrithm

import MySQLdb
import pandas as pd
import numpy as np
import re
import codecs 
import logging
import time
import datetime
from sqlalchemy import create_engine
import sys
reload(sys)
sys.setdefaultencoding('utf8')
    
def LP_cluster(p_df):
    num=0
    while len(set(np.array(p_df.index.labels[1])))>100:
        p_df_old = p_df.groupby(p_df.index.labels).sum()    #分组每一列求和(sum of sim)
        member_num = p_df.groupby(p_df.index.labels).size() #分组每一列的数量(num of cluster)
        values = member_num.values[:,np.newaxis]     #转换shape,便于后面广播 
        p_df_new = pd.DataFrame(p_df_old.values/values,columns=p_df_old.columns,index=p_df_old.index)#每一类的平均sim
        max_key = p_df_new.groupby(p_df_new.index.labels[0]).idxmax()  #每一列最大值所在的index，结果为dataframe  
        d = {key: value for (key, value) in max_key['sim']} 
        index_new = np.array([d[item] for item in np.array(p_df.index.labels[1])])
        p_df.index.labels = [p_df.index.labels[0],index_new]
        print len(set(np.array(p_df.index.labels[1]))),num,\
            abs(len(set(np.array(p_df.index.labels[1])))-len(set(np.array(p_df_old.index.labels[1])))) / float(len(set(np.array(p_df_new.index.labels[1])))),\
            p_df.groupby(p_df.index.labels).size().values.max(),'\n\n'
            
        num += 1
        if num >15:
            break
        if  abs(len(set(np.array(p_df.index.labels[1])))-len(set(np.array(p_df_old.index.labels[1])))) / float(len(set(np.array(p_df_new.index.labels[1])))) < 0.01:
            break
        if p_df.groupby(p_df.index.labels).size().values.max()>300:
            break
    cluster = pd.DataFrame(d.values())
    cluster.columns=['cluster']
    return cluster
  
if __name__ == "__main__":
    start = time.clock()
    date = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
    conn = MySQLdb.connect(host='localhost',port = 3306,user='haoming',passwd='111111',db ='neuron',charset='utf8')
    cur = conn.cursor()
    engine =create_engine('mysql+mysqldb://haoming:111111@localhost:3306/neuron?charset=utf8')
    sql=("select input1,input2,biesa,dsa from all_cells_scaled_distance where pds<0.5")
    data_raw = pd.read_sql(sql,conn)
    data_raw = data_raw.set_index(['input2','input1'])
    alpha = 3.1
    data_raw['sim'] = data_raw['biesa'] - alpha*data_raw['dsa']
    p_df = pd.DataFrame(data_raw['sim'],columns=['sim'])
    print p_df
    result = LP_cluster(p_df)
    result = pd.concat([pd.DataFrame(p_df.index.levels[0]),result],axis=1,ignore_index=True)
    result.columns=['neuron_name','clusterID']
    print result
    result.to_sql('all_cells_scaled_distance_result',engine,if_exists='replace',index=False,chunksize=1000)
    
    end = time.clock()
    print end-start


    
