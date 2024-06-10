//
//  DataManager.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 6/6/24.
//

import Foundation

@Observable
class PostManager {
    private(set) var posts: [Post] = MockData.samplePosts
    var isLoading: Bool = true
    
    // 데이터가 앱 시작시 한번만 불러와져도 되므로 init 에서 작성하고 App 시작시 초기화되도록 함
    init() {
        fetchPosts()
    }
    
    // TODO: 실제 데이터 받아오도록 수정
    private func fetchPosts() {
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            self.posts = MockData.samplePosts
            self.isLoading = false
        }
    }
}
