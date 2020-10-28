import csv
import time
import pandas as pd
from itertools import chain, combinations

def clean_kaggle__data():#clean the data get from Kaggle
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

def get_freq_set(set_, trans_num, min_sup):#This function is going to get the set that fit the min_sup
    l = 1
    set_dict = {}
    freq_dict = {}
    for set__ in set_: #list of set
        for ele in combinations(set__, l): 
            if len(ele) !=0:
                ele_ = set((ele))
                if (str(ele_ ) in set_dict):
                    set_dict[str(ele_ )]  = (set_dict[str(ele_ )][0], set_dict[str(ele_ )][1]+1)
                    freq_dict[str(ele_ )]  = (freq_dict[str(ele_ )][0], freq_dict[str(ele_ )][1]+1)
                else:
                    set_dict[str(ele_ )] = (ele_, 1)
                    freq_dict[str(ele_ )] = (ele_, 1)
            else: break
    l += 1
    set_dict = check_fit_min_sup(set_dict, min_sup, trans_num)
    freq_dict = check_fit_min_sup(freq_dict, min_sup, trans_num)
    while True:
        _set = set()
        for key in set_dict:
            for e in set_dict[key][0]:
                _set.add(e)
        re_dict = set_dict
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
                        freq_dict[str(s)]  = (freq_dict[str(s )][0], freq_dict[str(s)][1]+1)
                    else:
                        set_dict[str(s)] = (s, 1)
                        freq_dict[str(s)] = (s, 1)
        ans_dict = check_fit_min_sup(set_dict, min_sup, trans_num)
        freq_dict = check_fit_min_sup(freq_dict, min_sup, trans_num)
        if (len(ans_dict)==0):
            return freq_dict
        l +=1
    
def check_fit_min_sup(dict_, min_sup, trans_num):
    for key in list(dict_):
        if(float(dict_[key][1]) < min_sup):
            dict_.pop(key)
    return dict_

def get_rule_with_conf(freq_set, min_conf):
    #for every freq set :
    #   for every possible set in each freq set without the set itself
    #          the possbilty = (the times / trans_num) of freq set / the times/ trans_num of the possible set
    #           if the possbilty > min_conf:
    #               rule get
    c = 0
    s = set()
    subtra = set()
    rul_dict = {}
    tt = []
    for fs in freq_set: #for all freq set
        #print(fs)
        if len(freq_set[fs][0]) > 1 :
            for l in range(1, len(freq_set[fs][0])): 
                tmp_set = combinations(freq_set[fs][0], l)#all possible set of that set
                for i in tmp_set:
                    for k in range(len(i)):
                        s.add(i[k])
                    if len(s) >= len(freq_set[fs][0]):
                        subtra = s - freq_set[fs][0]
                    else:
                        subtra = freq_set[fs][0] - s
                    
                    for key in freq_set:
                        if len(freq_set[key][0] - subtra) == 0 :
                            #print( "s:", s, "sub:", subtra,"sub_num:", freq_set[key][1], "freq_set:",  freq_set[fs][0], "freq_num: ", freq_set[fs][1])
                            pos = float(freq_set[fs][1] / freq_set[key][1])
                    
                    if (pos >= min_conf):
                        st = str(s) + "->" + str(subtra)
                        tt.append(st)
                        rul_dict[str(s)] = subtra
                    s = set()
                    subtra = set()
    print(sorted(tt))
    exit()
    return rul_dict
    
def get_sup(dict_, sup, trans_num):
    for key in dict_:
        print(dict_[key][0], " : ", float(dict_[key][1]/trans_num))



if __name__ == "__main__":
    k_ans = {}
    i_ans = {}
    min_sup = 2
    min_conf = 0.75
    #item_set = clean_data()
    k_item_set = clean_kaggle__data()
    print("Start_kaggle")
    freq_set= get_freq_set(k_item_set, len(k_item_set), min_sup)
    #get_sup(freq_set, min_sup, len(k_item_set))
    print(len(freq_set))
    ru = get_rule_with_conf(freq_set, min_conf)
    ans = []
    for key in ru:
        tmp = [key, " -> ", ru[key]]
        ans.append(tmp)
    print(ans)
    exit()
    print("With min_sup: ", min_sup ,", min_conf: ", min_conf,  "The ass rule is: ", ans)
    '''print("Start_ibm")
    freq_set= get_freq_set(item_set, len(item_set), min_sup)
    get_sup(freq_set, min_sup, len(item_set))
    ru = get_rule_with_conf(freq_set, min_conf)
    ans = []
    for key in ru:
        tmp = [key, " -> ", ru[key]]
        ans.append(tmp)
    #print("With min_sup: ", min_sup ,", min_conf: ", min_conf,  "The ass rule is: ", ans)'''