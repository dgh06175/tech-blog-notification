//
//  DataManager.swift
//  TechBlogNotifications
//
//  Created by 이상현 on 6/6/24.
//

import Foundation
import FirebaseFirestore

@Observable
class PostManager {
    enum PostError: Error {
        case firestoreError
        case parseError
    }
    
    private var lastDocument: DocumentSnapshot?
    private let pageSize: Int = 10
    
    private(set) var posts: [Post] = []
    
    private let bookmarkManager = BookmarkManager()
    private let db = Firestore.firestore()

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
    
    @MainActor
    private func loadMockData() {
        self.posts = MockData.placeHolderPosts
        self.isLoading = false
    }
    
    // 실제 데이터 받아오기
    private func fetchPosts() async throws {
        do {
            var query: Query = db.collection("posts")
                .order(by: "created_at", descending: true)
                .limit(to: pageSize)
            
            if let lastDocument = lastDocument {
                query = query.start(afterDocument: lastDocument)
            }
            
            let snapshot = try await query.getDocuments()
            
            let fetchedPosts = try snapshot.documents.compactMap { document -> PostDTO? in
                try document.data(as: PostDTO.self)
            }
            
            let newPosts = fetchedPosts.map { dto in
                Post(from: dto, isWatched: false, isBookmarked: bookmarkManager.isBookmarked(id: dto.id ?? ""))
            }
            
            self.posts.append(contentsOf: newPosts)
            self.lastDocument = snapshot.documents.last
            self.isLoading = false
        } catch {
            print("Firestore 오류: \(error)")
            throw PostError.firestoreError
        }
    }
    
    // 다음 페이지 데이터를 요청하는 메서드
    func loadNextPage() async {
        guard !isLoading else { return }
        
        do {
            try await fetchPosts()
        } catch {
            print("페이지를 로드하는 중 오류 발생: \(error)")
        }
    }
    
    func toggleBookmark(for post: Post) {
        post.isBookmarked.toggle()
        if post.isBookmarked {
            bookmarkManager.saveBookmark(post: post)
        } else {
            bookmarkManager.removeBookmark(post: post)
        }
    }
    
    func getBookmarkedPosts() -> [Post] {
        bookmarkManager.fetchBookmarkedPosts(from: posts)
    }
}
