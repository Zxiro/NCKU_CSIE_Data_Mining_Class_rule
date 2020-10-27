import csv
import time
import pandas as pd
import numpy as np
from itertools import chain, combinations
from collections import namedtuple, OrderedDict 

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
        if(re_dict[key] < min_sup):
            re_dict.pop(key)
    return re_dict

def ele_in_trans_in_seq(tran_lis, feq_dict):
    trans_in_seq = []
    tmp_ = []
    sor_dict = []
    tmp_dict = {}
    for tran in tran_lis: #type(tran) = set
        for e in tran:
            for set_ in feq_dict:
                if(e == set_):
                    tmp_dict[str(e)] = feq_dict[set_] #出現次數
                    break
        #sor_dict[str(tran)] = (tmp_dict)
        sor_dict.append(tmp_dict)
        tmp_dict = {}
    for set_ in sor_dict:
        r = sorted(sorted(set_.items(), key = lambda i : i) ,key = lambda k : k[1], reverse = True)
        for i in r:
            tmp_.append(i[0])
        trans_in_seq.append(tmp_)
        tmp_ = []

    return trans_in_seq


def get_freq_item(tree, tran_lis):
    # for item in tree:
    #   generate all paths that contain the item
    #   if the sup of that path >= min_sup:
    #    get the sup of that path
    for item in tree.items():#Every item in the tree
        print(tree._route[item])
    exit()
    pass



def build_cond_tree(paths):
    cond_tree = FPTree()
    condition_item = None
    items = set()

    # Import the nodes in the paths into the new tree. Only the counts of the
    # leaf notes matter; the remaining counts will be reconstructed from the
    # leaf counts.
    for path in paths: #{B, MA, MI, J}, {B, TE, MA, J}
        if condition_item is None:
            condition_item = path[-1]._item
        #con = JAM
        point = cond_tree.get_root()
        for node in path:
            next_point = point.search(node._item) #check this node's children contains this item or not
            if not next_point:
                items.add(node._item)
                count = node.get_num() if node._item == condition_item else 0
                next_point = FPNode(cond_tree, node._item, count)
                point.add(next_point)
                cond_tree.update_route(next_point)# Tree add B
            point = next_point

    assert condition_item is not None

    # Calculate the counts of the non-leaf nodes.
    for path in cond_tree.get_all_path(condition_item): #B, MA, MI
        count = path[-1].get_num() # 1
        for node in reversed(path[:-1]):
            node._num += count #+=1

    return cond_tree

def find_with_suffix(tree, suffix): #suffix 後綴
        print(tree.items()) #for all item in the tree
        exit()
        for item in tree.items():
            print()
            support = sum(n.count for n in nodes) #這個item 出現幾次
            if support >= min_sup and item not in suffix: #確定是leaf
                # New winner!
                found_set = [item] + suffix #Beer
                yield (found_set, support)
                #(JAM, 2), ([Beer, cold], 2)
                # Build a conditional tree and recursively search for frequent
                # itemsets within it.
                cond_tree = build_cond_tree(tree.get_all_path(item))
                for s in find_with_suffix(cond_tree, found_set):
                    yield s # pass along the good news to our caller

   

'''def conditional_tree_from_paths(paths):
    """Build a conditional FP-tree from the given prefix paths."""
    tree = FPTree()
    condition_item = None
    items = set()

    # Import the nodes in the paths into the new tree. Only the counts of the
    # leaf notes matter; the remaining counts will be reconstructed from the
    # leaf counts.
    for path in paths:{B, MA, MI, J}, {B, TE, MA, J}
        if condition_item is None:
            condition_item = path[-1].item
        #con = JAM
        point = tree.root
        for node in path:
            next_point = point.search(node.item) #check this node's children contains this item or not
            if not next_point:
                # Add a new node to the tree.
                items.add(node.item)
                count = node.count if node.item == condition_item else 0
                next_point = FPNode(tree, node.item, count)
                point.add(next_point)
                tree._update_route(next_point)# Tree add B
            point = next_point

    assert condition_item is not None

    # Calculate the counts of the non-leaf nodes.
    for path in tree.prefix_paths(condition_item): #B, MA, MI
        count = path[-1].count # 1
        for node in reversed(path[:-1]):
            node._count += count #+=1

    return tree'''


class FPTree(object):

    route = namedtuple('Route', 'head tail')

    def __init__(self):
        self._root = FPNode(self, None, None)#The root of fptree is null
        self._route = {}

    def items(self):
        item_lis = {}
        for r in self._route:
            item_lis[r] = self._route[r]
        return item_lis

    def add_trans(self, trans): #Add node into tree
        init_point = self.get_root() # point to the root
        for item in trans:
            next_point = init_point.search(item) #Ensure that node contains a child node of that item or not
            if next_point == None: #If it is a new item 
                next_point = FPNode(self, item) #Init a new node
                init_point.add(next_point) #This node become a child
                self.update_route(next_point) #The route add a new node, so it has to be updated
            else:
                next_point.increase_num()
            init_point = next_point

    def update_route(self, node): #Since it is a new node go into the tree, so the route of the item must be updated
        
        try: #If there exist a route that contains the item of the node, then the tail of the route will be that item and it's neighbor will be it too
            present_route = self._route[node._item]
            present_route[1]._neighbor = node
            self._route[node._item] = self.route(present_route[0], node)
        except KeyError: #New node so the route does not exist and that item will be the head of the route
            self._route[node._item] = self.route(node, node) #The node will be the head and the tail of the route

    def build_freq_dict(self, lis):
        freq_dict = {}
        re_dict = {}
        tmp = []
        concat_tree = FPTree()
        for l in lis: #l for each path
            try:
                for ele in l:
                    if (ele._item in re_dict):
                        re_dict[ele._item]  += ele.get_freq_num()
                    else:
                        re_dict[ele._item] = ele.get_freq_num()
                tmp.append(re_dict)
                re_dict = {}
            except TypeError:
                continue
        print(tmp)
        print(re_dict)
        exit()
        for key in re_dict:
            if re_dict[key]>= min_sup:
                freq_dict[key]  = re_dict[key]
        return freq_dict

    def get_all_path(self, item):
        #print('head', self._route[item][0]._item, self._route[item][0], self._route[item][0].get_num() )
        head = self._route[item][0]
        total_list = []
        while True:
            if(head != None):
                p = self.get_prefix_path(head)
                total_list.append(p)
                head = head.get_neighbor()
            else:
                return total_list

    def get_prefix_path(self, node): #Get the prefix path of given node
        path = []
        path.append(node)
        node = node.get_parent()
        while node != self.get_root() and node != None:
            path.append(node)
            node = node.get_parent()
        path.reverse()
        return path

    def get_root(self):
        return self._root
class FPNode(object):
    def __init__(self, tree, item, num = 1):
        self._tree = tree
        self._item = item #The item put in the node
        self._num = num #The number of item appears in the whole transaction
        self._children = {} #
        self._neighbor = None
        self._parent = None
    
    def add(self, child): #Add child into node
        if not child._item in self._children:
            self._children[child._item] = child
            child._parent = self

    def search(self, item):#Search the item exist or not
        try:
            return self._children[item] 
        except KeyError:
            return None

    def get_tree(self): #Return the tree that this node appears
        return self._tree
    
    def get_num(self): #Return the number of this item appeaers
        if self == None:
            return 0 
        else:
            return self._num
        
    def get_freq_num(self): #Return the number of this item appeaers
        if self == None:
            return 0 
        else:
            return self._freq_num
        
    def get_item(self): #Return the item
        return self._item

    def get_neighbor(self): #Return the neighbor of the node -> neighbor is the same item 
        return self._neighbor

    def get_parent(self):
        return self._parent

    def increase_num(self): #Increase the count of the item appears
        self._num += 1

if __name__ == "__main__":
    min_sup = 2
    min_conf = 0.75
    tran_lis = clean_kaggle__data()#print(tran_lis)
    feq_dict = ele_in_seq(tran_lis, len(tran_lis), min_sup)#print(feq_dict)
    trans_in_seq = ele_in_trans_in_seq(tran_lis, feq_dict)
    print(trans_in_seq)#List of list -> [[A, B, C], [C, D, F]....]
    t = FPTree() #Init FPtree
    for i in range(len(trans_in_seq)):
        t.add_trans(trans_in_seq[i]) #Add transaction into tree
    for ele in sorted(feq_dict.items(), key = lambda s : s[1]):
        build_cond_tree(t.get_all_path(ele[0]))
         # Search for frequent itemsets, and yield the results we find.
        for itemset in find_with_suffix(t, []):
           print(itemset)