# SpartaTraveler
***
### 1. 프로젝트 소개

![](https://velog.velcdn.com/images/lries7897/post/eaecfbe5-d346-4210-9ba4-a0f1d7b8e57a/image.png)

프로젝트 데모영상 : 



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
- [구글API를 이용한 지도와 마커 사용방법](https://floor5th.tistory.com/88)
- [Flask 400 bad request: keyerror: 오류](https://jae04099.tistory.com/entry/PythonFlask-400-bad-request-keyerror-%ED%95%B4%EA%B2%B0)
    
***

### 3. 적용 기술
- ![](https://velog.velcdn.com/images/lries7897/post/c5347b01-bd36-4660-9fb4-9be2c079e71d/image.svg)
- ![](https://velog.velcdn.com/images/lries7897/post/4d823368-8bbb-4b3a-a375-44c926ae38a4/image.svg)
- ![](https://velog.velcdn.com/images/lries7897/post/c9e7711d-7a2c-4016-ba4c-c208c7f66c65/image.svg)
- ![](https://velog.velcdn.com/images/lries7897/post/5cfe62be-d84a-43f3-88bc-1dd0cc38024c/image.svg)
- ![](https://velog.velcdn.com/images/lries7897/post/c6619738-192d-4d2d-8860-b33d59dccc51/image.svg)
- ![](https://velog.velcdn.com/images/lries7897/post/75d83ebb-f013-459b-9c4f-368a871e52ac/image.svg)
- ![](https://velog.velcdn.com/images/lries7897/post/c12099a3-dd54-4183-8cf9-785901ce4780/image.svg)
- ![](https://velog.velcdn.com/images/lries7897/post/54164564-28a8-4123-b909-a71fc44263b7/image.svg)
- ![](https://velog.velcdn.com/images/lries7897/post/14492954-59c1-4c59-8276-3292f3c2c081/image.svg)


*** 
### 4. 주요 기능
+ jwt를 활용한 사용자 인증
+ jinja2 템플릿 활용
+ 네이버 지도 api활용



*** 
### 5. GitHub / S.A 주소 
+ github : https://github.com/Yoepee/til
+ S.A : https://velog.io/@lries7897/8%EC%A1%B0-%EC%9D%B4%EB%85%B8%EB%B2%A0%EC%9D%B4%EC%85%98-%EA%B0%95%EC%9B%90-1%EC%A3%BC%EC%B0%A8Mini-project-S.A
