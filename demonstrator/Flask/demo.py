from flask import Flask, request, render_template
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('minimal.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_files = request.files.getlist('files')
    documents = []
    for x in uploaded_files:
        document = x.read()
        documents.append(str(document))
    myRegEx = re.compile('\w+')  # compile regex for fast repetition
    texts = []
    for document in documents:
        text = myRegEx.findall(document.lower())
        texts.append(text)
    print(texts)
    return 'success'

if __name__ == '__main__':
    app.run()
