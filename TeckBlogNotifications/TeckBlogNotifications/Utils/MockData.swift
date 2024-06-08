//
//  MockPostData.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 6/8/24.
//

import Foundation

struct MockData {
    static var samplePosts: [Post] = [
        Post(blogName: "Toss Tech", link: "https://toss.tech/article/react-native-2024", title: "토스가 꿈꾸는 React Native 기술의 미래", timestamp: Date(), isBookMark: false, bookMarkCount: 0, isSeen: false, tags: ["React Native", "Mobile"]),
        Post(blogName: "Kakao Tech", link: "https://tech.kakao.com/2024/04/29/techmeet-web-editor/", title: "웹 텍스트 에디터 개발에 필요한 고민과 신규 에디터 소개 / 제5회 Kakao Tech Meet", timestamp: Date(), isBookMark: false, bookMarkCount: 0, isSeen: false, tags: ["Web", "Editor"]),
        Post(blogName: "Toss Tech", link: "https://toss.tech/article/docs-engineering", title: "더 자유롭고, 빠르고, 정확하게: 토스페이먼츠 API 문서 엔지니어링", timestamp: "2024. 3. 20".parseDate(), isBookMark: false, bookMarkCount: 0, isSeen: false, tags: ["API", "Engineering"]),
        Post(blogName: "Toss Tech", link: "https://toss.tech/article/engineering-note-9", title: "프론트엔드 배포 시스템의 진화 (1) - 결제 SDK에 카나리 배포 적용하기", timestamp: "2024. 3. 5".parseDate(), isBookMark: false, bookMarkCount: 0, isSeen: false, tags: ["Frontend", "Deployment"]),
        Post(blogName: "Kakao Tech", link: "https://tech.kakao.com/2024/04/29/techmeet-webview-debugging/", title: "Chrome Devtools를 활용하여 나만의 웹뷰 디버깅 환경 만들기 / 제5회 Kakao Tech Meet", timestamp: "2024. 4. 29".parseDate(), isBookMark: false, bookMarkCount: 0, isSeen: false, tags: ["Webview", "Debugging"]),
        Post(blogName: "Kakao Tech", link: "https://tech.kakao.com/2024/04/29/techmeet-image-viewer/", title: "[Phocus] 사용자 경험 중심 스벨트 이미지 뷰어 라이브러리 / 제5회 Kakao Tech Meet", timestamp: "2024. 4. 29".parseDate(), isBookMark: false, bookMarkCount: 0, isSeen: false, tags: ["Image Viewer", "Svelte"]),
        Post(blogName: "Woowahan Tech", link: "https://techblog.woowahan.com/17241/", title: "배민선물하기 AI 메시지 제작기: 생성 AI가 센스 있는 선물 메시지를 대신 쓰기까지", timestamp: "2024. 5. 2".parseDate(), isBookMark: false, bookMarkCount: 0, isSeen: false, tags: ["AI", "Messaging"]),
        Post(blogName: "Woowahan Tech", link: "https://techblog.woowahan.com/17221/", title: "JPA에서 아이디를 자동증가 값으로 사용 시 하이버네이트의 @NaturalId 사용해 보기", timestamp: "2024. 4. 30".parseDate(), isBookMark: false, bookMarkCount: 0, isSeen: false, tags: ["JPA", "Hibernate"]),
        Post(blogName: "Woowahan Tech", link: "https://techblog.woowahan.com/15903/", title: "우리 팀을 위한 ESLint, Prettier 공유 컨피그 만들어보기", timestamp: "2024. 4. 24".parseDate(), isBookMark: false, bookMarkCount: 0, isSeen: false, tags: ["ESLint", "Prettier"])
    ]
}
