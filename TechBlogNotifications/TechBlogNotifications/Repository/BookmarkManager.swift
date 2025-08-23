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
    private var cachedBookmarks: [String] = []

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

    func fetchBookmarks() -> [String] {
        return UserDefaults.standard.array(forKey: bookmarksKey) as? [String] ?? []
    }

    func fetchBookmarkedPosts(from posts: [Post]) -> [Post] {
        return posts.filter { cachedBookmarks.contains($0.id) }
    }
    
    func isBookmarked(id: String) -> Bool {
        return cachedBookmarks.contains(id)
    }
}
