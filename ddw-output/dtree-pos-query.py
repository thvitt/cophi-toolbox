#!/usr/bin/env python

import pandas as pd



# ausgabe eines token anhand seiner id
def get_token(df, tokenid):
    return df[df['TokenId'] == int(tokenid)]



# ausgabe aller dependency-tree-children, tokenid = id of parent
def get_children(df, tokenid):
    return df[df['DependencyHead'] == str(tokenid)]



# nur children mit bestimmtem postag ausgeben, tokenid = id of parent
def get_children_pos(df, tokenid, postag):
    df = df[df['DependencyHead'] == str(tokenid)]
    return df[df['CPOS'] == postag]



# checkt ob tokenid (= id of parent) -> je child mit postag1 -> child mit postag2
def walk_tree_pos2(df, tokenid, postag1, postag2):
    result = {}

    ch1 = get_children_pos(df, tokenid, postag1)                 # given tokenid, get children matching postag1

    for index, child1 in ch1.iterrows():                         # for each of those
        ch2 = get_children_pos(df, child1['TokenId'], postag2)   # get children matching postag2

        if not ch2.empty:
            for index, child2 in ch2.iterrows():
                result[child1['TokenId']] = child2      # also return id of corresponding head noun

            return result
    return None



# checkt ob tokenid -> je child mit postag1 -> je child mit postag2 -> child mit postag3
def walk_tree_pos3(df, tokenid, postag1, postag2, postag3):
    result = {}

    ch1 = get_children_pos(df, tokenid, postag1)                 # given tokenid, get children matching postag1

    for index, child1 in ch1.iterrows():                         # for each of those
        ch2 = get_children_pos(df, child1['TokenId'], postag2)   # get children matching postag2

        if not ch2.empty:
            for index, child2 in ch2.iterrows():
                ch3 = get_children_pos(df, child2['TokenId'], postag3)

                if not ch3.empty:
                    for index, child3 in ch3.iterrows():
                        result[child1['TokenId']] = child3      # also return id of corresponding head noun

                    return result
    return None
