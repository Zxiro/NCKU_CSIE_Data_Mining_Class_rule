import re
import csv
import math
import time
import pandas as pd
from itertools import chain, combinations

def clean_data(csv): #clean the data generate by IBM #data_10^4trans
    df = pd.read_csv('./'+csv+'.csv')
    df['customer'] = ""
    df['transaction'] = ""
    df['item'] = ""
    df.rename(columns={"         1          1         42":"tmp"}, inplace = True)
    df["tmp"][0] = "         1          1         42"

    for i in range(df.shape[0]):
        tmp = df["tmp"][i].split()
        df['transaction'][i] = tmp[1]
        df['item'][i] = tmp[2]

    df.drop(["tmp"], inplace = True, axis = 1)
    df.to_csv('./clean_data.csv')

def get_set(set_, dict, trans_num):
    l = 1
    set_dict = {}
    for set__ in set_:
        for ele in combinations(set__, l):
            if len(ele) !=0:
                ele_ = set((ele))
                if (str(ele_ ) in set_dict):
                    set_dict[str(ele_ )]  = (set_dict[str(ele_ )][0], set_dict[str(ele_ )][1]+1)
                else:
                    set_dict[str(ele_ )] = (ele_, 1)
            else: break
    l+=1
    set_dict = check_fit_min_sup(set_dict, 0.01, trans_num)
    while l<4:
        tmp_set = set()
        for key in set_dict:
            tmp_set.add((set_dict[key][0].pop()))
        set_dict = {}
        for ele_ in combinations(tmp_set, l): #個數為一的freq_set裡能夠進行L個分組           
            ele = set(list(ele_))
            print(ele)
            if len(ele) !=0:    
                for i in range(len(set_)):
                    if((ele & set_[i]) == (ele)):
                        if (str(ele) in set_dict):
                            set_dict[str(ele)]  = (set_dict[str(ele)][0], set_dict[str(ele)][1]+1)
                        else:
                            set_dict[str(ele)] = (ele, 1)
            else: break   
        print(len(set_dict))
        set_dict = check_fit_min_sup(set_dict, 0.01, trans_num)
        print(len(set_dict))
        print("Into next L")
        time.sleep(5)
        l +=1
    
def check_fit_min_sup(dict_, min_sup, trans_num):
    for key in list(dict_):
        if(dict_[key][1]/trans_num <min_sup):
            dict_.pop(key)
    return dict_

    
if __name__ == "__main__":
    clean_data('data_ntrans_1_tlen_5_nitems_1')
    df = pd.read_csv('./clean_data.csv')
    items = df.groupby("transaction")  #print(items.groups) #0-962 kinds of items appear in which transaction
    item_dict = items.groups
    item_set = []
    for key in item_dict:
        tmp = set()
        for i in list(item_dict[key]): # The item exist in the transaction
            item = df['item'][i]
            tmp.add(item) # The list of item of #key transaction
        item_set.append(tmp)
    get_set(item_set, item_dict, len(item_set))#print(item_set)# The list of set of each transaction
    #print(len(item_set))# The number of all transaction
    