# Claude Instructions

## 프로젝트 개요
이 프로젝트는 기술 블로그 알림 시스템입니다.

## 작업 지침
- iOS 앱이 클라이언트
- Spring Boot 서버는 현재 Firebase Functions 로 마이그레이션 예정
- 데이터베이스는 FireStore 사용
- Swift 코드 스타일: SwiftUI, iOS 컨벤션 따름
- Firebase Functions 는 Python 언어로
- 테스트 실행: `./gradlew test` (서버), Xcode Test (iOS)
- 빌드 명령: `./gradlew build` (서버)

## 코드 컨벤션
- 기존 코드 스타일 유지
- 공식 지침에서 권장하는 가장 깔끔하고 정석적인 스타일 사용
- 최대한 심플하게 유지. yagni dry kiss 명심

## 파일 구조
- `TechBlogNotifications/`: iOS 앱
- `tech-blog-scraper-functions/`: 스크래핑 함수들
- `TechBlogNotificationsServer/`: Spring Boot 서버, 삭제 되었으니, 스크래핑 로직 참고용

# 작업 순서

1. Firebase Function 에 각 블로그별 스크래핑 스크립트 추가
   - [ ] 로컬에서 테스트 가능하도록
   - [ ] `scripts/scrapping-strategy.md` 에 작성된 블로그 별 스크래픽 전략에 따라 구현. 전략은 API 사용 또는 RSS 파싱 둘 중하나만.
2. Funcions 에서 스크래핑한 정보들을 FireStore 에 업로드
3. iOS 의 통신 코드를 기존 자체 API 방식에서 FireStore 과 연동된 방식으로 업로드