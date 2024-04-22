# TechBlog_Alarm

기술 블로그 새로운 글 알림

매일 아침 8시~8시30분 사이에 아래 블로그중 새로운 게시글이 올라왔을 경우 Issues 를 발생시켜 알림을 보냅니다.

[Toss](https://toss.tech)

[Woowahan](https://techblog.woowahan.com)

[Kakao](https://tech.kakao.com/blog)

## 체크리스트

## 1. 파이썬 웹 스크래핑

기술 블로그들의 html 컨텐츠를 파싱하여 JSON 으로 로컬에 저장하고, 최신 게시글 일 경우 그 정보를 JSON 으로 파이썬으로 전달한다.

- [ ] 기능 분리 및 로직 추상화하여 유지보수 시에 변경하는 부분 최소화 하기
- [x] json 으로 CRUD 기능 구현, 내부적으로 set 사용하여 성능 향상
- [ ] RDBMS 로 변경
- [x] 파이썬 결과물 JSON 형식으로 자바스크립트로 전달
- [ ] 게시글 하루에 여러개 올라오더라도 적용되도록 개선

## 2. 자바스크립트

최신 블로그 게시글 정보를 JSON 으로 받아서 게시글 형식의 markdown 문자열로 만들고 `@actions/github` 라이브러리를 활용하여 깃허브 add, push, 이슈발생 로직을 수행한다.

## 3. Github Actions로 자동화

위 과정을 Github Actions로 매일 수행하도록 자동화한다.

```
.github
├── actions
│   ├── create-blog-post-issue
│   │   ├── action.yaml
└── workflows
    └── main.yaml
```

`main.yaml` 파일로 actions 의 job을 정의하고 `action.yaml` 로 이슈를 발생한다.

또한 로컬 환경에서 Github Actions 를 실행하여 테스트 하기 위해 `act` 로 Docker 컨테이너를 사용한다.
