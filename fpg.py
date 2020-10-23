import re
import csv
import math
import time
import pandas as pd
from itertools import chain, combinations

def clean_kaggle__data():
    df = pd.read_csv('./kaggle_.csv')
    item_lis = []
    for i in range(len(df)):
        tmp = set()
        for k in df.iloc[i]:
            strr = k.split(',')
        for s in strr:
            tmp.add(s)
        item_lis.append(tmp)
    return item_lis

def clean_data(): #clean the data generate by IBM #data_10^4trans
    #print(item_set)# The list of set of each transaction
    #print(len(item_set))# The number of all transaction
    df = pd.read_csv('./AR.csv')
    df['transaction'] = ""
    df['item'] = ""
    df.rename(columns={"Col":"tmp"}, inplace = True)

    for i in range(df.shape[0]):
        tmp = df["tmp"][i].split()
        df['transaction'][i] = tmp[1]
        df['item'][i] = tmp[2]

    df.drop(["tmp"], inplace = True, axis = 1)

    items = df.groupby("transaction")  #print(items.groups) #0-962 kinds of items appear in which transaction
    item_dict = items.groups
    item_set = []

    for key in item_dict:
        tmp = set()
        for i in list(item_dict[key]): # The item exist in the transaction
            item = df['item'][i]
            tmp.add(item) # The list of item of #key transaction
        item_set.append(tmp)

    return item_set

def ele_in_seq(tran_lis, trans_num, min_sup):
    re_dict = {}

    for ele_ in tran_lis:
        for ele in ele_:
            if (str(ele) in re_dict):
                re_dict[str(ele )]  = (re_dict[str(ele)]+1)
            else:
                re_dict[str(ele )] = (1)

    for key in re_dict:
        if(float(re_dict[key] / trans_num) < min_sup):
            re_dict.pop(key)
    #sorted(re_dict.items(), key = lambda x : x[1])
    return re_dict

def ele_in_trans_in_seq(tran_lis, feq_dict):
    trans_in_seq = []
    tmp_ = []
    sor_dict = {}
    tmp_dict = {}
    for tran in tran_lis: #type(tran) = set
        for e in tran:
            for set_ in feq_dict:
                if(e == set_):
                    tmp_dict[str(e)] = feq_dict[set_]
                    break
        sor_dict[str(tran)] = (tmp_dict)
        tmp_dict = {}

    for key in sor_dict:
        tmp = sorted(sor_dict[key].items(), key = lambda x : x[1])
        for i in range(len(tmp)):
            tmp_.append(tmp[i][0])
        trans_in_seq.append(tmp_)
        tmp_ = []
    return trans_in_seq
class FPTree(object):
    def __init__(self):
        self._root = FPNode(self, None, None)#The root of fptree is null

class FPNode(object):
    def __init__(self, tree, item, num = 1):
        self._tree = tree
        self._item = item #The item put in the node
        self._num = num #The number of item appears in the whole transaction

if __name__ == "__main__":
    #First get freq ele  (check)
    #Second sort the transaction by the decreasing order of the freq ele (check)
    #for every trans:
    #   for every ele in trans:
    #       put the item_name and add the conut of the item
    min_sup = 0.1
    min_conf = 0.75
    tran_lis = clean_kaggle__data()
    feq_dict = ele_in_seq(tran_lis, len(tran_lis), min_sup)
    print(feq_dict)
    trans_in_seq = ele_in_trans_in_seq(tran_lis, feq_dict)
    print(trans_in_seq)