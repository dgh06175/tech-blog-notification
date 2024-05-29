# Tech Blog Notification

기술 블로그 새로운 글 알림

매일 아침 8시~8시30분 사이에 아래 블로그중 새로운 게시글이 올라왔을 경우 Issues 를 발생시켜 알림을 보냅니다.

[Toss](https://toss.tech)

[Woowahan](https://techblog.woowahan.com)

[Kakao](https://tech.kakao.com/blog)

## 실행 과정 및 데이터 흐름

1. Github Workflows (`main.yaml`)

- `/.github/workflows/main.yaml` 은 Github Actions의 워크플로우를 정의한다.
- 정해진 스케줄에 `jobs`가 트리거되도록 설정된다.
- check_blog_post job을 실행한다.

2. Github Actions (jobs: `check_blog_post`)

- Github Action의 실제 로직이 작성된 곳이다.
- ubuntu(리눅스) 에서 실행된다.
- 로직 실행을 위한 준비 (자바, 노드 및 라이브러리 설치)를 한다.
- 자바 코드를 빌드 한 후 `target/teckblog-alarm-1.0-SNAPSHOT.jar` 파일을 실행한다.

3. 웹 스크래핑 및 데이터 관리 (`src/main/java/org.example/`, `database/`)

- 저장된 블로그 링크들에서 게시글의 링크값을 불러온다.
- `database/` 폴더 내부의 파일에 저장된 링크들과 비교하여 새로운 데이터와 과거 데이터를 추가한다.

4. Github Actions 나머지 작업

- `database/new` 에 저장된 결과값들을 읽어서 새로운 게시글이 있는지 확인 후 이번 단계의 `output` 으로 불리언 `new_posts`를 반환한다.

5. Github 커밋, 푸쉬

- `new_posts`가 true 일 경우 변경된 DB를 github에 커밋 및 푸쉬한다.

6. Github 이슈 발생

- `new_posts`가 true 일 경우 `/.github/actions/creats-blog-post-issue/` 안의 `action.yaml` 을 실행한다.

- `create-issue.js` 파일을 실행한다.
- 비밀 변수로 관리되는 깃허브 토큰을 받고, `database/new/*.json` 파일들을 읽어서 파싱한 후 이슈에 들어갈 제목, 본문 문자열로 가공한다.
- `@actions/core`, `@actions/github` 라이브러리를 사용하여 이슈를 생성한다.

7. 알림 전송

본 레파지토리에서 issues 를 watch 중이라면, 이메일로 알림이 전송된다.

## 체크리스트

- [ ] 기능 분리 및 로직 추상화하여 유지보수 시에 변경하는 부분 최소화 하기
- [x] json 으로 CRUD 기능 구현, 내부적으로 set 사용하여 성능 향상
- [ ] RDBMS 로 변경하기
- [x] 파이썬 결과물 JSON 형식으로 자바스크립트로 전달
- [x] 게시글 하루에 여러개 올라오더라도 적용되도록 개선
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
    - [x] 파싱한 결과와 저장된 결과를 비교
        - [x] 새로 올라온 게시글 정보 반환
        - [x] DB에 저장할 게시글 정보들 반환

- 새로 올라온 게시글 정보 출력
    - [x] 파일에 저장

- 버그 수정
    - [ ] 게시물 링크를 기준으로 중복 검사 하는것으로 변경 (링크가 동일하면 다른 데이터가 바뀌어도 새로 업로드 하지 않음)
    - [ ] 커밋 전에 새로운 링크 데이터 출력하는 것으로 변경 (디버깅)

- [ ] Gradle로 변경
- [ ] Spring MVC 적용

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

### 기능 추가

- [ ] 블로그 개수 추가
- [ ] 토스 저자 표시 기능
    - [ ] 본문 데이터 받아와서 저자 긁어오기
- [ ] 키워드 기능
    - ML로 주요 태그 추출해서 키워드 표시 및 필터링 가능하도록
