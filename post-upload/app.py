
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb+srv://test:1234@cluster0.sh1ym.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta_plus_week1

from datetime import datetime

@app.route('/')
def home():
    return render_template('post_upload.html')

@app.route('/main')
def main():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    diaries = list(db.diary.find({}, {'_id': False}))
    return jsonify({'all_diary': diaries})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    scope_receive = request.form['scope_give']
    address_receive = request.form['address_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'title':title_receive,
        'content':content_receive,
        'scope':scope_receive,
        'address':address_receive,
        'file': f'{filename}.{extension}',
        'time': today.strftime('%Y.%m.%d')
    }

    db.diary.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})+home()

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)