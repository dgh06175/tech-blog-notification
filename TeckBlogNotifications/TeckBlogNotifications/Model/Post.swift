//
//  Item.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 5/29/24.
//

import Foundation
import SwiftData

@Model
final class Post {
    @Attribute(.unique) var link: String
    var blogName: String
    var title: String
    var timestamp: Date
    var isBookMark: Bool
    var bookMarkCount: Int
    var isSeen: Bool
    var tags: [String]
    
    init(blogName: String, link: String, title: String, timestamp: Date, isBookMark: Bool = false, bookMarkCount: Int, isSeen: Bool = false, tags: [String]) {
        self.blogName = blogName
        self.link = link
        self.title = title
        self.isBookMark = isBookMark
        self.bookMarkCount = bookMarkCount
        self.isSeen = isSeen
        self.tags = tags
        self.timestamp = timestamp
    }
}
