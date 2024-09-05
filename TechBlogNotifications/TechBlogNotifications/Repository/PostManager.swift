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
    
    private var currentPage: Int = 0
    
    private(set) var posts: [Post] = []
    //    private(set) var posts: [Post] = MockData.placeHolderPosts
    var isLoading: Bool = true
    
    // 데이터가 앱 시작시 한번만 불러와져도 되므로 init 에서 작성하고 App 시작시 초기화되도록 함
    init() {
        Task {
            do {
                try await fetchPosts(page: currentPage)
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
    private func fetchPosts(page: Int) async throws {
        let urlString = Config.API_URL
        guard let url = URL(string: "\(urlString)posts?page=\(page)") else {
            throw PostError.urlError
        }
        
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .formatted(DateFormatter.iso8601Full)
            let fetchedPosts = try decoder.decode([Post].self, from: data)
            
            //            self.posts = fetchedPosts
            self.posts.append(contentsOf: fetchedPosts)
            self.isLoading = false
        } catch {
            print("디코딩 오류: \(error)")
            throw PostError.parseError
        }
    }
    
    // 페이지를 증가시키고 새로운 데이터를 요청하는 메서드
    func loadNextPage() async {
        currentPage += 1
        do {
            try await fetchPosts(page: currentPage)
        } catch {
            print("페이지를 로드하는 중 오류 발생: \(error)")
        }
    }
}
