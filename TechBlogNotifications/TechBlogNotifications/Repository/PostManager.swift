//
//  DataManager.swift
//  TechBlogNotifications
//
//  Created by 이상현 on 6/6/24.
//

import Foundation
import FirebaseFirestore
import Network

@Observable
class PostManager {
    enum PostError: Error {
        case firestoreError
        case parseError
    }
    
    private var lastDocument: DocumentSnapshot?
    private let pageSize: Int = 10
    private let networkMonitor = NWPathMonitor()
    private let networkQueue = DispatchQueue(label: "NetworkMonitor")
    
    private(set) var posts: [Post] = []
    private(set) var isConnected: Bool = true
    
    private let bookmarkManager = BookmarkManager()
    private let db = Firestore.firestore()

    var isLoading: Bool = true
    
    
    // 데이터가 앱 시작시 한번만 불러와져도 되므로 init 에서 작성하고 App 시작시 초기화되도록 함
    init() {
        startNetworkMonitoring()
        
        Task {
            do {
                try await fetchPosts()
            } catch {
                print("\(error) 예외 발생")
            }
        }
    }
    
    deinit {
        networkMonitor.cancel()
    }
    
    private func startNetworkMonitoring() {
        networkMonitor.pathUpdateHandler = { [weak self] path in
            DispatchQueue.main.async {
                self?.isConnected = path.status == .satisfied
                if path.status == .satisfied {
                    print("네트워크 연결됨 - 데이터 새로고침 시도")
                    Task {
                        try? await self?.refreshPosts()
                    }
                } else {
                    print("네트워크 연결 끊어짐 - 오프라인 모드")
                }
            }
        }
        networkMonitor.start(queue: networkQueue)
    }
    
    private func refreshPosts() async throws {
        guard isConnected else { return }
        
        lastDocument = nil
        await MainActor.run {
            posts.removeAll()
            isLoading = true
        }
        
        try await fetchPosts()
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
            
            let snapshot = try await query.getDocuments(source: .default)
            
            let fetchedPosts = try snapshot.documents.compactMap { document -> PostDTO? in
                try document.data(as: PostDTO.self)
            }
            
            let newPosts = fetchedPosts.map { dto in
                Post(from: dto, isWatched: false, isBookmarked: bookmarkManager.isBookmarked(id: dto.id ?? ""))
            }
            
            await MainActor.run {
                self.posts.append(contentsOf: newPosts)
                self.lastDocument = snapshot.documents.last
                self.isLoading = false
            }
            
            if snapshot.metadata.isFromCache {
                print("데이터를 캐시에서 로드했습니다 (오프라인 모드)")
            } else {
                print("데이터를 서버에서 로드했습니다")
            }
            
        } catch {
            print("Firestore 오류: \(error)")
            if let firestoreError = error as NSError?, firestoreError.code == 14 {
                print("네트워크 연결 문제로 인한 오류 - 오프라인 모드로 전환")
                await MainActor.run {
                    self.isLoading = false
                }
                try await loadFromCache()
            } else {
                throw PostError.firestoreError
            }
        }
    }
    
    private func loadFromCache() async throws {
        do {
            var query: Query = db.collection("posts")
                .order(by: "created_at", descending: true)
                .limit(to: pageSize)
            
            if let lastDocument = lastDocument {
                query = query.start(afterDocument: lastDocument)
            }
            
            let snapshot = try await query.getDocuments(source: .cache)
            
            let fetchedPosts = try snapshot.documents.compactMap { document -> PostDTO? in
                try document.data(as: PostDTO.self)
            }
            
            let newPosts = fetchedPosts.map { dto in
                Post(from: dto, isWatched: false, isBookmarked: bookmarkManager.isBookmarked(id: dto.id ?? ""))
            }
            
            await MainActor.run {
                self.posts.append(contentsOf: newPosts)
                self.lastDocument = snapshot.documents.last
            }
            
            print("캐시에서 \(newPosts.count)개의 게시물을 로드했습니다")
        } catch {
            print("캐시에서 데이터를 로드할 수 없습니다: \(error)")
        }
    }
    
    // 다음 페이지 데이터를 요청하는 메서드
    func loadNextPage() async {
        guard !isLoading else { return }
        
        await MainActor.run {
            self.isLoading = true
        }
        
        do {
            try await fetchPosts()
        } catch {
            print("페이지를 로드하는 중 오류 발생: \(error)")
            await MainActor.run {
                self.isLoading = false
            }
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
