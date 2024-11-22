//
//  Post.swift
//  TechBlogNotifications
//
//  Created by 이상현 on 9/25/24.
//

import Foundation

@Observable
class Post: Identifiable {
    var id: Int64
    var link: String
    var baseUrl: String
    var blogName: String
    var title: String
    var pubDate: Date
    var scrapedDate: Date
    
    var isWatched: Bool = false
    var isBookmarked: Bool = false
    
    init(from dto: PostDTO) {
        self.id = dto.id
        self.link = dto.link
        self.baseUrl = Post.extractDomain(from: dto.link) ?? dto.link
        self.blogName = dto.blogName
        self.title = dto.title
        self.pubDate = dto.pubDate
        self.scrapedDate = dto.scrapedDate
    }
    
    init(from dto: PostDTO, isWatched: Bool, isBookmarked: Bool) {
        self.id = dto.id
        self.link = dto.link
        self.baseUrl = Post.extractDomain(from: dto.link) ?? dto.link
        self.blogName = dto.blogName
        self.title = dto.title
        self.pubDate = dto.pubDate
        self.scrapedDate = dto.scrapedDate
        self.isWatched = isWatched
        self.isBookmarked = isBookmarked
    }
    
    init(id: Int64, link: String, blogName: String, title: String, pubDate: Date, scrapedDate: Date, isWatched: Bool, isBookmarked: Bool) {
        self.id = id
        self.link = link
        self.baseUrl = Post.extractDomain(from: link) ?? link
        self.blogName = blogName
        self.title = title
        self.pubDate = pubDate
        self.scrapedDate = scrapedDate
        self.isWatched = isWatched
        self.isBookmarked = isBookmarked
    }
}

extension Post {
    // 블로그 글 도메인에서 baseURL 추출하는 메소드
    static func extractDomain(from urlString: String) -> String? {
        guard let url = URL(string: urlString),
              let scheme = url.scheme,
              let host = url.host else {
            return nil
        }
        
        return "\(scheme)://\(host)"
    }
}
