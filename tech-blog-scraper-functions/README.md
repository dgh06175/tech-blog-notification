# Tech Blog Scraper Functions

Firebase Functions로 구현된 기술 블로그 스크래핑 시스템

## 지원 블로그

### RSS 방식
- **삼성 기술블로그**: https://techblog.samsung.com/rss
- **카카오 기술블로그**: https://tech.kakao.com/blog/feed  
- **우아한형제들**: https://techblog.woowahan.com/feed/

### API 방식
- **인프랩**: https://tech.inflab.com/page-data/index/page-data.json
- **토스**: API 엔드포인트 사용
- **네이버 D2**: https://d2.naver.com/api/v1/contents
- **뱅크샐러드**: 2단계 API 호출 방식

## 로컬 테스트

### 환경 설정
```bash
pip install -r requirements-dev.txt
```

### 테스트 실행
```bash
# 모든 스크래퍼 테스트
python test_scrapers.py

# 특정 스크래퍼만 테스트
python test_scrapers.py samsung
python test_scrapers.py kakao
python test_scrapers.py woowahan
python test_scrapers.py inflab
python test_scrapers.py toss
python test_scrapers.py naver_d2
python test_scrapers.py banksalad
```

## Firebase Functions 배포

### 배포 전 준비
```bash
firebase init functions
```

### 배포
```bash
firebase deploy --only functions
```

## API 엔드포인트

- **모든 블로그 스크래핑**: `/scrape_all_blogs`
- **특정 블로그 스크래핑**: `/scrape_single_blog?blog=BLOG_NAME`

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