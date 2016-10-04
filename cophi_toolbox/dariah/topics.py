#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import re
from collections import defaultdict
import logging


__author__ = "DARIAH-DE"
__authors__ = "Steffen Pielstroem"
__email__ = "pielstroem@biozentrum.uni-wuerzburg.de"
__license__ = ""
__version__ = "0.1"
__date__ = "2016-06-13"

log = logging.getLogger('cophi_toolbox.dariah.topics')
log.addHandler(logging.NullHandler())

# To enable logger, uncomment the following three lines.
#logging.basicConfig(level=logging.INFO,
#                    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
#                    datefmt='%d-%b-%Y %H:%M:%S')

########################################################################
# Corpus ingestion
########################################################################


def readCorpus(path):
    """
    Read corpus into strings.

    Args:
        path (str): Path/glob pattern of the text files to process.

    Author:
        DARIAH-DE
    """

    files = glob.glob(path)
    documents = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as document:
            document = document.read()
            documents.append(document)
    log.info('Ingested corpus successfully.')
    return documents


def docLabels(path):
    """
    Create a list of names (of the files) using paths and return a
    list.

    Args:
        path (str): Path/glob pattern of the text files to process.

    Author:
        DARIAH-DE
    """

    labels = [os.path.basename(x) for x in glob.glob(path)]
    labels = [x.split('.')[0] for x in labels]
    log.info('Created %s doc labels.', len(labels))
    return labels

########################################################################
# Preprocessing
########################################################################


def tokenize(documents):
    """
    Tokenize (means breaking a stream of text up into words) text and
    return in a list of lists.

    Args:
        documents (List[str]): List of lists containing text.

    Todo:
        * Using version from gensim tutorial without regex?
            `texts = [[word for word in document.lower().split()]
                     for document in documents]`

    Author:
        DARIAH-DE
    """

    # define regular expression for tokenization
    myRegEx = re.compile('\w+')  # compile regex for fast repetition
    texts = []
    for document in documents:
        text = myRegEx.findall(document.lower())
        texts.append(text)
    log.info('Successfully tokenized.')
    return texts


def removeHapaxLeg(texts):
    """
    Remove hapax legomena (words that occurs only once within a
    context) and return text.

    Args:
        texts (List[str]): List of lists containing tokens.

    Author:
        DARIAH-DE
    """

    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
        texts = [[token for token in text if frequency[token] > 1]
                 for text in texts]
    log.info('Removed hapax legomena.')
    return texts


def removeStopWords(texts, stoplist):
    """
    Remove stopwords (usually refer to the most common words) according
    to selected stopword list and return text.

    Args:
        texts (List[str]): List of lists containing tokens.
        stoplist (str): Corpus language?

            ``de``
                German
            ``en``
                English
            ``es``
                Spanish
            ``fr``
                French

    Todo:
        * Replace `.helpful_stuff/stopwords/`

    Author:
        DARIAH-DE
    """

    if isinstance(stoplist, str):
        file = open('./helpful_stuff/stopwords/' + stoplist)
        stoplist = file.read()
        stoplist = [word for word in stoplist.split()]
        stoplist = set(stoplist)
    texts = [[word for word in text if word not in stoplist]
             for text in texts]
    log.info('Removed stopwords.')
    return texts
