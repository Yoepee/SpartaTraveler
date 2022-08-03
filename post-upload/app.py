
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:1234@cluster0.sh1ym.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta_plus_week1

from datetime import datetime

from bson.json_util import dumps
from bson.objectid import ObjectId

@app.route('/')
def home():
    return render_template('post_upload.html')

@app.route('/main')
def main():
    return render_template('main_test.html')

#상세페이지를 보여주는 기능
@app.route('/post', methods=['GET'])
def post():
    file_name = request.args.get('file_name_give', False)
    print(file_name)
    return render_template('post.html', value=file_name)

@app.route('/showpost', methods=['POST'])
def show_post():
    file_name = request.form.get('file_name_give', False)
    print(file_name)
    diaries = list(db.diary.find({'file': file_name}))
    print(dumps(diaries))
    return jsonify({'all_diary': dumps(diaries)})

#검색 기능
@app.route('/search', methods=['POST'])
def search_show():
    find_name = request.form.get('find_name_give', False)
    search_name = request.form.get('search_name_give', False)
    print(find_name,search_name)

    diaries = list(db.diary.find({find_name: {'$regex':search_name}}))
    return jsonify({'all_diary': dumps(diaries)})

#데이터베이스에 저장된 게시글을 전송해 main_test.html파일에서 보여줌
@app.route('/view', methods=['GET'])
def show_diary():
    diaries = list(db.diary.find({}, {'_id': False}))
    return jsonify({'all_diary': diaries})

#사용자로부터 게시글 데이터가 들어오면 데이터베이스에 저장
@app.route('/posting', methods=['POST'])
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

    return jsonify({'msg': '저장 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)