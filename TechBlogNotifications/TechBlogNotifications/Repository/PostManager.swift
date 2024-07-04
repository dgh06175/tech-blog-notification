//
//  DataManager.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 6/6/24.
//

import Foundation

@Observable
class PostManager {
    private(set) var posts: [Post] = MockData.placeHolderPosts
    var isLoading: Bool = true
    
    // 데이터가 앱 시작시 한번만 불러와져도 되므로 init 에서 작성하고 App 시작시 초기화되도록 함
    init() {
        Task {
            await fetchPosts()
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
    private func fetchPosts() async {
        guard let url = URL(string: "http://localhost:8080/find-all") else {
            return
        }
        
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .formatted(DateFormatter.iso8601Full)
            let fetchedPosts = try decoder.decode([Post].self, from: data)
            self.posts = fetchedPosts
            self.isLoading = false
        } catch {
            print("JSON 파싱 에러: \(error)")
        }
    }
}
