


import pandas as pd
import numpy as np 
import os 
from pandas import DataFrame,Series
import re


# df = pd.read_csv(r'/mnt/e/analasy/data.csv', encoding='unicode_escape')
df = pd.read_csv(r'/mnt/e/analasy/data.csv')

print(df.columns)  #查看列名
# print(df.dtypes) 

for row_index, row in df.iterrows():
    print ("-----------------")
    print ("row_index: ", row_index)
    # print ("row: ", row)
    print ("rsrp0: ", row["rsrp0"])
    rsrplit = []
    for i in range(3):  
        rsrplit.append(row["rsrp" + str(i)])
    print ("rsrplit: ", rsrplit)
    index = np.argmax(np.array(rsrplit))
    value = np.array(rsrplit)[index]
    print (index, value)

    df['sevcell'][row_index] = row["gnodebid"]
    df['sevcellhighestrsrp'][row_index] = value

    rsrplit = []
    for i in range(2):  
        for j in range(2):
            # neb0cellid	neb0gnodebid	neb0ssbid0	neb0rsrp0	neb0ssbid1	neb0rsrp1
            strname = "neb" + str(i) + "rsrp" + str(j)
            print ("strname: ", strname)
            rsrplit.append(i)
            rsrplit.append(j)
            rsrplit.append(row[strname])
            # rsrplit.append(i, j, row[strname])
    print ("rsrplit: \n", rsrplit)
    rsrplit_np = np.array(rsrplit).reshape(-1,3)
    print ("rsrplit_np: \n", rsrplit_np)
        
    index = np.argmax(rsrplit_np, axis=0)
    print ("index: ", index)
    index_i = rsrplit_np[index[2]][0]
    highrsrp = rsrplit_np[index[2], 2]
    print ("index_i: ", index_i)
    nebcellid = row["neb" + str(index_i) + "cellid"]
    nebgnodebid = row["neb" + str(index_i) + "gnodebid"]
    print (nebcellid)
    print (nebgnodebid)

    df['nebhighrsrp'][row_index] = highrsrp
    df['nebhighid'][row_index] = nebgnodebid

df.to_csv("data_process.csv")
    

