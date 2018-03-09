# -*- coding: utf-8 -*-

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


def get_name(data):
    L = []
    #F:\project\2 neuron classification\dataset\Zhao 2014 ArXiv\All_Cells_Scaled\C2\207375.swc
    reg = '([0-9]+).swc'
    recom = re.compile(reg)
    for item in data['neuron_name']:
        name = re.findall(recom,item)
        L.append(name[0])
    names = pd.DataFrame(L)
    names.columns=['name']
    return names

    
if __name__ == "__main__":
    start = time.clock()
    date = datetime.datetime.now().strftime("%Y%m%d")
    conn = MySQLdb.connect(host='localhost',port = 3306,user='haoming',passwd='111111',db ='neuron',charset='utf8')
    cur = conn.cursor()
    engine =create_engine('mysql+mysqldb://haoming:111111@localhost:3306/neuron?charset=utf8')
    name = 'all_cells_scaled_simmat_cluster_result_'+ date
    sql1=("select neuron_name,cluster from %s ORDER BY neuron_name" % name)
    data1 = pd.read_sql(sql1,conn)
    print data1.shape
    
    sql2=("select neuron_name, groupID from all_cells_scaled_total_sum order by neuron_name")
    data2 = pd.read_sql(sql2,conn)
    name = get_name(data2)
    data2_new = pd.concat([name,data2.groupID],axis=1,ignore_index=True)
    data2_new.columns=['neuron_name','groupID']
    print data2_new.shape
    
    
    result = data1.merge(data2_new, left_on='neuron_name', right_on='neuron_name', how='inner')
    print result
    
    name_result = 'all_cells_scaled_simmat_result_analysis_'+date
    result.to_sql(name_result,engine,if_exists='replace',index=False,chunksize=1000)

    end = time.clock()
    print end-start


    
