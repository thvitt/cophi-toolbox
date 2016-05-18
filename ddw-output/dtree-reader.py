#!/usr/bin/env python

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

"""
aus den dependency relations einen graph bauen
- satzweise, für jedes token: ein edge aus tok_id:DependencyHead
- labels: tokens für nodes, DependencyRelation für edges
- edges: vgl. http://www.coli.uni-saarland.de/projects/sfb378/negra-corpus/kanten.html

http://guitarpenguin.is-programmer.com/posts/44818.html
https://networkx.github.io/documentation/latest/reference/drawing.html
https://networkx.github.io/documentation/latest/reference/functions.html
http://networkx.lanl.gov/reference/classes.digraph.html
"""

df = pd.read_csv("EffiBriestKurz.txt.csv", sep="\t")
sent_max = df["SentenceId"].max()
trees = []


### READER

# construct dependency trees

for sent_id in range(sent_max+1):                           # iterate through sentences
    sentence = df[df['SentenceId'] == sent_id]              # return rows corresponding to sent_id

    dg = nx.DiGraph()                                       # a new directed graph

    for row in sentence.iterrows():
        tok_id = str(row[0])                                # current token id
        tok = row[1].get("Token")                           # current token
        head_id = row[1].get("DependencyHead")              # token head id
        rel = row[1].get("DependencyRelation")              # dependency relation

        if head_id.isdigit() == True:
            head = df.iloc[int(head_id), 6]                 # get head token
        else:
            head = "ROOT"                                   # or mark as root

        dg.add_node(tok, id=tok_id)                         # save token id as node attribute
        dg.add_node(head, id=head_id)
        dg.add_edge(head, tok, rel=rel)                     # add edge to graph

    trees.append(dg)                                        # save digraph


### QUERIES

# query for relation type

query1 = 'NK'

print("All edges of type", query1, ":\n")

for tree in trees:
    rel = dict([((u, v), d['rel']) for u, v, d in tree.edges(data=True)])

    for nodes, r in rel.items():
        if r == query1:
            print(r, nodes)

print("\n")


# query for token id

query2 = 921

for tree in trees:
    id = dict([(u, d['id']) for u, d in tree.nodes(data=True)])

    for token, i in id.items():
        if i == str(query2):
            print("Token", i, ":", token)
            print(nx.info(tree, token))

print("\n")


# query for token

query2 = "von"

for tree in trees:
    id = dict([(u, d['id']) for u, d in tree.nodes(data=True)])

    for token, i in id.items():
        if token == query2:
            print("Token", i, ":", token)
            print(nx.info(tree, token))

print("\n")


# visualise a sentence

query3 = 33

dg = trees[query3]
print("Dependency Tree for Sentence", query3, ":")
print(nx.info(dg))
print("Token IDs:", nx.get_node_attributes(dg, 'id'))       # mapping back into dataframe

pos = nx.spectral_layout(dg)
edge_labels = dict([((u, v), d['rel']) for u, v, d in dg.edges(data=True)])
nx.draw_networkx_edge_labels(dg, pos, edge_labels=edge_labels)
nx.draw_networkx(dg, pos, with_labels=True)

plt.axis('off')
plt.show()
