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
        df['customer'][i] = tmp[0]
        df['transaction'][i] = tmp[1]
        df['item'][i] = tmp[2]

    df.drop(["tmp"], inplace = True, axis = 1)
    df.to_csv('./clean_data.csv')
def get_set_min_sup(set_, dict):
    num = 0
    set_num = 0
    for key in item_dict:
        item_list = []
        for i in list(item_dict[key]): # The item exist in the transaction
            item = df['item'][i]
            item_list.append(item) # The list of item of #key transaction
        item_set = set(item_list)
        if( len(set_ & item_set ) >= len(set_)):
            num+=1
        for l in range(len(item_list)+1):
            if l > 0:
                for ele in combinations(item_list, l):
                    #print(ele)
                    set_num += 1
        print(key, set_num)
    print(num)
    print(set_num) #set_num = 400832


    
if __name__ == "__main__":
    clean_data('data_ntrans_1_tlen_5_nitems_1')
    df = pd.read_csv('./clean_data.csv')
    df.drop(['customer'], axis = 1, inplace = True)
    items = df.groupby("transaction")
    #print(items.groups) #0-962 kinds of items appear in which transaction
    item_dict = items.groups
    get_set_min_sup({420}, item_dict)