//
//  DataManager.swift
//  TechBlogNotifications
//
//  Created by 이상현 on 6/6/24.
//

import Foundation

@Observable
class PostManager {
    enum PostError: Error {
        case urlError
        case parseError
    }
    
    private(set) var posts: [Post] = MockData.placeHolderPosts
    var isLoading: Bool = true
    
    // 데이터가 앱 시작시 한번만 불러와져도 되므로 init 에서 작성하고 App 시작시 초기화되도록 함
    init() {
        Task {
            do {
                try await fetchPosts()
            } catch {
                print("\(error) 예외 발생")
            }
        }
    }
    
    // 임시 받아오기
    private func fetchMockPosts() {
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            self.posts = MockData.placeHolderPosts
            self.isLoading = false
        }
    }
    
    // 실제 데이터 받아오기
    private func fetchPosts() async throws {
        guard let urlString = ProcessInfo.processInfo.environment["APIBaseURL"],
              let url = URL(string: urlString + "posts") else {
            throw PostError.urlError
        }
        
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .formatted(DateFormatter.iso8601Full)
            let fetchedPosts = try decoder.decode([Post].self, from: data)
            self.posts = fetchedPosts
            self.isLoading = false
        } catch {
            print("디코딩 오류: \(error)")
            throw PostError.parseError
        }
    }
}

struct Article {
    let id: Int
    let content: String
    var isFavorite: Bool = false
}

protocol ArticleRepository {
    func loadArticles() -> [Article]
}

class Database: ArticleRepository {
    func loadArticles() -> [Article] {
        // 실제로는 데이터베이스에서 데이터를 불러온다.
        return [Article(id: 3, content: "DB에서 불러온 데이터")]
    }
}

class ArticleService {
    private var articles: [Article]
    private let repository: ArticleRepository
    
    init(repository: ArticleRepository) {
        self.articles = repository.loadArticles()
        self.repository = repository
    }
    
    // 값 반환하도록 변경
    func calculateScore() -> Int {
        var score = 0
        for article in articles {
            print(article.isFavorite ? "20추가" : "10추가")
            score += article.isFavorite ? 20 : 10
        }
        return score
    }
}
