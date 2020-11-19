# -*- coding: utf-8 -*-
'''Set absolute right rule -> key to pass the graduate exam
[al, la, os, ds, sw, dm, ca, st, tc, fi, ci, en, em, fs, ch, ce, jp, aj, bs, ck, dv, econ, f, ge, hy]
'''
import os
import numpy as np
import pandas as pd
from sklearn import tree
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz 2.44.1/bin/'


#feature_list with 25 features
feature_list = ['al', 'la', 'os', 'ds', 'sw', 'dm', 'ca', 'st', 'tc', 'fi', 'ci',
                'en', 'em', 'fs', 'ch', 'ce', 'jp', 'aj', 'bs', 'ck', 'dv', 'ec', 'fj', 'ge', 'hy']

def generate_data(fea_list): #Generate the data with 25 attrs
    tmp = []  
    ans_list = []
    for i in range(5000): #500 student data
        te = np.random.randint(1, 7, 25)
        tmp.append(list(te))
    stud_data = pd.DataFrame(np.row_stack(tmp), columns = feature_list)
    print(stud_data)
    for ind in stud_data.index:
        if (stud_data.iloc[ind]['ds'] >= 4 and 
            stud_data.iloc[ind]['la'] >= 4 and  
            stud_data.iloc[ind]['fs'] >= 2 and
            (stud_data.iloc[ind]['ds'] + stud_data.iloc[ind]['la'])/2 >= 4.5 and
            (stud_data.iloc[ind]['la'] > stud_data.iloc[ind]['dm']) and
            (np.mean(stud_data.iloc[ind]))>=3.5 and
            stud_data.iloc[ind]['ch'] >= 1):
            ans_list.append(1)
        else:
            ans_list.append(0)
    #print(ans_list)
    return stud_data, ans_list

x, y = generate_data(feature_list)

tr_x, te_x, tr_y, te_y = train_test_split(x, y, test_size = 0.3)

#Build Classifer
clf = tree.DecisionTreeClassifier()
gen_clf = clf.fit(tr_x, tr_y)
text_representation = tree.export_text(gen_clf)
print(text_representation)
#print(getmembers(gen_clf.tree_))
fig = plt.figure(figsize=(25,20))
_ = tree.plot_tree(clf, 
                   feature_names=feature_list,  
                   class_names = ['G', 'T'],
                   filled=True)
fig.savefig("decistion_tree.png")

#Predict
test_y_predicted = gen_clf.predict(te_x)

#Accuracy
accuracy = metrics.accuracy_score(te_y, test_y_predicted)
print("Acc : ", float(accuracy*100), " % ")
