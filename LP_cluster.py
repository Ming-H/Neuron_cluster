# -*- coding: utf-8 -*-
# * cluster by label propagation alogrithm(simmat)

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
    p_df[p_df<0.01]=0
    print p_df
    num=0
    while len(set(p_df.columns.values))>89:
        p_df_old = p_df.groupby(p_df.index).sum()    #分组每一列求和(sum of sim)
        member_num = p_df.groupby(p_df.index).size() #分组每一列的数量(num of cluster)
        values = member_num.values[:,np.newaxis]     #转换shape,便于后面广播 
        p_df_new = pd.DataFrame(p_df_old.values/values,columns=p_df_old.columns,index=p_df_old.index)#每一类的平均sim
        max_key = p_df_new.idxmax()   #每一列最大值所在的index，结果为dataframe  
        p_df.columns= max_key.values  #把每一列最大值的index赋给columns
        p_df.index = max_key.values   #把每一列最大值的index赋给index  
        print len(set(p_df.columns.values)), num, abs(len(set(p_df.columns.values))-len(set(p_df_new.columns.values)))/float(len(set(p_df_new.columns.values))), member_num.values.max()
        if num >20:
            break
        #if  abs(len(set(p_df.columns.values))-len(set(p_df_new.columns.values)))/float(len(set(p_df_new.columns.values))) < 0.00001:
            #break
        if member_num.values.max()>300:
            break
        num += 1
        print '\n\n'
    print p_df 
    cluster = pd.DataFrame(p_df.index)
    cluster.columns=['cluster']
    return cluster

    
if __name__ == "__main__":
    start = time.clock()
    date = datetime.datetime.now().strftime("%Y%m%d")
    conn = MySQLdb.connect(host='localhost',port = 3306,user='haoming',passwd='111111',db ='neuron',charset='utf8')
    cur = conn.cursor()
    engine =create_engine('mysql+mysqldb://haoming:111111@localhost:3306/neuron?charset=utf8')
    sql=("select * from all_cells_scaled_simmat_norm")
    data = pd.read_sql(sql,conn)
    for i in range(data.shape[0]):
        data.values[i][i] = 0       
    cluster = LP_cluster(data)
    result = pd.concat([pd.read_sql('select * from all_cells_scaled_namelist',conn),cluster],axis=1,ignore_index=True,names=True)
    result.columns=['neuron_name','cluster']
    name = 'all_cells_scaled_simmat_cluster_result_'+ date
    result.to_sql(name,engine,if_exists='replace',index=False,chunksize=1000)
    end = time.clock()
    print end-start


    
