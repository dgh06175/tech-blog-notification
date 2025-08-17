# 기술 블로그 스크래퍼 Firebase Functions

매일 새벽 4시(한국시간)에 자동으로 7개 기술 블로그를 스크래핑하고 FireStore에 업로드하는 Firebase Functions 프로젝트입니다.

## 지원하는 블로그
- Samsung Research 기술 블로그
- Kakao Tech 블로그
- 우아한형제들 기술 블로그
- Inflab Tech 블로그
- Toss Tech 블로그
- Naver D2 블로그
- 뱅크샐러드 기술 블로그

## 배포 방법

### 1. Firebase CLI 설치
```bash
npm install -g firebase-tools
```

### 2. Firebase 로그인
```bash
firebase login
```

### 3. 프로젝트 설정
```bash
# .firebaserc 파일에서 YOUR_PROJECT_ID를 실제 Firebase 프로젝트 ID로 변경
firebase use YOUR_PROJECT_ID
```

### 4. 배포
```bash
firebase deploy --only functions
```

## Functions 목록

### HTTP Functions
- `scrape_and_upload_all_blogs`: 모든 블로그 스크래핑 및 FireStore 업로드
- `scrape_all_blogs`: 모든 블로그 스크래핑만 (업로드 없음)
- `scrape_single_blog`: 특정 블로그만 스크래핑
- `get_collection_stats`: FireStore 컬렉션 통계 조회

### Scheduled Function
- `scheduled_scrape_and_upload`: 매일 새벽 4시(한국시간) 자동 실행

## 로그 확인
```bash
firebase functions:log
```

## 로컬 테스트
```bash
python test_scrapers.py           # 스크래퍼 테스트
python test_integration.py        # 통합 테스트
```

## 프로젝트 구조

```
tech-blog-scraper-functions/
├── main.py                 # Firebase Functions 엔트리포인트
├── requirements.txt        # Firebase Functions 의존성
├── requirements-dev.txt    # 로컬 개발용 의존성
├── test_scrapers.py       # 로컬 테스트 스크립트
├── README.md
└── scrapers/
    ├── __init__.py
    ├── base_scraper.py     # 기본 스크래퍼 인터페이스
    ├── samsung_scraper.py
    ├── kakao_scraper.py
    ├── woowahan_scraper.py
    ├── inflab_scraper.py
    ├── toss_scraper.py
    ├── naver_d2_scraper.py
    └── banksalad_scraper.py
```