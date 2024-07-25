//
//  ArticleTests.swift
//  ArticleTests
//
//  Created by 이상현 on 7/10/24.
//

import XCTest
@testable import TechBlogNotifications

class MockRepository: ArticleRepository {
    func loadArticles() -> [Article] {
        return [
            Article(id: 1, content: "테스트1", isFavorite: true),
            Article(id: 2, content: "테스트2")
        ]
    }
}

final class ArticleServiceTests: XCTestCase {
    func test점수_계산() {
        let mockRepository = MockRepository()
        let articleService = ArticleService(repository: mockRepository)
        
        let score = articleService.calculateScore()
        
        XCTAssertEqual(score, 30, "점수 계산 테스트 통과 실패")
    }
}
