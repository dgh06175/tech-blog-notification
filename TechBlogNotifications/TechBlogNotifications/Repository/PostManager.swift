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
    private var lastDocument: DocumentSnapshot?
    private let pageSize: Int = 10
    private let networkMonitor = NWPathMonitor()
    private let networkQueue = DispatchQueue(label: "NetworkMonitor")
    
    private(set) var posts: [Post] = []
    private(set) var isConnected: Bool = true
    
    private let bookmarkManager = BookmarkManager()
    private let db = Firestore.firestore()

    private var hasMorePosts: Bool = true
    var isLoading: Bool = false
    
    
    // 데이터가 앱 시작시 한번만 불러와져도 되므로 init 에서 작성하고 App 시작시 초기화되도록 함
    init() {
        startNetworkMonitoring()
        
        Task {
            await loadInitialPosts()
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
                        await self?.refreshPosts()
                    }
                } else {
                    print("네트워크 연결 끊어짐 - 오프라인 모드")
                }
            }
        }
        networkMonitor.start(queue: networkQueue)
    }
    
    private func refreshPosts() async {
        guard isConnected else { return }
        await loadInitialPosts()
    }
    
    @MainActor
    private func loadMockData() {
        self.posts = MockData.placeHolderPosts
        self.isLoading = false
    }
    
    // 실제 데이터 받아오기
    private func fetchPosts(reset: Bool) async {
        guard await beginLoading(reset: reset) else { return }

        do {
            let query = await makeQuery()
            let snapshot = try await query.getDocuments(source: .default)
            try await handleSnapshot(snapshot, reset: reset)
        } catch {
            print("Firestore 오류: \(error)")
            await finishLoading()
        }
    }
    
    private func makeQuery() async -> Query {
        let startingDocument = await MainActor.run { lastDocument }
        var query: Query = db.collection("posts")
            .order(by: "date", descending: true)
            .limit(to: pageSize)
        
        if let startingDocument {
            query = query.start(afterDocument: startingDocument)
        }
        return query
    }
    
    private func handleSnapshot(_ snapshot: QuerySnapshot, reset: Bool) async throws {
        let fetchedPosts = try snapshot.documents.compactMap { document -> PostDTO? in
            try document.data(as: PostDTO.self)
        }
        
        let newPosts = fetchedPosts.map { dto in
            Post(from: dto,
                 isWatched: false,
                 isBookmarked: bookmarkManager.isBookmarked(id: dto.id ?? ""))
        }
        
        await MainActor.run {
            if reset {
                posts = newPosts
            } else {
                let existingIds = Set(posts.map { $0.id })
                let filtered = newPosts.filter { !existingIds.contains($0.id) }
                posts.append(contentsOf: filtered)
            }
            lastDocument = snapshot.documents.last
            hasMorePosts = snapshot.documents.count == pageSize
        }
        await finishLoading()
    }
    
    private func beginLoading(reset: Bool) async -> Bool {
        return await MainActor.run {
            if isLoading {
                return false
            }
            if reset {
                posts.removeAll()
                lastDocument = nil
                hasMorePosts = true
            }
            isLoading = true
            return true
        }
    }
    
    private func finishLoading() async {
        await MainActor.run {
            isLoading = false
        }
    }
    
    private func loadInitialPosts() async {
        await fetchPosts(reset: true)
    }
    
    // 다음 페이지 데이터를 요청하는 메서드
    func loadNextPage() async {
        guard hasMorePosts else { return }
        await fetchPosts(reset: false)
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
