# jwt의 쿠키만료시간 설정을 위한 함수
import datetime
# 비밀번호를 암호화하기위한 함수 hashlib
import hashlib
# flask 의 기본내장함수들 = render_templaste : html 위치, request = 정보 받아오기, jsonify = 메세지보내기, session = 서버에 session값 등 저장
from flask import *
# pyjwt를 호출
import jwt

from datetime import datetime, timedelta, date

app = Flask(__name__)
# 토큰 생성에 사용될 secret key 를 flask 환경변수에 등록 (session을 사용해도 secret-key는 필요함)
app.config.update(
    DEBUG=True,
    JWT_SECRET_KEY="I`M IML",
    JWT_ACCESS_COOKIE_PATH='/'
)


# 문자열 해싱(암호화) 설정
m = hashlib.sha256()
m.update('This is sparta'.encode('utf-8'))
m.update(', it is very hard'.encode('utf-8'))
# 토큰을 위한 시크릿 키
SECRET_KEY = 'SPARTA'

# 데이터베이스
from pymongo import MongoClient

client = MongoClient('mongodb+srv://Now:rla15923@cluster0.otpdv.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


# 메인페이지
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    # 토큰 유효성검사
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms='HS256')
        user_info = db.users.find_one({'userid': payload['id']})
        return render_template('index.html', id=user_info['userid'])
    # 토큰의 유효기간이 만료되었다는 에러문구
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    # 토큰이 유효하지 않다는 에러문구
    except jwt.exceptions.DecodeError:
        # return jsonify({'result': 'fail', 'msg': "로그인이 필요합니다!"})
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# href='/'사용이 안먹을 때 html파일로 바로 연결되도록 등록
@app.route('/index.html')
def home1():
    return render_template('index.html')


#한칸을 더 내리면 안됨
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


#회원가입 페이지 이동
@app.route('/join')
def join():
    return render_template('join.html')


# href='/'사용이 안먹을 때 html파일로 바로 연결되도록 등록
@app.route('/write')
def home2():
    return render_template('write.html')


# 회원가입
@app.route("/join2", methods=["POST"])
def join_ok():
    # html로 부터 받아오는 변수값 저장
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    password2_receive = request.form['password2_give']

    # 공백이 있는지 유효성검사
    if id_receive == "" or password_receive == "" or password2_receive == "":
        return jsonify({'msg': '작성되지 않은 정보가 있습니다.'})
    else:
        # 중복 아이디가 있는지 유효성 검사
        if (db.users.find_one({'userid': id_receive})) is not None:
            return jsonify({'msg': '중복되는 아이디가 있습니다.'})
        else:
            # 비밀번호는 잘못입력하면 계정을 못쓸 수 있기때문에 1,2를 통해 검사함 (동일한지 유효성검사)
            if password_receive != password2_receive:
                return jsonify({'msg': '비밀번호가 다릅니다.'})
            else:
                # pw 암호화 (hexdigest = 16진수로 암호화)
                pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
                # DB에 저장될 딕셔너리형 자료형으로 대입
                doc = {
                    'userid': id_receive,
                    'password': pw_hash
                }
                # 데이터베이스 저장
                db.users.insert_one(doc)
                return jsonify({'msg': '회원가입 완료'})


# 로그인 되는지 확인하는 함수
@app.route("/login2", methods=["POST"])
def login_ok():
    # html로 부터 받아오는 변수값 저장
    inputid_receive = request.form['inputid_give']
    inputpw_receive = request.form['inputpw_give']

    # join과 동일한 방식으로 pw 암호화
    pw_hash = hashlib.sha256(inputpw_receive.encode('utf-8')).hexdigest()

    # 해당 아이디가 있는지 유효성 검사
    user = db.users.find_one({'userid': inputid_receive})
    # user = db.users.find_one({'userid': inputid_receive, 'password':pw_hash})를 통한 아이디 비밀번호 동시검사 가능
    if user is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        if user['password'] == pw_hash:
            # 세션을 통한 로그인 검사일 시에 session에 id값을 데입하는 예제
            # session['userid'] = request.form['inputid_give']
            # 하루동안 유효한 토큰
            payload = {
                'id': inputid_receive,
                'exp': datetime.utcnow() + timedelta(days=1)
            }
            # jwt를 암호화
            # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            # 로그인 성공, 토큰 전달
            return jsonify({'result': 'success', 'token': token})
        else:
            # 비밀번호가 틀릴 때 출력값
            return jsonify({'result': 'fail', 'msg': '비밀번호가 다릅니다.'})
    else:
        # 아이디가 틀릴 때 출력값
        return jsonify({'result': 'fail', 'msg': '존재하지 않는 계정입니다.'})


@app.route('/write2', methods=['POST'])
def save_post():

    title_receive = request.form['title_give']
    star_receive = request.form['star_give']
    address_receive = request.form['address_give']
    content_receive = request.form['content_give']

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%y-%m-%d-%H-%M-%S')
    mydate = today.strftime('%y.%m.%d')
    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'title': title_receive,
        'star': star_receive,
        'address': address_receive,
        'content': content_receive,
        'file': f'{filename}.{extension}',
        'date': mydate
    }

    db.posts.insert_one(doc)

    return jsonify({'msg': '저장완료'})


@app.route('/write2', methods=['GET'])
def show_diary():
    posts = list(db.posts.find({}, {'_id': False}))
    return jsonify({'all_posts': posts})


if __name__ == '__main__':
    # session 사용시 지정해야할 정보 secret key지정하지않으면 동작x
    # app.secret_key = 'super secret key'
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run('0.0.0.0', port=5000, debug=True)
