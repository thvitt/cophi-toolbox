from flask import Flask, request, render_template
import os
import re
from collections import defaultdict
from werkzeug.utils import secure_filename

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
        document = f.read()
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
    print(texts, labels)
    return 'success'

if __name__ == '__main__':
    app.debug = True
    app.run()
