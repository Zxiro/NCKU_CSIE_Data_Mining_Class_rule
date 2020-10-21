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

def fit_min_sup(lis):
    re_dict = {}
    for ele_ in lis:
        for ele in ele_:
            if (str(ele) in re_dict):
                re_dict[str(ele )]  = (re_dict[str(ele)][0], re_dict[str(ele )][1]+1)
            else:
                re_dict[str(ele )] = (ele, 1)
    return re_dict

if __name__ == "__main__":
    lis = clean_kaggle__data()
    seq_lis = fit_min_sup(lis)
    print(seq_lis)