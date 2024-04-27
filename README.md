# TechBlog_Alarm

기술 블로그 새로운 글 알림

매일 아침 8시~8시30분 사이에 아래 블로그중 새로운 게시글이 올라왔을 경우 Issues 를 발생시켜 알림을 보냅니다.

[Toss](https://toss.tech)

[Woowahan](https://techblog.woowahan.com)

[Kakao](https://tech.kakao.com/blog)

## 실행 과정 및 데이터 흐름

1. Github Workflows (`main.yaml`)

- `/.github/workflows/main.yaml` 은 Github Actions의 워크플로우를 정의한다.
- 정해진 스케줄에 `jobs`가 트리거되도록 설정된다.
- check_blog_post 액션을 실행한다.

2. Github Actions (jobs: `check_blog_post`)

- Github Action의 실제 로직이 작성된 곳이다.
- ubuntu(리눅스) 에서 실행된다.
- 로직 실행을 위한 준비 (파이썬, 노드 의존성 설치)를 한다.
- 쉘 스크립트로 `scrapper/main.py` 를 실행한다.

3. 웹 스크래핑 및 데이터 관리 (`scrapper/`, `pastData/`)

- `scrapper/main.py`는 저장된 블로그 링크들에서 게시글의 링크값을 불러온다.
- `pastData/*.json` 파일에 저장된 링크들과 비교하여 새로운 데이터라면 json에 링크 정보를 추가하고, 출력한다.

4. Github Actions 나머지 작업

- `scrapper/main.py`에서 `print` 된 값을 정제하여 output 변수에 넣는다.
- 환경변수 파일 `$GITHUB_ENV`에 환경 변수 `POST_DATA`에 결과값을 저장한다.

5. Github 푸쉬

- `POST_DATA`가 비어있지 않을 경우 변경된 json 파이를을 github에 커밋 및 푸쉬한다.

6. Github 이슈 발생

- `POST_DATA`가 비어있지 않을 경우 `/.github/actions/creats-blog-post-issue/` 안의 `action.yaml` 을 실행한다.

- `create-issue.js` 파일을 실행한다.
- 비밀 변수로 관리되는 깃허브 토큰과 `POST_DATA` 를 받아서 파싱한 다음, 이슈에 들어갈 제목, 본문 문자열로 가공한다.
- `@actions/core`, `@actions/github` 라이브러리를 사용하여 이슈를 생성한다.

7. 알림 전송

본 레파지토리에서 issues 를 watch 중이라면, 이메일로 알림이 전송된다.

## 체크리스트

- [ ] 기능 분리 및 로직 추상화하여 유지보수 시에 변경하는 부분 최소화 하기
- [x] json 으로 CRUD 기능 구현, 내부적으로 set 사용하여 성능 향상
- [ ] RDBMS 로 변경하기
- [x] 파이썬 결과물 JSON 형식으로 자바스크립트로 전달
- [ ] 게시글 하루에 여러개 올라오더라도 적용되도록 개선
- [ ] 웹 스크래퍼 테스트 자동화
- [x] 파이썬에서 자바로 옮기기

## 해야할 것

### 깃허브 이슈 알림

- html 요청
    - [x] HTML or XML 요청
    - [x] 블로그 사이트 html 또는 RSS(.xml) 반환 (블로그 지원에 따라)

- 파싱
    - [x] 첫 화면에서 보이는 최근 게시글들의 링크, 제목, 저자, 시간 가져오기
        - [x] 토스 기술블로그
        - [x] 우아한형제들 기술블로그
        - [x] 카카오 기술블로그

- 데이터 관리
    - [ ] 파싱한 결과와 저장된 결과를 비교
        - [ ] 새로 올라온 게시글 정보 반환
        - [ ] DB에 저장할 게시글 정보들 반환

- 새로 올라온 게시글 정보 출력
    - [ ] print 해서 우분투의 깃허브 액션 환경변수에 저장

- RDBMS 로 바꾸기 (github workflows - PostgreSQL)
    - [ ] 파일 새로 만들기
    - [ ] 불러오기
    - [ ] 저장
    - [ ] 수정
    - [ ] 삭제

### 앱 또는 웹

- 깃허브 이슈 알림 대신에 Spring 으로 API 만들기
- React 로 웹 페이지 또는 SwiftUI 로 iOS 앱 만들고 API 연결
- 배포
