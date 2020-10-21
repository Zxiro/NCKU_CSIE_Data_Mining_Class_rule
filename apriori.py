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
    df = pd.read_csv('./data_ntrans_1_tlen_5_nitems_1.csv')
    df['transaction'] = ""
    df['item'] = ""
    df.rename(columns={"         1          1         42":"tmp"}, inplace = True)
    df["tmp"][0] = "         1          1         42"

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

def get_freq_set(set_, trans_num, min_sup, length):
    l = 1
    set_dict = {}
    for set__ in set_: #list of set
        for ele in combinations(set__, l):
            if len(ele) !=0:
                ele_ = set((ele))
                if (str(ele_ ) in set_dict):
                    set_dict[str(ele_ )]  = (set_dict[str(ele_ )][0], set_dict[str(ele_ )][1]+1)
                else:
                    set_dict[str(ele_ )] = (ele_, 1)
            else: break
    l += 1
    set_dict = check_fit_min_sup(set_dict, min_sup, trans_num)

    while l <= length:
        _set = set()
        for key in set_dict:
            for e in set_dict[key][0]:
                _set.add(e)
        set_dict = {}
        tmp_set = list(combinations(_set, l))
        for e in range(len(tmp_set)):
            s = set()
            for k in range(len(tmp_set[e])):
                s.add(tmp_set[e][k])
            tmp_set[e] = s
       
        for i in range(trans_num):
            for s in tmp_set:
                if(s & set_[i] == s):
                    if (str(s) in set_dict):
                        set_dict[str(s)]  = (set_dict[str(s)][0], set_dict[str(s)][1]+1)
                    else:
                        set_dict[str(s)] = (s, 1)

        if l == length:
            if len(check_fit_min_sup(set_dict, min_sup, trans_num)) == 0:
                print("Doesn't exist!")
                return {}
            return set_dict
        
        set_dict = check_fit_min_sup(set_dict, min_sup, trans_num)
        if (len(set_dict)==0):
            print("Doesn't exist!")
            return {}
        print("Into next length")
        l +=1
    
def check_fit_min_sup(dict_, min_sup, trans_num):
    for key in list(dict_):
        if(float(dict_[key][1] / trans_num) < min_sup):
            dict_.pop(key)
    return dict_

    
if __name__ == "__main__":
    k_ans = {}
    i_ans = {}
    item_set = clean_data()
    k_item_set = clean_kaggle__data()
    k_ans = get_freq_set(k_item_set, len(k_item_set), 0.01, 4)
    print(len(k_ans.keys()), k_ans.keys())
    i_ans = get_freq_set(item_set, len(item_set), 0.004, 2)
    print(k_ans.keys(), i_ans.keys())