//
//  BookmarkManager.swift
//  TechBlogNotifications
//
//  Created by 이상현 on 9/25/24.
//

import Foundation

@Observable
class BookmarkManager {
    private let bookmarksKey = "bookmarks"
    private var cachedBookmarks: [Int64] = []

    init() {
        self.cachedBookmarks = fetchBookmarks()
    }
    
    func saveBookmark(post: Post) {
        if !cachedBookmarks.contains(post.id) {
            cachedBookmarks.append(post.id)
            UserDefaults.standard.set(cachedBookmarks, forKey: bookmarksKey)
        }
    }

    func removeBookmark(post: Post) {
        if let index = cachedBookmarks.firstIndex(of: post.id) {
            cachedBookmarks.remove(at: index)
            UserDefaults.standard.set(cachedBookmarks, forKey: bookmarksKey)
        }
    }

    func fetchBookmarks() -> [Int64] {
        return UserDefaults.standard.array(forKey: bookmarksKey) as? [Int64] ?? []
    }

    func fetchBookmarkedPosts(from posts: [Post]) -> [Post] {
        return posts.filter { cachedBookmarks.contains($0.id) }
    }
    
    func isBookmarked(id: Int64) -> Bool {
        return cachedBookmarks.contains(id)
    }
}
