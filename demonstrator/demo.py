#!/usr/bin/env python3

from flask import Flask, request, render_template, send_file
import os
import re
from collections import defaultdict
from werkzeug.utils import secure_filename
import threading, webbrowser
import logging
import numpy as np
import matplotlib.pyplot as plt
from gensim import corpora, models, similarities
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from io import BytesIO


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('files')
    documents = []
    labels = []
    texts = []
    for f in files:
        document = f.readlines()
        documents.append(str(document))
        labels.append(secure_filename(f.filename))
    labels = [x.split('.')[0] for x in labels]
    regex = re.compile('\w+')
    for document in documents:
        text = regex.findall(document.lower())
        texts.append(text)

    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    texts = [[token for token in text if frequency[token] > 1] for text in texts]

    stoplist = request.files['stoplist']
    stoplist = str(stoplist.readlines())
    stoplist = regex.findall(stoplist)
    stoplist = set(stoplist)
    texts = [[word for word in text if word not in stoplist]
             for text in texts]

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    model = models.LdaModel(corpus, id2word=dictionary, num_topics=10, passes=10)

    topic_labels = []
    for i in range(10):
        terms = [x[0] for x in model.show_topic(i, topn=3)]
        topic_labels.append(" ".join(terms))

    no_of_docs = len(documents)
    doc_topic = np.zeros((no_of_docs, 10))
    for doc, i in zip(corpus, range(no_of_docs)):
        topic_dist = model.__getitem__(doc)
        for topic in topic_dist:
            doc_topic[i][topic[0]] = topic[1]

    no_of_topics = len(labels)
    if no_of_topics > 20:
        plt.figure(figsize=(20, 20))
    plt.pcolor(doc_topic, norm=None, cmap='Reds')
    plt.yticks(np.arange(doc_topic.shape[0])+1.0, labels)
    plt.xticks(np.arange(doc_topic.shape[1])+0.5, topic_labels, rotation='90')
    plt.gca().invert_yaxis()
    plt.colorbar(cmap='Reds')
    plt.tight_layout()
    plt.savefig("./static/congrats.svg")
    return render_template('success.html')

if __name__ == '__main__':
    threading.Timer(1.25, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    app.debug = True
    app.run()
