# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요
여러 기술 블로그의 최신 글을 모아서 보여주는 iOS 앱. 매일 새벽 4시(KST)에 Firebase Functions가 블로그를 스크래핑해 Firestore에 저장하고, iOS 앱이 Firestore에서 직접 읽어온다.

- `TechBlogNotifications/`: iOS 앱 (SwiftUI, Firebase 연동)
- `tech-blog-scraper-functions/`: 스크래핑용 Firebase Functions (Python)
- `docs/`: iOS 앱과 동일한 Firestore `posts` 데이터를 보여주는 정적 웹페이지. GitHub Pages가 이 폴더를 그대로 서빙(`https://dgh06175.github.io/tech-blog-notification/`), 빌드 단계 없음.
- `TechBlogNotificationsServer/`: 삭제된 옛 Spring Boot 서버. **코드 없음** — 과거 스크래핑 로직 참고가 필요하면 git 이력에서 찾을 것.
- `scripts/scrapping-strategy.md`: 블로그별 스크래핑 전략(RSS vs API) 기록. 새 블로그 추가 전 반드시 확인.

## 작업 지침
- 서버 로직은 Spring Boot에서 Firebase Functions(Python)로 마이그레이션 완료된 상태. 새 서버 로직은 전부 Python으로 작성.
- 데이터베이스는 Firestore. iOS는 자체 API가 아니라 Firestore와 직접 통신한다(FirebaseFirestore SDK).
- 각 블로그 스크래핑 전략은 RSS 파싱 또는 API 호출 둘 중 하나만 사용한다(`scripts/scrapping-strategy.md` 참고). 웹 스크래핑은 최후의 수단.
- 최대한 심플하게 유지 (YAGNI, DRY, KISS).

## 빌드 / 테스트 명령

### iOS 앱 (`TechBlogNotifications/`)
- Xcode에서 `TechBlogNotifications.xcodeproj` 열어서 `TechBlogNotifications` 스킴으로 빌드/실행.
- 헤드리스 빌드: `xcodebuild -scheme TechBlogNotifications -destination 'platform=iOS Simulator,name=iPhone 15' build`
- 테스트: Xcode Test (별도 유닛테스트 타겟 없음, SwiftUI 프리뷰로 UI 확인)
- Firestore 연동 확인 시 `GoogleService-Info.plist`의 번들 ID가 활성 스킴과 일치하는지 확인.

### Firebase Functions (`tech-blog-scraper-functions/`)
```bash
cd tech-blog-scraper-functions
python3 -m venv .venv && source .venv/bin/activate   # 또는 Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```
- 스크래퍼만 로컬 테스트 (네트워크 호출 실제 발생, Firestore 미사용):
  `python test_scrapers.py` (전체) / `python test_scrapers.py <blog_key>` (단일, 예: `toss`, `samsung`, `kakao`, `woowahan`, `inflab`, `naver_d2`, `banksalad`)
- 스크래핑 + 파싱 통합 테스트: `python test_integration.py`
- Firestore 업로드까지 검증 (배포 전 필수): `python test_firestore_upload.py`
- 배포: `firebase deploy --only functions` (사전에 `firebase login`, `.firebaserc`에 프로젝트 ID 설정 필요)
- 배포 후 로그 확인: `firebase functions:log`
- 이 프로젝트에는 pytest 같은 테스트 프레임워크가 없다 — 위 스크립트들은 `if __name__ == "__main__"`으로 직접 실행하는 형태.

## 아키텍처

### 스크래퍼 구조 (`tech-blog-scraper-functions/scrapers/`)
- `base_scraper.py`의 `BaseScraper` 추상 클래스를 각 블로그 스크래퍼가 상속. 두 메서드만 구현하면 됨:
  - `get_blog_name() -> str`
  - `scrape() -> List[Dict[str, Any]]` — 내부에서 `Post` dataclass를 만들고 `.to_dict()`로 반환
- `Post.to_dict()`가 만드는 필드(`blog_name`, `title`, `link`, `date`, `scraped_at`)가 `firestore_uploader.py`가 기대하는 형식이므로, 새 스크래퍼를 추가할 때 이 계약을 반드시 지킬 것.
- `BaseScraper.parse_date()`가 Unix timestamp(초/밀리초), ISO 8601, RFC 2822(RSS), 기타 일반 날짜 문자열을 모두 처리하므로 날짜 파싱은 직접 구현하지 말고 이걸 재사용.
- 새 블로그 추가 순서: `scripts/scrapping-strategy.md`에 전략(RSS/API) 기록 → 스크래퍼 클래스 작성 → `main.py`의 `scrapers` 리스트와 `scraper_map` 딕셔너리 양쪽에 등록.

### Functions 엔트리포인트 (`main.py`)
- HTTP: `scrape_and_upload_all_blogs`(스크래핑+업로드), `scrape_all_blogs`(스크래핑만), `scrape_single_blog?blog=<key>&upload=<bool>`(블로그 지정), `get_collection_stats`
- Scheduled: `scheduled_scrape_and_upload` — 매일 04:00 Asia/Seoul, 크론 `0 4 * * *`

### Firestore 업로드 (`firestore_uploader.py`)
- 컬렉션명 `posts`. 문서 ID는 `blog_name` + 정규화된 link(프로토콜 제거, 소문자 host)를 MD5 해시한 값 — 동일 글의 중복 업로드를 이 ID로 방지하므로, 링크 정규화 로직(`_normalize_link`)을 건드릴 때는 기존 문서 ID와의 하위 호환성을 고려할 것.
- 기존 문서면 `update`, 없으면 `create_at`/`updated_at` 포함해 `set`.

### iOS 앱 (`TechBlogNotifications/TechBlogNotifications/`)
- 레이어 구조: `Model/`(PostDTO 등 Firestore 매핑 모델) → `Repository/`(Firestore 접근·비즈니스 로직) → `Domain/`(도메인 확장) → `View/`(SwiftUI 화면), 공용 상수/헬퍼는 `Utils/`.
- 상태관리는 `@Observable` 매크로 사용 (ObservableObject 아님).
- `PostManager`가 핵심 데이터 소스: Firestore `posts` 컬렉션을 `date` 내림차순, 페이지당 10개씩 커서 기반(`startAfterDocument`) 페이지네이션으로 로드. `NWPathMonitor`로 네트워크 상태를 감시하다가 재연결 시 자동으로 `refreshPosts()` 호출.
- `BookmarkManager`는 북마크 ID 목록과 북마크한 글 스냅샷(`StoredBookmark`)을 UserDefaults에 별도 저장 — 오프라인에서도 북마크 글을 보여주기 위함. 북마크 관련 코드 수정 시 두 저장소(ID 목록 + 스냅샷)의 정합성(`cleanupIfNeeded`)을 깨지 않도록 주의.
- `Post`는 여러 개의 이니셜라이저(DTO 기반, DTO+상태, 필드 직접 지정)를 갖고 있음 — Firestore 로드용과 UserDefaults 복원용 경로가 다르기 때문.

### 웹페이지 (`docs/`)
- 순수 HTML/CSS/JS, 빌드 도구 없음. Firebase JS SDK는 `js/app.js`에서 gstatic CDN의 ES 모듈을 직접 import.
- `js/firebase-config.js`의 `firebaseConfig`는 공개 저장소에 그대로 커밋되어 있음 — Firestore 보안 규칙(`allow read: if true; allow write: if false;`)이 실제 접근 제어를 담당하므로 의도된 것. `appId`는 별도 웹앱을 등록하지 않아 iOS 앱의 값을 재사용 중(Firestore 읽기엔 문제없음).
- `js/app.js`가 iOS `MainView.groupPostsByDate` / `PostManager` 로직을 그대로 재현: `date` 내림차순 + 커서 페이지네이션("더 보기" 버튼), 오늘/어제 글은 "최신" 섹션, 나머지는 월별 섹션, `blog_name === "Aws"` 제외. 북마크 등 iOS의 부가 기능은 의도적으로 없음(단순 조회 전용).

## 커밋 컨벤션
- `<type>: <한글 요약>` 형식, 예: `fix: 북마크 기능 수정`. type은 `feat`, `fix`, `chore`, `refactor` 등 사용.
