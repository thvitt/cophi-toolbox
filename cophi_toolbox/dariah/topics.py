"""
__author__ = "DARIAH"
__authors__ = "Steffen Pielstroem"
__email__ = "pielstroem@biozentrum.uni-wuerzburg.de"
__license__ = ""
__version__ = ""
__date__ = = ""
"""

################################################################################
# Load all dependencies
################################################################################

import glob
import os
import re
from collections import defaultdict


################################################################################
# Corpus ingestion
################################################################################

def readCorpus(path):
	"""
	__author__ = "DARIAH"
	__authors__ = "Steffen Pielstroem"
	__email__ = "pielstroem@biozentrum.uni-wuerzburg.de"

	Read corpus into a list of lists and return the list.
	
	Key argument:
	path (string)
	"""
    files = glob.glob(path)
    documents = []
    for file in files:
        document = open(file)
        document = document.read()
        documents.append(document)
    return documents

def docLabels(path):
	"""
	__author__ = "DARIAH"
	__authors__ = "Steffen Pielstroem"
	__email__ = "pielstroem@biozentrum.uni-wuerzburg.de"

	Create and return a list of document labels from file names.
	"""
    labels = [os.path.basename(x) for x in glob.glob(path)]
    labels = [x.split('.')[0] for x in labels]
    return labels

################################################################################
# Preprocessing
################################################################################

def tokenize(documents):
	"""
	__author__ = "DARIAH"
	__authors__ = "Steffen Pielstroem"
	__email__ = "pielstroem@biozentrum.uni-wuerzburg.de"

	Tokenize and return text.
	"""
    # define regular expression for tokenization
    myRegEx = re.compile('\w+') # compile regex for fast repetition
    texts = []
    for document in documents:
        text = myRegEx.findall(document.lower())
        texts.append(text)
    # Version from Gensim-Tutorial: whithout regex
    #texts = [[word for word in document.lower().split()]
    #         for document in documents]
    return texts

def removeHapaxLeg(texts):
	"""
	__author__ = "DARIAH"
	__authors__ = "Steffen Pielstroem"
	__email__ = "pielstroem@biozentrum.uni-wuerzburg.de"

	Remove hapax legomena and return text.
	"""
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    texts = [[token for token in text if frequency[token] > 1]
            for text in texts]
    return texts

def removeStopWords(texts, stoplist):
	"""
	__author__ = "DARIAH"
	__authors__ = "Steffen Pielstroem"
	__email__ = "pielstroem@biozentrum.uni-wuerzburg.de"

	Remove stopwords according to stopword list and return text.
	"""
    if isinstance(stoplist, str):
        file = open('./helpful_stuff/stopwords/' + stoplist)
        stoplist = file.read()
        stoplist = [word for word in stoplist.split()]
        stoplist = set(stoplist)
    texts = [[word for word in text if word not in stoplist]
             for text in texts]
    return texts

