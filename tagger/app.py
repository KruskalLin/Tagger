import os,sys,json,time

from IPython.core import magic
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import nltk
from nltk.tag import *
from flask_cors import CORS


UPLOAD_FOLDER = os.path.curdir + os.path.sep + 'uploads' + os.path.sep
TAG_FOLDER = os.path.curdir + os.path.sep + 'tags' + os.path.sep
ALLOWED_EXTENSIONS = {'txt'}
JAR = './static/stanford-ner.jar'
MODEL = './static/english.conll.4class.distsim.crf.ser.gz'
ner_tagger = StanfordNERTagger(MODEL, JAR, encoding='utf8')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.')[-1].lower() in ALLOWED_EXTENSIONS


def spans(txt, tags):
    offset = 0
    for tag in tags:
        offset = txt.find(tag[0], offset)
        yield tag[0], tag[1], offset, offset+len(tag[0])
        offset += len(tag[0])

def merge_index(lst):
    new_index = []
    for indexs in lst:
        if len(new_index) > 0 and new_index[-1]['end'] + 1 == indexs['start']:
            new_index[-1] = {
                "start": new_index[-1]['start'],
                "end": indexs['end'],
                "word": new_index[-1]['word'] + ' ' + indexs['word']
            }
        else:
            new_index.append(indexs)
    return new_index

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TAG_FOLDER'] = TAG_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app, supports_credentials=True)


@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            json.dumps({'error': 'not file provide', 'code': 400})
        file = request.files['file']
        if file.filename == '':
            json.dumps({'error': 'filename error', 'code': 400})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename).rsplit('.')[0] + '$' + str(int(time.time())) + '.'\
                       + secure_filename(file.filename).rsplit('.')[1]
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            sentence = open(filepath, 'r', encoding='utf8').read()
            tokens = nltk.word_tokenize(sentence)
            print(tokens)
            tags = ner_tagger.tag(tokens)
            tags_index = []
            for tag_tuple in spans(sentence, tags):
                if tag_tuple[1] == 'LOCATION':
                    tags_index.append({
                        "start": tag_tuple[2],
                        "end": tag_tuple[3],
                        "word": tag_tuple[0]
                    })
            tag = {"data": merge_index(tags_index)}
            tagname = os.path.join(app.config['TAG_FOLDER'], filename.rsplit('.')[0] + '.json')
            fp = open(tagname, 'w', encoding='utf8')
            json.dump(tag, fp)
            return json.dumps({'code': 200, 'url': url_for('upload_file', filename=filename)})


@app.route('/getTextList', methods=['GET'])
def get_text_list():
    dir_list = os.listdir(app.config['UPLOAD_FOLDER'])
    return json.dumps({'code': 200, 'list': dir_list})


@app.route('/getTexts', methods=['GET'])
def texts():
    filename = request.args.get('name')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    text = open(filepath, 'r', encoding='utf8').read()
    return text


@app.route('/getTags', methods=['GET'])
def tags():
    filename = request.args.get('name')
    tagname = os.path.join(app.config['TAG_FOLDER'], filename.rsplit('.')[0] + '.json')
    tags = open(tagname, 'r', encoding='utf8').read()
    return tags


@app.route('/saveTags', methods=['POST'])
def save_tags():
    post_json = request.get_data()
    data = json.loads(post_json)
    filename = data['name']
    tags = data['tags']
    tag = {"data": tags}
    tagname = os.path.join(app.config['TAG_FOLDER'], filename.rsplit('.')[0] + '.json')
    fp = open(tagname, 'w', encoding='utf8')
    json.dump(tag, fp)
    return json.dumps({'code': 200})


@app.route('/deleteFile', methods=['GET'])
def delete_file():
    filename = request.args.get('name')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename.rsplit('.')[0] + '.json')):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename.rsplit('.')[0] + '.json'))
    return json.dumps({'code': 200})




if __name__ == '__main__':
    app.run(host='0.0.0.0')
