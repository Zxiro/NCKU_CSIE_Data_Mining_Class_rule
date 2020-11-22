# -*- coding: utf-8 -*-
'''Set absolute right rule -> key to pass the graduate exam
[al, la, os, ds, sw, dm, ca, st, tc, fi, ci, en, em, fs, ch, ce, jp, aj, bs, ck, dv, ec, f, ge, hy]
'''
import numpy as np
import pandas as pd
import statistics as stat
from sklearn import tree, metrics, svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

#feature_list with 25 features
feature_list = ['al', 'la', 'os', 'ds', 'sw', 'dm', 'ca', 'st', 'tc', 'fi', 'ci',
                'en', 'em', 'fs', 'ch', 'ce', 'jp', 'aj', 'bs', 'ck', 'dv', 'ec', 'fj', 'ge', 'hy']

def generate_data(fea_list): #Generate the data with 25 attrs
    tmp = []  
    ans_list = []
    for i in range(10000): #student data
        te = np.random.randint(1, 7, 25)
        tmp.append(list(te))
    stud_data = pd.DataFrame(np.row_stack(tmp), columns = feature_list)
    #print(stud_data)
    for ind in stud_data.index:
        if (stud_data.iloc[ind]['ds'] >= 4 and 
            stud_data.iloc[ind]['la'] >= 4 and  
            stud_data.iloc[ind]['fs'] >= 2 and
            (stud_data.iloc[ind]['ds'] + stud_data.iloc[ind]['la'])/2 >= 4.5 and
            (stud_data.iloc[ind]['la'] > stud_data.iloc[ind]['dm']) and
            (np.mean(stud_data.iloc[ind]))>=3.5 and
            stat.stdev(stud_data.iloc[ind])<=1.6 and
            stud_data.iloc[ind]['ch'] >= 1):
            ans_list.append(1)
        else:
            ans_list.append(0)
    return stud_data, ans_list

def run_dec(tr_x, tr_y, te_x, te_y): #does not seperate the useless feas
    clf = DecisionTreeClassifier()
    gen_clf = clf.fit(tr_x, tr_y)
    text_representation = tree.export_text(gen_clf)
    print(text_representation)
    
    fig = plt.figure(figsize=(125,100))
    _ = tree.plot_tree(clf, 
                       feature_names=feature_list,  
                       class_names = ['F', 'P'],
                       filled=True)
    fig.savefig("decistion_tree.png")
    
    test_y_predicted = gen_clf.predict(te_x)
    accuracy = metrics.accuracy_score(te_y, test_y_predicted)
    print("dec_tree_Acc : ", float(accuracy*100), " % ")

def run_svm(tr_x, tr_y, te_x, te_y):
    svc = svm.SVC(kernel=('rbf'))
    svc.fit(tr_x, tr_y)
    accuracy = svc.score(te_x, te_y)/svc.score(tr_x, tr_y)
    print("svm_Acc : ", float(accuracy*100), " % ")

def run_pla(tr_x, tr_y, te_x, te_y):
    per_clf = Perceptron(tol = 1e-3, random_state = 0, fit_intercept=(True))
    per_clf.fit(tr_x, tr_y)
    print("pla_Acc : ", float(per_clf.score(te_x, te_y))*100, " % ")  
    


def print_decision_rules(rf):

    for tree_idx, est in enumerate(rf.estimators_):
        tree = est.tree_
        assert tree.value.shape[1] == 1 # no support for multi-output

        print('TREE: {}'.format(tree_idx))

        iterator = enumerate(zip(tree.children_left, tree.children_right, tree.feature, tree.threshold, tree.value))
        for node_idx, data in iterator:
            left, right, feature, th, value = data

            # left: index of left child (if any)
            # right: index of right child (if any)
            # feature: index of the feature to check
            # th: the threshold to compare against
            # value: values associated with classes            

            # for classifier, value is 0 except the index of the class to return
            class_idx = np.argmax(value[0])

            if left == -1 and right == -1:
                print('{} LEAF: return class={}'.format(node_idx, class_idx))
            else:
                print('{} NODE: if feature[{}] < {} then next={} else next={}'.format(node_idx, feature, th, left, right))  

    
def run_ran(tr_x, tr_y, te_x, te_y):
    ran_clf = RandomForestClassifier(n_estimators = 100, max_depth=(5), random_state=(0))
    ran_clf.fit(tr_x, tr_y)
    #print_decision_rules(ran_clf)
    pred_y = ran_clf.predict(te_x)
    accuracy = metrics.accuracy_score(te_y, pred_y)
    print("ran_tree_Acc : ", float(accuracy*100), " % ")

if __name__ == "__main__":
    for i in range(5):
        x, y = generate_data(feature_list)
        
        tr_x, te_x, tr_y, te_y = train_test_split(x, y, test_size = 0.3)
    
        run_dec(tr_x, tr_y, te_x, te_y)
        run_ran(tr_x, tr_y, te_x, te_y)
        run_svm(tr_x, tr_y, te_x, te_y)
        run_pla(tr_x, tr_y, te_x, te_y)
    



