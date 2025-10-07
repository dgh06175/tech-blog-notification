//
//  BookmarkManager.swift
//  TechBlogNotifications
//
//  Created by 이상현 on 9/25/24.
//

import Foundation

@Observable
class BookmarkManager {
    private struct StoredBookmark: Codable {
        let id: String
        let link: String
        let blogName: String
        let title: String
        let pubDate: Date
        let scrapedDate: Date

        init(post: Post) {
            self.id = post.id
            self.link = post.link
            self.blogName = post.blogName
            self.title = post.title
            self.pubDate = post.pubDate
            self.scrapedDate = post.scrapedDate
        }

        func makePost() -> Post {
            Post(id: id,
                 link: link,
                 blogName: blogName,
                 title: title,
                 pubDate: pubDate,
                 scrapedDate: scrapedDate,
                 isWatched: false,
                 isBookmarked: true)
        }
    }

    private let bookmarksKey = "bookmarks"
    private let bookmarkedPostsKey = "bookmarked_posts"
    private var cachedBookmarks: [String]
    private var cachedBookmarkedPosts: [String: StoredBookmark]

    init() {
        let storedIds = UserDefaults.standard.array(forKey: bookmarksKey) as? [String] ?? []
        self.cachedBookmarks = storedIds

        if let data = UserDefaults.standard.data(forKey: bookmarkedPostsKey),
           let storedPosts = try? JSONDecoder().decode([StoredBookmark].self, from: data) {
            self.cachedBookmarkedPosts = Dictionary(uniqueKeysWithValues: storedPosts.map { ($0.id, $0) })
        } else {
            self.cachedBookmarkedPosts = [:]
        }

        cleanupIfNeeded()
    }
    
    func saveBookmark(post: Post) {
        if !cachedBookmarks.contains(post.id) {
            cachedBookmarks.append(post.id)
        }
        cachedBookmarkedPosts[post.id] = StoredBookmark(post: post)
        persist()
    }

    func removeBookmark(post: Post) {
        if let index = cachedBookmarks.firstIndex(of: post.id) {
            cachedBookmarks.remove(at: index)
        }
        cachedBookmarkedPosts.removeValue(forKey: post.id)
        persist()
    }

    func fetchBookmarks() -> [String] {
        cachedBookmarks
    }

    func fetchBookmarkedPosts(from posts: [Post]) -> [Post] {
        posts.filter { cachedBookmarks.contains($0.id) }
    }

    func fetchStoredBookmarkedPosts() -> [Post] {
        cachedBookmarks.compactMap { cachedBookmarkedPosts[$0]?.makePost() }
    }
    
    func isBookmarked(id: String) -> Bool {
        cachedBookmarks.contains(id)
    }

    func refreshBookmarkData(with post: Post) {
        guard cachedBookmarks.contains(post.id) else { return }
        cachedBookmarkedPosts[post.id] = StoredBookmark(post: post)
        persistStoredPosts()
    }

    private func persist() {
        persistBookmarkIds()
        persistStoredPosts()
    }

    private func persistBookmarkIds() {
        UserDefaults.standard.set(cachedBookmarks, forKey: bookmarksKey)
    }

    private func persistStoredPosts() {
        let encoder = JSONEncoder()
        let storedPosts = cachedBookmarks.compactMap { cachedBookmarkedPosts[$0] }
        if let data = try? encoder.encode(storedPosts) {
            UserDefaults.standard.set(data, forKey: bookmarkedPostsKey)
        } else {
            UserDefaults.standard.removeObject(forKey: bookmarkedPostsKey)
        }
    }

    private func cleanupIfNeeded() {
        let idSet = Set(cachedBookmarks)
        var didChange = false
        let filteredPosts = cachedBookmarkedPosts.filter { idSet.contains($0.key) }
        if filteredPosts.count != cachedBookmarkedPosts.count {
            cachedBookmarkedPosts = filteredPosts
            didChange = true
        }
        let filteredIds = cachedBookmarks.filter { cachedBookmarkedPosts[$0] != nil }
        if filteredIds.count != cachedBookmarks.count {
            cachedBookmarks = filteredIds
            didChange = true
        }
        if didChange {
            persistBookmarkIds()
            persistStoredPosts()
        }
    }
}
