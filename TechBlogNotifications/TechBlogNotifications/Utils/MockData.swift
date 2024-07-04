//
//  MockPostData.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 6/8/24.
//

import Foundation

struct MockData {
    static var placeHolderPosts: [Post] = [
        Post(id: 1, link: "https://tech.blog/article/future-of-tech-2024", blogName: "Tech Blog", title: "미래 기술에 대한 전망", pubDate: Date(), scrapedDate: Date()),
        Post(id: 2, link: "https://dev.blog/2024/04/29/editor-dev/", blogName: "Dev Blog", title: "에디터 개발의 고충과 새로운 기능 소개", pubDate: "2024. 5. 20".parseDate(), scrapedDate: Date()),
        Post(id: 3, link: "https://tech.blog/article/api-engineering", blogName: "Tech Blog", title: "API 엔지니어링: 자유롭고 빠르게", pubDate: "2024. 3. 20".parseDate(), scrapedDate: Date()),
        Post(id: 4, link: "https://tech.blog/article/deployment-system", blogName: "Tech Blog", title: "프론트엔드 배포 시스템 진화: 카나리 배포 적용", pubDate: "2024. 3. 5".parseDate(), scrapedDate: Date()),
        Post(id: 5, link: "https://dev.blog/2024/04/29/webview-debugging/", blogName: "Dev Blog", title: "Devtools로 웹뷰 디버깅 환경 만들기", pubDate: "2024. 4. 29".parseDate(), scrapedDate: Date()),
        Post(id: 6, link: "https://dev.blog/2024/04/29/image-viewer/", blogName: "Dev Blog", title: "스벨트 이미지 뷰어 라이브러리 소개", pubDate: "2024. 4. 29".parseDate(), scrapedDate: Date()),
        Post(id: 7, link: "https://tech.world/ai-messages/", blogName: "Tech World", title: "AI 메시지 생성기: 센스있는 메시지 만들기", pubDate: "2024. 5. 2".parseDate(), scrapedDate: Date()),
        Post(id: 8, link: "https://tech.world/jpa-hibernate/", blogName: "Tech World", title: "Hibernate에서 @NaturalId 사용하기", pubDate: "2024. 4. 30".parseDate(), scrapedDate: Date()),
        Post(id: 9, link: "https://tech.world/eslint-prettier/", blogName: "Tech World", title: "ESLint와 Prettier 설정 공유하기", pubDate: "2024. 4. 24".parseDate(), scrapedDate: Date())
    ]
}
