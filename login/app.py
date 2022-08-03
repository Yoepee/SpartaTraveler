from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTATRAVELER'

client = MongoClient('mongodb+srv://test:sparta@cluster0.y2pfd99.mongodb.net/?retryWrites=true&w=majority')
db = client.spartatraveler


@app.route('/')
# 자동로그인성공시 GET /favicon.ico HTTP/1.1 404 에러가 발생하는데 아이콘 누락오류라고함 실행에는 지장이없음
# 자동로그인토큰과 24시간동안 발급받은 토큰은 동일한 값과 접근권한을 가진 토큰임
def home():
    # index로 이동
    save_login = request.cookies.get('save_login')
    # 자동로그인쿠키의 이름을 가졌던 토큰을 우선적으로 확인함
    if save_login :
        print('자동로그인 쿠키가 존재함')
        # 토큰 유효성검사
        try:
            payload = jwt.decode(save_login, SECRET_KEY, algorithms='HS256')
            print('자동로그인 토큰복호화성공')
            return render_template('index.html')
        # 토큰의 유효기간이 만료되었다는 에러문구
        except jwt.ExpiredSignatureError:
            print('토큰만료')
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        # 토큰이 유효하지 않다는 에러문구
        except jwt.exceptions.DecodeError:
            print('토큰복호화실패')
            # return jsonify({'result': 'fail', 'msg': "로그인이 필요합니다!"})
            return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
        return render_template('index.html')
    else :
        print('자동로그인 쿠키가 없음')
        token_receive = request.cookies.get('mytoken')
        # 토큰 유효성검사
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms='HS256')
            print('jwt토큰복호화성공')
            return render_template('index.html')
        # 토큰의 유효기간이 만료되었다는 에러문구
        except jwt.ExpiredSignatureError:
            print('토큰만료')
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        # 토큰이 유효하지 않다는 에러문구
        except jwt.exceptions.DecodeError:
            print('토큰복호화실패')
            # return jsonify({'result': 'fail', 'msg': "로그인이 필요합니다!"})
            return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/chk_token')
def chk_token():
    # 토큰 유효성 검사
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template("index.html")
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/signup')
def detail():
    # 회원가입페이지로 이동
    return render_template("signup.html")


@app.route('/login')
def login():
    # 로그인페이지로 이동
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    email_receive = request.form['email_give']
    password_receive = request.form['password_give']

    # 받아온 암호를 복호화
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # 데이터베이스의 정보와 유저이름과 복호화된 암호를 비교
    result = db.users.find_one({'email': email_receive, 'password': pw_hash})

    # 유저를 찾았을 경우
    if result is not None:

        # 페이로드 작성
        payload = {
         'id': result.get('username'),
        # 로그인 하룻동안 유지 (24)
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }

        # 복호화 과정에서 에러가 발생함 수정
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        # jwt생성
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # 생성된 jwt를 반환
        return jsonify({'result': 'success', 'token': token})

    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})



@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    email_receive = request.form['email_give']
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    # 비밀번호 암호화
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # 유저정보 딕셔러니화
    doc = {
        "email" : email_receive,
        "username": username_receive,
        "password": password_hash
    }
    # 데이터베이스에 입력
    db.users.insert_one(doc)

    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dupName', methods=['POST'])
def check_dupName():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    email_receive = request.form['email_give']
    exists = bool(db.users.find_one({"email": email_receive}))
    return jsonify({'result': 'success', 'exists': exists})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)