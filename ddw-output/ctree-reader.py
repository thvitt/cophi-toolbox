#!/usr/bin/env python

import pandas as pd
from nltk.tree import ParentedTree

"""
from: http://conll.cemantix.org/2012/data.html
    "This is the bracketed structure broken before the first open parenthesis in the parse,
    and the word/part-of-speech leaf replaced with a *. The full parse can be created by
    substituting the asterix with the "([pos] [word])" string (or leaf) and concatenating
    the items in the rows of that column."
"""
"""
alle noun phrases inkl. pos-tags auslesen
-> mit nltk.tree.Tree und mapping zurück ins dataframe: satzweise die bäume wieder zusammensetzen als (LABEL TOKEN#TOKID)
https://stackoverflow.com/questions/25815002/nltk-tree-data-structure-finding-a-node-its-parent-or-children
https://stackoverflow.com/questions/14841997/how-to-navigate-a-nltk-tree-tree
http://www.nltk.org/howto/tree.html
http://nbviewer.ipython.org/github/gmonce/nltk_parsing/blob/master/1.%20NLTK%20Syntax%20Trees.ipynb
http://www.mit.edu/~6.863/spring2011/labs/nltk-tree-pages.pdf
"""

sign = '#'          # token#token_id delimiter for use inside tree objects

df = pd.read_csv("EffiBriestKurz.txt.csv", sep="\t")
sent_max = df["SentenceId"].max()
trees = []


### READER

# construct syntax trees

for sent_id in range(sent_max+1):                                       # iterate through sentences
    sentence = df[df['SentenceId'] == sent_id]                          # return rows corresponding to sent_id
    sent_string = tmp_string = tmp_string2 = ""

    for row in sentence.iterrows():
        tok_id = str(row[0])                                            # current token id
        tok = row[1].get("Token")                                       # current token
        tree_frag = row[1].get("SyntaxTree").strip("*")                 # current syntax tree fragment

        """
        if "*)" in sent_string:                                         # TODO: possible bug in csv tree writer
            if tmp_string:
                tmp_string2 = sent_string.replace("*)", "")             # we ran into "*)" a second time
                sent_string = tmp_string2
            else:
                tmp_string = sent_string.replace("*)", "")
                sent_string = tmp_string
        """

        if tree_frag.startswith("("):                                   # reconstruct tree + save token id
            sent_string += tree_frag + " " + tok + sign + tok_id + " "  # beginning of fragment
        elif not ")" in tree_frag:
            sent_string += tree_frag + " " + tok + sign + tok_id + " "  # middle
        else:                                                           # end
            """
            if tmp_string:                                              # TODO: possible bug in csv tree writer
                sent_string += " " + tok + sign + tok_id + tree_frag + ") "
                tmp_string = ""
            elif tmp_string2:
                sent_string += " " + tok + sign + tok_id + tree_frag + ")) "
                tmp_string2 = ""
            else:
            """
            sent_string += " " + tok + sign + tok_id + tree_frag + " "

    trees.append(sent_string)                                           # save reconstruction


### QUERIES

# query for constituent type

query1 = 'NP'

print("All constituents of type", query1, "+ POS-Tags:\n")

for string in trees:
    tree = ParentedTree.fromstring(string)                              # read string into tree object

    for subtree in tree.subtrees(filter=lambda t: t.label() == query1): # query subtrees
        print(subtree, "\n")

        for leaf in subtree.leaves():
            t, i = leaf.split(sign)                                     # map back to dataframe using token id
            pos = df.iloc[int(i), 9]                                    # and get a pos-tag
            print("{0}: {1} {2}".format(i, t, pos))
        print("\n")


# query for token or token id

query2 = 'Effi'     # '#921'

print("Token", query2, "found in:\n")

for string in trees:
    tree = ParentedTree.fromstring(string)                              # read string into tree object

    for subtree in tree.subtrees():
        for leaf in subtree.leaves():
            if query2 in leaf: print(subtree)                           # subtrees containing query


# visualise a sentence

query3 = 33

tree = ParentedTree.fromstring(trees[query3])
tree.draw()
