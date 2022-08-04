# SpartaTraveler
***
### 1. 프로젝트 소개

![](https://velog.velcdn.com/images/lries7897/post/eaecfbe5-d346-4210-9ba4-a0f1d7b8e57a/image.png)

프로젝트 데모영상 : https://www.youtube.com/watch?v=iRkpHzd3kvg

 >SpartaTraveler는 자신이 가보고 또 가보고 싶은 여행지, 맛집등의 장소를 리뷰하는 플랫폼입니다.
 당신이 아는 당신만의 여행을 알려주세요.

웹사이트 링크 : http://hanarosystem.shop/

***

### 2. 프로젝트 개요

+ 팀 소개
	Innovation in Kangwon 8조
    
    - 팀장: 이승환
    - 팀원: 이선홍, 김동엽, 이수형. 이예솔
    

+ 프로젝트 제작기간
  -  2022.08.01 ~ 2022.08.04
    
    
***   
### 프로젝트 중 발생한 문제와 해결
> - 로그인
자동로그인을 구현하던 때 쿠키를 클라이언트에서 저장하는 방식의 보안취약점에 대한 문제를 인식하여 서버에서 쿠키를 집어넣어 건네주는 방식으로 해결
이때 본래 자동로그인쿠키와 아이디저장 쿠키를 동시에 서버에서 저장하려했지만 서버에서의 변수값 참조시 예상과 다른 값이 들어가는 일이 발생하여 아이디 저장 쿠키의 값은 클라이언트에서 저장받는 방식으로 해결.
> - 자동 로그인 기능 유효성 검사
각 페이지별 서버에서 발행한 자동로그인 전용 토큰 검사가 필요한 상황이나 기존 로그인 토큰 검사와 겹쳐서 혼란 발생.
자동 로그인 기능을 우선적으로 try구문을 통한 검사 후 로그인 토큰 유효성 검사 (이중 try구문을 통한 문제 해결)
> - 데이터 베이스 공유로 인한 문제
입력이 제한된 데이터가 계속 올라옴. 문제를 확인해보니 개발파일 공유로 인한 메인 데이터베이스 간섭 발생
개발 시 데이터 베이스 분리
> - 게시글 고유번호 지정
게시글 문서번호를 지정해 줄 때 데이터베이스 개수를 통한 count 해주려고 했는데 삭제 기능이 있다면 문서개수가 변하여 중복하는 경우 고려
전역변수를 지정하여 문서 작성시 마다 count 기능 추가
> - 글 작성시 다양한 입력값 유효성 검사 (파일, 체크박스, input)
 서버에서 입력값 공백 (" ")을 검사하도록 지정하였으나 오작동, check박스 여부와 파일 등록 여부를 따로 검사하여 출력하도록 설정
> - Github issue 관리 부진
개발 우선 작업과 사용자 조작 미숙으로 인한 issue 미사용, 토의를 통한 issue 정립으로 

<details>
    <summary>
        <b>구글API를 이용한 지도와 마커 사용방법</b>
    </summary>
<br>구글지도 api를 써본적이 없지만 (https://developers.google.com/maps/gmp-get-started?hl=ko#api-key) 와 (https://floor5th.tistory.com/88) 를 참고하여 구현하였다

</details>

<details>
    <summary>
        <b>Flask 400 bad request: keyerror: 오류</b>
    </summary>
<br>클라이언트로부터 서버가 데이터를 받는 순간 Flask 400 bad request: keyerror:오류가 발생하였지만 코드를 아래와 같이 바꾸니 오류가 해결되었다.

```python
	##원래의 코드
	@app.route('/checkrecord/delete', methods=['POST'])
	def delete_record():
	    title_receive = request.form['music_title']		##이 줄
	    return jsonify({'result': 'success'})

	##변경 후 
	@app.route('/checkrecord/delete', methods=['POST'])
	def delete_record():
	    title_receive = request.form.get('music_title', False)	##이 줄
	    db.music_diary.delete_one({'music_title': title_receive})
	    return jsonify({'result': 'success'})
```

</details>

    
***
### 3. 알고리즘

사진을 클릭하면 연결 구조를 확인하실 수 있습니다.


![](https://velog.velcdn.com/images/lries7897/post/f4b572cc-cb7a-4d5a-b6cc-67c452f694cf/image.png)
    
***

### 4. 적용 기술
<img src="https://img.shields.io/badge/Jinja-B41717?style=for-the-badge&logo=jinja&logoColor=white">
<img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white">
<img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=HTML5&logoColor=white">
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white">
<img src="https://img.shields.io/badge/Bulma-00D1B2?style=for-the-badge&logo=Bulma&logoColor=white">
<img src="https://img.shields.io/badge/Font Awesome-528DD7?style=for-the-badge&logo=font awesome&logoColor=white">
<img src="https://img.shields.io/badge/Google Maps-4285F4?style=for-the-badge&logo=Google Maps&logoColor=white">
<img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=CSS3&logoColor=white">
<img src="https://img.shields.io/badge/JQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">
<img src="https://img.shields.io/badge/aws-232F3E?style=for-the-badge&logo=Amazon AWS&logoColor=white">
<img src="https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=Bootstrap&logoColor=white">
<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white">
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white">


*** 
### 5. 주요 기능
+ jwt를 활용한 사용자 인증
+ jinja2 템플릿 활용
+ 구글 api활용
+ 사용자 검색을 통한 데이터 베이스 문서 출력
+ 사용자 등록을 통해 파일, 정보 등록 및 공유



*** 
### 6. GitHub / S.A 주소 
+ github : https://github.com/Yoepee/til
+ S.A : https://velog.io/@lries7897/8%EC%A1%B0-%EC%9D%B4%EB%85%B8%EB%B2%A0%EC%9D%B4%EC%85%98-%EA%B0%95%EC%9B%90-1%EC%A3%BC%EC%B0%A8Mini-project-S.A
