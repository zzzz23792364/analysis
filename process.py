


import pandas as pd
import numpy as np 
import os 
from pandas import DataFrame,Series
import re
from bisect import bisect_left


# df = pd.read_csv(r'/mnt/e/analasy/data.csv', encoding='unicode_escape')
# df = pd.read_csv(r'/mnt/e/analasy/data.csv')

# print(df.columns)  #查看列名
# # print(df.dtypes) 

# for row_index, row in df.iterrows():
#     print ("-----------------")
#     print ("row_index: ", row_index)
#     # print ("row: ", row)
#     print ("rsrp0: ", row["rsrp0"])
#     rsrplit = []
#     for i in range(3):  
#         rsrplit.append(row["rsrp" + str(i)])
#     print ("rsrplit: ", rsrplit)
#     index = np.argmax(np.array(rsrplit))
#     value = np.array(rsrplit)[index]
#     print (index, value)

#     df['sevcell'][row_index] = row["gnodebid"]
#     df['sevcellhighestrsrp'][row_index] = value

#     rsrplit = []
#     for i in range(2):  
#         for j in range(2):
#             # neb0cellid	neb0gnodebid	neb0ssbid0	neb0rsrp0	neb0ssbid1	neb0rsrp1
#             strname = "neb" + str(i) + "rsrp" + str(j)
#             print ("strname: ", strname)
#             rsrplit.append(i)
#             rsrplit.append(j)
#             rsrplit.append(row[strname])
#             # rsrplit.append(i, j, row[strname])
#     print ("rsrplit: \n", rsrplit)
#     rsrplit_np = np.array(rsrplit).reshape(-1,3)
#     print ("rsrplit_np: \n", rsrplit_np)
        
#     index = np.argmax(rsrplit_np, axis=0)
#     print ("index: ", index)
#     index_i = rsrplit_np[index[2]][0]
#     highrsrp = rsrplit_np[index[2], 2]
#     print ("index_i: ", index_i)
#     nebcellid = row["neb" + str(index_i) + "cellid"]
#     nebgnodebid = row["neb" + str(index_i) + "gnodebid"]
#     print (nebcellid)
#     print (nebgnodebid)

#     df['nebhighrsrp'][row_index] = highrsrp
#     df['nebhighid'][row_index] = nebgnodebid

# df.to_csv("data_process.csv")

lkres = dict()

class Infos:
    def __init__(self, vol):
       self.vol = vol

class Property:
   def __init__(self):
      self.timestamp_list = []
      self.timestamp_map = dict()

def TransferTime(day, hour, min, s, ms):
    return day * 24 * 60 * 60 * 1000 + hour * 60 * 60 * 1000 + min * 60 * 1000 + s * 1000 + ms

def Lookup():
    # lkres = dict()
    lk = pd.read_csv(r'/mnt/e/analasy/look.csv')
    for row_index, row in lk.iterrows():
        day = row["day"]
        hour = row["hour"]
        min = row["min"]
        s = row["s"]
        ms = row["ms"]
        callid = row["callid"]
        vol = row["vol"]
        timestamp = TransferTime(day, hour, min, s, ms)
        print ("-----------------")
        print ("row_index: ", row_index)
        print (timestamp)
        if callid in lkres:
            # print("111")
            lkres[callid].timestamp_list.append(timestamp)
            info = Infos(row["vol"])
            lkres[callid].timestamp_map[timestamp] = info
        else:
            # print("222")
            t = Property()
            t.timestamp_list.append(timestamp)
            info = Infos(row["vol"])
            t.timestamp_map[timestamp] = info
            lkres[callid] = t

    for value in lkres.values():
        value.timestamp_list.sort()
    # return lkres

def TakeClosest(myList, myNumber):
    if (myNumber >= myList[-1]):
        return myList[-1]
    elif myNumber <= myList[0]:
        return myList[0]
    pos = bisect_left(myList, myNumber)
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before

def SetProperty():
    df = pd.read_csv(r'/mnt/e/analasy/data.csv')
    for row_index, row in df.iterrows():
        print ("++++++++++++++++++++++++++")
        # print ("row_index: ", row_index)
        day = row["day"]
        hour = row["hour"]
        min = row["min"]
        s = row["s"]
        ms = row["ms"]
        callid = row["callid"]
        timestamp = TransferTime(day, hour, min, s, ms)
        print('SetProperty ts = ', timestamp)
        if callid in lkres:
            # position = bisect.bisect(lkres[callid].timestamp_list, timestamp)
            ts = TakeClosest(lkres[callid].timestamp_list, timestamp)
            # print(position)
            # ts = lkres[callid].timestamp_list[position - 1]
            print(ts)
            infos = lkres[callid].timestamp_map[ts]
            df['overlap_flag'][row_index] = infos.vol
        else:
            df['overlap_flag'][row_index] = -1 # default invalid value
    df.to_csv("data_process.csv")


if __name__ == "__main__":
    # lkres = Lookup()
    Lookup()
    SetProperty()

    # debug
    for k, v in lkres.items():
        print(k)
        print(v.timestamp_list)
        print(v.timestamp_map)
    

